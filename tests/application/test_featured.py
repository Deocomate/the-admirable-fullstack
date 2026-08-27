import pytest

from admirable.application.use_cases.featured.add_featured import AddFeatured
from admirable.application.use_cases.featured.list_featured import ListFeatured
from admirable.application.use_cases.featured.remove_featured import RemoveFeatured
from admirable.application.use_cases.featured.reorder_featured import ReorderFeatured
from admirable.domain.entities.figure import Figure
from admirable.domain.exceptions import BusinessRuleViolationError, EntityNotFoundError
from tests.fakes.fake_category_repository import FakeCategoryRepository
from tests.fakes.fake_featured_figure_repository import FakeFeaturedFigureRepository
from tests.fakes.fake_figure_repository import FakeFigureRepository


def _figure(name: str, slug: str) -> Figure:
    return Figure(
        id=None,
        name=name,
        slug=slug,
        short_description=None,
        key_facts=[],
        content_blocks=[],
        search_text="",
    )


async def test_add_featured_assigns_next_priority() -> None:
    figures = FakeFigureRepository()
    featured = FakeFeaturedFigureRepository(figures)
    f1 = await figures.add(_figure("A", "a"))
    f2 = await figures.add(_figure("B", "b"))

    first = await AddFeatured(featured, figures).execute(f1.id)  # type: ignore[arg-type]
    second = await AddFeatured(featured, figures).execute(f2.id)  # type: ignore[arg-type]

    assert first.priority == 0
    assert second.priority == 1


async def test_add_featured_rejects_duplicate() -> None:
    figures = FakeFigureRepository()
    featured = FakeFeaturedFigureRepository(figures)
    f1 = await figures.add(_figure("A", "a"))
    await AddFeatured(featured, figures).execute(f1.id)  # type: ignore[arg-type]

    with pytest.raises(BusinessRuleViolationError):
        await AddFeatured(featured, figures).execute(f1.id)  # type: ignore[arg-type]


async def test_add_featured_missing_figure_raises() -> None:
    figures = FakeFigureRepository()
    featured = FakeFeaturedFigureRepository(figures)
    with pytest.raises(EntityNotFoundError):
        await AddFeatured(featured, figures).execute(999)


async def test_remove_and_list_featured() -> None:
    figures = FakeFigureRepository()
    featured = FakeFeaturedFigureRepository(figures)
    f1 = await figures.add(_figure("A", "a"))
    added = await AddFeatured(featured, figures).execute(f1.id)  # type: ignore[arg-type]

    listed = await ListFeatured(featured, FakeCategoryRepository()).execute()
    assert len(listed) == 1

    await RemoveFeatured(featured).execute(added.id)  # type: ignore[arg-type]
    listed = await ListFeatured(featured, FakeCategoryRepository()).execute()
    assert listed == []


async def test_reorder_featured() -> None:
    figures = FakeFigureRepository()
    featured = FakeFeaturedFigureRepository(figures)
    f1 = await figures.add(_figure("A", "a"))
    f2 = await figures.add(_figure("B", "b"))
    await AddFeatured(featured, figures).execute(f1.id)  # type: ignore[arg-type]
    await AddFeatured(featured, figures).execute(f2.id)  # type: ignore[arg-type]

    await ReorderFeatured(featured).execute([f2.id, f1.id])  # type: ignore[list-item]

    listed = await ListFeatured(featured, FakeCategoryRepository()).execute()
    assert [item.figure_slug for item in listed] == ["b", "a"]
