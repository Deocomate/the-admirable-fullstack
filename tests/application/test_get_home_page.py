from admirable.application.use_cases.public.get_home_page import GetHomePage
from admirable.domain.entities.featured_figure import FeaturedFigure
from admirable.domain.entities.figure import Figure
from tests.fakes.fake_category_repository import FakeCategoryRepository
from tests.fakes.fake_featured_figure_repository import FakeFeaturedFigureRepository
from tests.fakes.fake_figure_repository import FakeFigureRepository
from tests.fakes.fake_story_snippet_repository import FakeStorySnippetRepository


def _blank_figure(name: str, slug: str) -> Figure:
    return Figure(
        id=None, name=name, slug=slug, short_description=None,
        key_facts=[], content_blocks=[], search_text="",
    )


async def _seed_figures(figures: FakeFigureRepository, count: int) -> list[Figure]:
    return [await figures.add(_blank_figure(f"Figure {i}", f"figure-{i}")) for i in range(count)]


_UseCaseFixture = tuple[GetHomePage, FakeFigureRepository, FakeFeaturedFigureRepository]


async def _make_use_case() -> _UseCaseFixture:
    figures = FakeFigureRepository()
    categories = FakeCategoryRepository()
    story_snippets = FakeStorySnippetRepository()
    featured = FakeFeaturedFigureRepository(figures)
    use_case = GetHomePage(figures, categories, story_snippets, featured)
    return use_case, figures, featured


async def test_zero_featured_backfills_all_six_from_latest() -> None:
    use_case, figures, _featured = await _make_use_case()
    await _seed_figures(figures, 10)

    page = await use_case.execute()

    assert page.featured_figure is None
    assert len(page.latest_figures) == 6
    assert all(not f.is_featured for f in page.latest_figures)


async def test_three_featured_backfills_remaining_three() -> None:
    use_case, figures, featured = await _make_use_case()
    seeded = await _seed_figures(figures, 10)
    for priority, figure in enumerate(seeded[:3]):
        await featured.add(FeaturedFigure(id=None, figure_id=figure.id, priority=priority))  # type: ignore[arg-type]

    page = await use_case.execute()

    assert page.featured_figure is not None
    assert page.featured_figure.is_featured is True
    assert len(page.latest_figures) == 6
    featured_in_latest = sum(1 for f in page.latest_figures if f.is_featured)
    assert featured_in_latest == 2  # 3 featured total minus 1 used as hero
    non_featured_in_latest = sum(1 for f in page.latest_figures if not f.is_featured)
    assert non_featured_in_latest == 4


async def test_six_featured_still_backfills_one() -> None:
    """`slice(1, 6)` on exactly 6 featured records yields only 5 — one
    non-featured backfill slot remains, matching Laravel's own behavior.
    Only >=7 featured records avoid backfill entirely (see the next test)."""
    use_case, figures, featured = await _make_use_case()
    seeded = await _seed_figures(figures, 10)
    for priority, figure in enumerate(seeded[:6]):
        await featured.add(FeaturedFigure(id=None, figure_id=figure.id, priority=priority))  # type: ignore[arg-type]

    page = await use_case.execute()

    assert page.featured_figure is not None
    assert len(page.latest_figures) == 6
    assert sum(1 for f in page.latest_figures if f.is_featured) == 5
    assert sum(1 for f in page.latest_figures if not f.is_featured) == 1


async def test_ten_featured_uses_top_seven_only() -> None:
    use_case, figures, featured = await _make_use_case()
    seeded = await _seed_figures(figures, 10)
    for priority, figure in enumerate(seeded):
        await featured.add(FeaturedFigure(id=None, figure_id=figure.id, priority=priority))  # type: ignore[arg-type]

    page = await use_case.execute()

    assert page.featured_figure is not None
    assert page.featured_figure.slug == "figure-0"
    assert len(page.latest_figures) == 6
    assert [f.slug for f in page.latest_figures] == [f"figure-{i}" for i in range(1, 7)]
