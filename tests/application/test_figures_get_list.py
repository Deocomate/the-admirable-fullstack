from admirable.application.dto.category_dto import CreateCategoryCommand
from admirable.application.dto.figure_dto import CreateFigureCommand
from admirable.application.use_cases.categories.create_category import CreateCategory
from admirable.application.use_cases.figures.create_figure import CreateFigure
from admirable.application.use_cases.figures.get_figure import GetFigure
from admirable.application.use_cases.figures.list_figures import ListFigures, ListFiguresQuery
from tests.fakes.fake_category_repository import FakeCategoryRepository
from tests.fakes.fake_figure_repository import FakeFigureRepository
from tests.fakes.fake_file_storage import FakeFileStorage
from tests.fakes.fake_story_snippet_repository import FakeStorySnippetRepository


async def test_get_figure_includes_category_names() -> None:
    figures = FakeFigureRepository()
    categories = FakeCategoryRepository()
    storage = FakeFileStorage()

    category = await CreateCategory(categories).execute(CreateCategoryCommand(name="Science"))
    created = await CreateFigure(figures, storage).execute(
        CreateFigureCommand(name="Marie Curie", category_ids=[category.id])
    )

    result = await GetFigure(figures, categories).execute(created.id)
    assert result.category_names == ["Science"]


async def test_list_figures_includes_story_counts() -> None:
    figures = FakeFigureRepository()
    categories = FakeCategoryRepository()
    story_snippets = FakeStorySnippetRepository()
    storage = FakeFileStorage()

    await CreateFigure(figures, storage).execute(CreateFigureCommand(name="A"))
    await CreateFigure(figures, storage).execute(CreateFigureCommand(name="B"))

    result = await ListFigures(figures, categories, story_snippets).execute(
        ListFiguresQuery(page=1, per_page=15)
    )
    assert result.total == 2
    assert all(item.story_snippets_count == 0 for item in result.items)
