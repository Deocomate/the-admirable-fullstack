"""Migrate business data from the Laravel source database to the new
`admirable` target database. Read-only against the source, idempotent
against the target (INSERT ... ON DUPLICATE KEY UPDATE), preserves primary
keys.

Usage:
    uv run python scripts/migrate_data.py \\
        --source-url mysql+asyncmy://... [--dry-run] [--with-media]
"""

import asyncio
import json
import logging
import shutil
from collections.abc import Sequence
from pathlib import Path

import typer
from sqlalchemy import RowMapping, text
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from admirable.config import get_settings
from admirable.domain.value_objects.audio_status import AudioStatus
from admirable.domain.value_objects.content_block import build_search_text, parse_content_blocks

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("migrate_data")

app = typer.Typer(add_completion=False)

_VALID_AUDIO_STATUSES = {s.value for s in AudioStatus}


async def _fetch(conn: AsyncConnection, sql: str) -> Sequence[RowMapping]:
    return (await conn.execute(text(sql))).mappings().all()


def _build_search_text(content_blocks_raw: str | None, fallback_content: str | None) -> str:
    if content_blocks_raw:
        try:
            raw = json.loads(content_blocks_raw)
        except (TypeError, ValueError):
            raw = []
        blocks = parse_content_blocks(raw if isinstance(raw, list) else [])
        text_out = build_search_text(blocks)
        if text_out:
            return text_out
    return fallback_content or ""


def _normalize_audio_status(raw: str | None) -> str:
    if raw in _VALID_AUDIO_STATUSES:
        return raw
    if raw is not None:
        logger.warning("Unknown audio_status %r, mapping to 'idle'", raw)
    return "idle"


async def _migrate_users(source: AsyncConnection, target: AsyncConnection) -> None:
    rows = await _fetch(
        source, "SELECT id, name, role, email, password, created_at, updated_at FROM users"
    )
    for row in rows:
        role = row["role"] if row["role"] in ("superadmin", "admin") else "admin"
        if role != row["role"]:
            logger.warning(
                "User %s has unknown role %r, mapping to 'admin'", row["id"], row["role"]
            )
        await target.execute(
            text(
                "INSERT INTO users (id, name, role, email, password, created_at, updated_at) "
                "VALUES (:id, :name, :role, :email, :password, :created_at, :updated_at) "
                "ON DUPLICATE KEY UPDATE name=:name, role=:role, email=:email, "
                "password=:password, updated_at=:updated_at"
            ),
            {**dict(row), "role": role},
        )
    logger.info("users: migrated %d rows", len(rows))


async def _migrate_categories(source: AsyncConnection, target: AsyncConnection) -> None:
    rows = await _fetch(source, "SELECT id, name, slug, created_at, updated_at FROM categories")
    for row in rows:
        await target.execute(
            text(
                "INSERT INTO categories (id, name, slug, created_at, updated_at) "
                "VALUES (:id, :name, :slug, :created_at, :updated_at) "
                "ON DUPLICATE KEY UPDATE name=:name, slug=:slug, updated_at=:updated_at"
            ),
            dict(row),
        )
    logger.info("categories: migrated %d rows", len(rows))


async def _migrate_figures(source: AsyncConnection, target: AsyncConnection) -> int:
    rows = await _fetch(
        source,
        "SELECT id, name, slug, avatar_path, short_description, key_facts, content_blocks, "
        "content, audio_path, audio_status, audio_error, youtube_url, created_at, updated_at "
        "FROM figures",
    )
    empty_search_with_blocks = 0
    for row in rows:
        content_blocks = row["content_blocks"]
        content = row["content"]
        assert isinstance(content_blocks, str | None)
        assert isinstance(content, str | None)
        search_text = _build_search_text(content_blocks, content)
        if not search_text and content_blocks not in (None, "", "[]"):
            empty_search_with_blocks += 1
        await target.execute(
            text(
                "INSERT INTO figures (id, name, slug, avatar_path, short_description, key_facts, "
                "content_blocks, search_text, audio_path, audio_status, audio_error, youtube_url, "
                "created_at, updated_at) "
                "VALUES (:id, :name, :slug, :avatar_path, :short_description, :key_facts, "
                ":content_blocks, :search_text, :audio_path, :audio_status, :audio_error, "
                ":youtube_url, :created_at, :updated_at) "
                "ON DUPLICATE KEY UPDATE name=:name, slug=:slug, avatar_path=:avatar_path, "
                "short_description=:short_description, key_facts=:key_facts, "
                "content_blocks=:content_blocks, search_text=:search_text, audio_path=:audio_path, "
                "audio_status=:audio_status, audio_error=:audio_error, youtube_url=:youtube_url, "
                "updated_at=:updated_at"
            ),
            {
                "id": row["id"],
                "name": row["name"],
                "slug": row["slug"],
                "avatar_path": row["avatar_path"],
                "short_description": row["short_description"],
                "key_facts": row["key_facts"],
                "content_blocks": content_blocks,
                "search_text": search_text,
                "audio_path": row["audio_path"],
                "audio_status": _normalize_audio_status(row["audio_status"]),
                "audio_error": row["audio_error"],
                "youtube_url": row["youtube_url"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            },
        )
    if empty_search_with_blocks:
        logger.warning(
            "figures: %d rows have non-empty content_blocks but empty search_text",
            empty_search_with_blocks,
        )
    logger.info("figures: migrated %d rows", len(rows))
    return len(rows)


async def _migrate_category_figure(source: AsyncConnection, target: AsyncConnection) -> None:
    rows = await _fetch(source, "SELECT category_id, figure_id FROM category_figure")
    for row in rows:
        await target.execute(
            text(
                "INSERT INTO category_figure (category_id, figure_id) "
                "VALUES (:category_id, :figure_id) "
                "ON DUPLICATE KEY UPDATE category_id=category_id"
            ),
            dict(row),
        )
    logger.info("category_figure: migrated %d rows", len(rows))


async def _migrate_story_snippets(source: AsyncConnection, target: AsyncConnection) -> int:
    rows = await _fetch(
        source,
        "SELECT id, figure_id, title, subtitle, content_blocks, content, image_path, "
        "audio_path, audio_status, audio_error, youtube_url, created_at, updated_at "
        "FROM story_snippets",
    )
    for row in rows:
        content_blocks = row["content_blocks"]
        content = row["content"]
        assert isinstance(content_blocks, str | None)
        assert isinstance(content, str | None)
        search_text = _build_search_text(content_blocks, content)
        await target.execute(
            text(
                "INSERT INTO story_snippets (id, figure_id, title, subtitle, content_blocks, "
                "search_text, image_path, audio_path, audio_status, audio_error, youtube_url, "
                "created_at, updated_at) "
                "VALUES (:id, :figure_id, :title, :subtitle, :content_blocks, :search_text, "
                ":image_path, :audio_path, :audio_status, :audio_error, :youtube_url, "
                ":created_at, :updated_at) "
                "ON DUPLICATE KEY UPDATE title=:title, subtitle=:subtitle, "
                "content_blocks=:content_blocks, search_text=:search_text, image_path=:image_path, "
                "audio_path=:audio_path, audio_status=:audio_status, audio_error=:audio_error, "
                "youtube_url=:youtube_url, updated_at=:updated_at"
            ),
            {
                "id": row["id"],
                "figure_id": row["figure_id"],
                "title": row["title"],
                "subtitle": row["subtitle"],
                "content_blocks": content_blocks,
                "search_text": search_text,
                "image_path": row["image_path"],
                "audio_path": row["audio_path"],
                "audio_status": _normalize_audio_status(row["audio_status"]),
                "audio_error": row["audio_error"],
                "youtube_url": row["youtube_url"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            },
        )
    logger.info("story_snippets: migrated %d rows", len(rows))
    return len(rows)


async def _migrate_featured_figures(source: AsyncConnection, target: AsyncConnection) -> None:
    rows = await _fetch(
        source, "SELECT id, figure_id, priority, created_at, updated_at FROM featured_figures"
    )
    for row in rows:
        await target.execute(
            text(
                "INSERT INTO featured_figures (id, figure_id, priority, created_at, updated_at) "
                "VALUES (:id, :figure_id, :priority, :created_at, :updated_at) "
                "ON DUPLICATE KEY UPDATE priority=:priority, updated_at=:updated_at"
            ),
            dict(row),
        )
    logger.info("featured_figures: migrated %d rows", len(rows))


async def _migrate_settings(source: AsyncConnection, target: AsyncConnection) -> None:
    rows = await _fetch(source, "SELECT `key`, value, created_at, updated_at FROM settings")
    for row in rows:
        await target.execute(
            text(
                "INSERT INTO settings (`key`, value, created_at, updated_at) "
                "VALUES (:key, :value, :created_at, :updated_at) "
                "ON DUPLICATE KEY UPDATE value=:value, updated_at=:updated_at"
            ),
            dict(row),
        )
    logger.info("settings: migrated %d rows", len(rows))


async def _migrate_contacts(source: AsyncConnection, target: AsyncConnection) -> None:
    rows = await _fetch(
        source,
        "SELECT id, type, label, value, icon, sort_order, is_active, created_at, updated_at "
        "FROM contacts",
    )
    for row in rows:
        await target.execute(
            text(
                "INSERT INTO contacts (id, type, label, value, icon, sort_order, is_active, "
                "created_at, updated_at) "
                "VALUES (:id, :type, :label, :value, :icon, :sort_order, :is_active, "
                ":created_at, :updated_at) "
                "ON DUPLICATE KEY UPDATE type=:type, label=:label, value=:value, icon=:icon, "
                "sort_order=:sort_order, is_active=:is_active, updated_at=:updated_at"
            ),
            dict(row),
        )
    logger.info("contacts: migrated %d rows", len(rows))


_TABLES_WITH_SURROGATE_KEYS = (
    "users",
    "figures",
    "story_snippets",
    "featured_figures",
    "contacts",
    "categories",
)


async def _reset_auto_increment(target: AsyncConnection) -> None:
    for table in _TABLES_WITH_SURROGATE_KEYS:
        result = await target.execute(text(f"SELECT MAX(id) AS max_id FROM {table}"))
        max_id = result.scalar() or 0
        await target.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = {max_id + 1}"))
    logger.info("AUTO_INCREMENT reset on all tables with surrogate keys")


def _copy_media(project_root: Path) -> list[str]:
    source_dir = project_root / "storage" / "app" / "public" / "uploads"
    target_dir = project_root / "media" / "uploads"
    target_dir.mkdir(parents=True, exist_ok=True)
    if source_dir.exists():
        shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
        logger.info("Copied media from %s to %s", source_dir, target_dir)
    else:
        logger.warning("Source media directory not found: %s", source_dir)
    return []


async def _run(source_url: str, dry_run: bool, with_media: bool) -> None:
    settings = get_settings()
    source_engine = create_async_engine(source_url)
    target_engine = create_async_engine(settings.db.dsn)

    async with source_engine.connect() as source_conn, target_engine.begin() as target_conn:
        await _migrate_users(source_conn, target_conn)
        await _migrate_categories(source_conn, target_conn)
        await _migrate_figures(source_conn, target_conn)
        await _migrate_category_figure(source_conn, target_conn)
        await _migrate_story_snippets(source_conn, target_conn)
        await _migrate_featured_figures(source_conn, target_conn)
        await _migrate_settings(source_conn, target_conn)
        await _migrate_contacts(source_conn, target_conn)

        if dry_run:
            logger.info("--dry-run: rolling back target transaction")
            await target_conn.rollback()
            await source_engine.dispose()
            await target_engine.dispose()
            return

        await _reset_auto_increment(target_conn)

    if with_media:
        missing = _copy_media(Path(__file__).resolve().parent.parent)
        if missing:
            backups_dir = Path(__file__).resolve().parent.parent / "backups"
            backups_dir.mkdir(exist_ok=True)
            (backups_dir / "missing-media.txt").write_text("\n".join(missing), encoding="utf-8")

    await source_engine.dispose()
    await target_engine.dispose()
    logger.info("Migration complete.")


@app.command()
def main(
    source_url: str = typer.Option(
        ..., help="Source DB URL, e.g. mysql+asyncmy://ro:pw@host/db"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Roll back the target transaction at the end."
    ),
    with_media: bool = typer.Option(
        False, "--with-media", help="Also copy uploads/ into media/."
    ),
) -> None:
    asyncio.run(_run(source_url, dry_run, with_media))


if __name__ == "__main__":
    app()
