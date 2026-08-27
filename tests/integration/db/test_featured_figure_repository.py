from sqlalchemy.ext.asyncio import AsyncSession

from admirable.domain.entities.featured_figure import FeaturedFigure
from admirable.domain.entities.figure import Figure
from admirable.infrastructure.db.repositories.featured_figure_repository_impl import (
    FeaturedFigureRepositoryImpl,
)
from admirable.infrastructure.db.repositories.figure_repository_impl import FigureRepositoryImpl


def make_figure(slug: str) -> Figure:
    return Figure(
        id=None,
        name="Featured Figure",
        slug=slug,
        short_description=None,
        key_facts=[],
        content_blocks=[],
        search_text="",
    )


async def test_reorder_and_list_ordered(db_session: AsyncSession) -> None:
    figure_repo = FigureRepositoryImpl(db_session)
    featured_repo = FeaturedFigureRepositoryImpl(db_session)

    f1 = await figure_repo.add(make_figure("ff-1-it"))
    f2 = await figure_repo.add(make_figure("ff-2-it"))
    await db_session.flush()

    await featured_repo.add(FeaturedFigure(id=None, figure_id=f1.id, priority=0))  # type: ignore[arg-type]
    await featured_repo.add(FeaturedFigure(id=None, figure_id=f2.id, priority=1))  # type: ignore[arg-type]

    await featured_repo.reorder([f2.id, f1.id])  # type: ignore[list-item]

    ordered = await featured_repo.list_ordered_with_figure()
    slugs = [figure.slug for _, figure in ordered if figure.slug in ("ff-1-it", "ff-2-it")]
    assert slugs == ["ff-2-it", "ff-1-it"]


async def test_available_figures_excludes_featured(db_session: AsyncSession) -> None:
    figure_repo = FigureRepositoryImpl(db_session)
    featured_repo = FeaturedFigureRepositoryImpl(db_session)

    featured = await figure_repo.add(make_figure("avail-featured-it"))
    unfeatured = await figure_repo.add(make_figure("avail-plain-it"))
    await db_session.flush()
    await featured_repo.add(FeaturedFigure(id=None, figure_id=featured.id, priority=0))  # type: ignore[arg-type]

    available = await featured_repo.list_available_figures(search=None, limit=100)
    slugs = {f.slug for f in available}
    assert "avail-plain-it" in slugs
    assert "avail-featured-it" not in slugs
    _ = unfeatured
