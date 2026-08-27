"""Verify the target database matches the source after migration.

Usage:
    uv run python scripts/verify_migration.py --source-url mysql+asyncmy://...
"""

import asyncio
from pathlib import Path

import typer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from admirable.config import get_settings

app = typer.Typer(add_completion=False)

_TABLES = [
    "users",
    "categories",
    "figures",
    "category_figure",
    "story_snippets",
    "featured_figures",
    "settings",
    "contacts",
]


async def _count(conn: object, table: str) -> int:
    result = await conn.execute(text(f"SELECT COUNT(*) FROM {table}"))  # type: ignore[attr-defined]
    return result.scalar() or 0


async def _run(source_url: str) -> bool:
    settings = get_settings()
    source_engine = create_async_engine(source_url)
    target_engine = create_async_engine(settings.db.dsn)
    ok = True

    async with source_engine.connect() as source_conn, target_engine.connect() as target_conn:
        print(f"{'table':<20} {'source':>10} {'target':>10} {'match':>8}")
        for table in _TABLES:
            source_count = await _count(source_conn, table)
            target_count = await _count(target_conn, table)
            match = source_count == target_count
            ok = ok and match
            status = "OK" if match else "MISMATCH"
            print(f"{table:<20} {source_count:>10} {target_count:>10} {status:>8}")

        replacement_char = await target_conn.execute(
            text(
                "SELECT COUNT(*) FROM figures WHERE name LIKE '%�%' "
                "OR search_text LIKE '%�%'"
            )
        )
        bad_encoding = replacement_char.scalar() or 0
        print(f"\nRows with U+FFFD (bad encoding): {bad_encoding}")
        ok = ok and bad_encoding == 0

        empty_search = await target_conn.execute(
            text(
                "SELECT COUNT(*) FROM figures WHERE (search_text IS NULL OR search_text = '') "
                "AND content_blocks IS NOT NULL AND content_blocks != '[]'"
            )
        )
        empty_search_count = empty_search.scalar() or 0
        print(f"Figures with empty search_text but non-empty content_blocks: {empty_search_count}")
        ok = ok and empty_search_count == 0

        orphan_snippets = await target_conn.execute(
            text(
                "SELECT COUNT(*) FROM story_snippets s "
                "LEFT JOIN figures f ON f.id = s.figure_id WHERE f.id IS NULL"
            )
        )
        orphan_snippets_count = orphan_snippets.scalar() or 0
        print(f"Orphan story_snippets (missing figure_id): {orphan_snippets_count}")
        ok = ok and orphan_snippets_count == 0

        orphan_featured = await target_conn.execute(
            text(
                "SELECT COUNT(*) FROM featured_figures ff "
                "LEFT JOIN figures f ON f.id = ff.figure_id WHERE f.id IS NULL"
            )
        )
        orphan_featured_count = orphan_featured.scalar() or 0
        print(f"Orphan featured_figures (missing figure_id): {orphan_featured_count}")
        ok = ok and orphan_featured_count == 0

        orphan_category_figure = await target_conn.execute(
            text(
                "SELECT COUNT(*) FROM category_figure cf "
                "LEFT JOIN figures f ON f.id = cf.figure_id "
                "LEFT JOIN categories c ON c.id = cf.category_id "
                "WHERE f.id IS NULL OR c.id IS NULL"
            )
        )
        orphan_cf_count = orphan_category_figure.scalar() or 0
        print(f"Orphan category_figure rows: {orphan_cf_count}")
        ok = ok and orphan_cf_count == 0

        try:
            fulltext_result = await target_conn.execute(
                text(
                    "SELECT COUNT(*) FROM figures "
                    "WHERE MATCH(name, short_description, search_text) "
                    "AGAINST('khoa' IN BOOLEAN MODE)"
                )
            )
            match_count = fulltext_result.scalar()
            print(f"\nFULLTEXT MATCH sample query ('khoa') returned {match_count} rows")
        except Exception as exc:
            print(f"\nFULLTEXT MATCH query failed: {exc}")
            ok = False

        backups_dir = Path(__file__).resolve().parent.parent / "backups"
        missing_media_path = backups_dir / "missing-media.txt"
        media_root = Path(__file__).resolve().parent.parent / "media"
        missing: list[str] = []
        for table, column in [
            ("figures", "avatar_path"),
            ("figures", "audio_path"),
            ("story_snippets", "image_path"),
            ("story_snippets", "audio_path"),
        ]:
            rows = await target_conn.execute(
                text(f"SELECT {column} AS path FROM {table} WHERE {column} IS NOT NULL")
            )
            for row in rows.mappings().all():
                rel_path = row["path"]
                if rel_path and not (media_root / rel_path).exists():
                    missing.append(f"{table}.{column}: {rel_path}")
        missing_media_path.parent.mkdir(exist_ok=True)
        missing_media_path.write_text("\n".join(missing), encoding="utf-8")
        print(f"\nMissing media files: {len(missing)} (see {missing_media_path})")

    await source_engine.dispose()
    await target_engine.dispose()
    return ok


@app.command()
def main(
    source_url: str = typer.Option(..., help="Source DB URL for read-only comparison."),
) -> None:
    ok = asyncio.run(_run(source_url))
    print(f"\n{'PASS' if ok else 'FAIL'}")
    raise typer.Exit(0 if ok else 1)


if __name__ == "__main__":
    app()
