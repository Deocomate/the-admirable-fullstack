from sqlalchemy.ext.asyncio import AsyncSession

from admirable.domain.entities.category import Category
from admirable.domain.entities.featured_figure import FeaturedFigure
from admirable.domain.entities.figure import Figure
from admirable.domain.value_objects.content_block import parse_content_blocks
from admirable.infrastructure.db.repositories.category_repository_impl import CategoryRepositoryImpl
from admirable.infrastructure.db.repositories.featured_figure_repository_impl import (
    FeaturedFigureRepositoryImpl,
)
from admirable.infrastructure.db.repositories.figure_repository_impl import FigureRepositoryImpl
from tests.integration.sql_counter import SqlCounter


def make_figure(name: str, slug: str) -> Figure:
    blocks = parse_content_blocks([{"type": "heading", "text_en": f"About {name} — cà phê ☕"}])
    return Figure(
        id=None,
        name=name,
        slug=slug,
        short_description="A short bio",
        key_facts=[],
        content_blocks=blocks,
        search_text=f"About {name}",
    )


async def test_add_and_get_by_id(db_session: AsyncSession) -> None:
    repo = FigureRepositoryImpl(db_session)
    figure = await repo.add(make_figure("Marie Curie", "marie-curie-it"))
    assert figure.id is not None

    fetched = await repo.get_by_id(figure.id)
    assert fetched is not None
    assert fetched.slug == "marie-curie-it"
    # Vietnamese diacritics + emoji round-trip through JSON storage intact
    assert fetched.content_blocks[0].text_en == "About Marie Curie — cà phê ☕"


async def test_get_by_slug(db_session: AsyncSession) -> None:
    repo = FigureRepositoryImpl(db_session)
    await repo.add(make_figure("Alan Turing", "alan-turing-it"))
    fetched = await repo.get_by_slug("alan-turing-it")
    assert fetched is not None
    assert fetched.name == "Alan Turing"


async def test_slug_exists(db_session: AsyncSession) -> None:
    repo = FigureRepositoryImpl(db_session)
    figure = await repo.add(make_figure("Ada Lovelace", "ada-lovelace-it"))
    assert await repo.slug_exists("ada-lovelace-it") is True
    assert await repo.slug_exists("ada-lovelace-it", exclude_id=figure.id) is False
    assert await repo.slug_exists("nonexistent-it") is False


async def test_update_and_delete(db_session: AsyncSession) -> None:
    repo = FigureRepositoryImpl(db_session)
    figure = await repo.add(make_figure("Grace Hopper", "grace-hopper-it"))
    figure.name = "Grace Murray Hopper"
    updated = await repo.update(figure)
    assert updated.name == "Grace Murray Hopper"

    await repo.delete(figure.id)  # type: ignore[arg-type]
    assert await repo.get_by_id(figure.id) is None  # type: ignore[arg-type]


async def test_sync_categories(db_session: AsyncSession) -> None:
    category_repo = CategoryRepositoryImpl(db_session)
    figure_repo = FigureRepositoryImpl(db_session)

    cat_a = await category_repo.add(Category(id=None, name="Scientists IT", slug="scientists-it"))
    cat_b = await category_repo.add(Category(id=None, name="Engineers IT", slug="engineers-it"))
    figure = await figure_repo.add(make_figure("Katherine Johnson", "katherine-johnson-it"))
    assert cat_a.id is not None
    assert cat_b.id is not None
    assert figure.id is not None

    await figure_repo.sync_categories(figure.id, [cat_a.id, cat_b.id])
    fetched = await figure_repo.get_by_id(figure.id)
    assert fetched is not None
    assert sorted(fetched.category_ids) == sorted([cat_a.id, cat_b.id])

    await figure_repo.sync_categories(figure.id, [cat_a.id])
    fetched = await figure_repo.get_by_id(figure.id)
    assert fetched is not None
    assert fetched.category_ids == [cat_a.id]


async def test_list_paginated_no_n_plus_one(
    db_session: AsyncSession, sql_counter: SqlCounter
) -> None:
    repo = FigureRepositoryImpl(db_session)
    for i in range(5):
        await repo.add(make_figure(f"Person {i}", f"person-{i}-it"))
    await db_session.flush()

    sql_counter.reset()
    page = await repo.list_paginated(search=None, category_id=None, page=1, per_page=15)
    assert len(page.items) >= 5
    # 1 count query + 1 data query + 1 selectinload(categories) query = 3
    assert sql_counter.count <= 3, f"expected <=3 queries, got {sql_counter.count}"


async def test_search_featured_first_ordering(db_session: AsyncSession) -> None:
    figure_repo = FigureRepositoryImpl(db_session)
    featured_repo = FeaturedFigureRepositoryImpl(db_session)

    plain = await figure_repo.add(make_figure("Plain Person", "plain-person-it"))
    featured = await figure_repo.add(make_figure("Featured Person", "featured-person-it"))
    await db_session.flush()
    await featured_repo.add(FeaturedFigure(id=None, figure_id=featured.id, priority=0))  # type: ignore[arg-type]

    page = await figure_repo.search(query="Person", category_slug=None, page=1, per_page=10)
    slugs = [f.slug for f in page.items]
    assert slugs.index("featured-person-it") < slugs.index("plain-person-it")
    _ = plain
