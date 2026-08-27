import pytest

from admirable.application.dto.category_dto import CreateCategoryCommand
from admirable.application.dto.contact_dto import CreateContactCommand
from admirable.application.dto.figure_dto import CreateFigureCommand
from admirable.application.dto.story_dto import CreateStoryCommand
from admirable.application.use_cases.categories.create_category import CreateCategory
from admirable.application.use_cases.contacts.create_contact import CreateContact
from admirable.application.use_cases.figures.create_figure import CreateFigure
from admirable.application.use_cases.public.get_about_us_page import GetAboutUsPage
from admirable.application.use_cases.public.get_category_page import GetCategoryPage
from admirable.application.use_cases.public.get_contact_page import GetContactPage
from admirable.application.use_cases.public.get_figure_detail import GetFigureDetail
from admirable.application.use_cases.public.get_story_detail import GetStoryDetail
from admirable.application.use_cases.public.list_categories import ListCategories
from admirable.application.use_cases.public.search_figures import SearchFigures, SearchFiguresQuery
from admirable.application.use_cases.stories.create_story import CreateStory
from admirable.domain.exceptions import EntityNotFoundError
from tests.fakes.fake_category_repository import FakeCategoryRepository
from tests.fakes.fake_contact_repository import FakeContactRepository
from tests.fakes.fake_figure_repository import FakeFigureRepository
from tests.fakes.fake_file_storage import FakeFileStorage
from tests.fakes.fake_setting_repository import FakeSettingRepository
from tests.fakes.fake_story_snippet_repository import FakeStorySnippetRepository


async def test_search_figures_by_name() -> None:
    figures = FakeFigureRepository()
    categories = FakeCategoryRepository()
    story_snippets = FakeStorySnippetRepository()
    storage = FakeFileStorage()

    await CreateFigure(figures, storage).execute(CreateFigureCommand(name="Marie Curie"))
    await CreateFigure(figures, storage).execute(CreateFigureCommand(name="Alan Turing"))

    result = await SearchFigures(figures, categories, story_snippets).execute(
        SearchFiguresQuery(query="Curie")
    )
    assert result.total == 1
    assert result.figures[0].name == "Marie Curie"


async def test_get_figure_detail_includes_related() -> None:
    figures = FakeFigureRepository()
    categories = FakeCategoryRepository()
    story_snippets = FakeStorySnippetRepository()
    storage = FakeFileStorage()

    category = await CreateCategory(categories).execute(CreateCategoryCommand(name="Science"))
    main = await CreateFigure(figures, storage).execute(
        CreateFigureCommand(name="Marie Curie", category_ids=[category.id])
    )
    await CreateFigure(figures, storage).execute(
        CreateFigureCommand(name="Albert Einstein", category_ids=[category.id])
    )

    result = await GetFigureDetail(figures, categories, story_snippets).execute(main.slug)
    assert result.name == "Marie Curie"
    assert len(result.related_figures) == 1
    assert result.related_figures[0].name == "Albert Einstein"


async def test_get_figure_detail_missing_slug_raises() -> None:
    figures = FakeFigureRepository()
    categories = FakeCategoryRepository()
    story_snippets = FakeStorySnippetRepository()

    with pytest.raises(EntityNotFoundError):
        await GetFigureDetail(figures, categories, story_snippets).execute("no-such-slug")


async def test_get_story_detail_includes_other_stories() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    storage = FakeFileStorage()
    figure = await CreateFigure(figures, storage).execute(CreateFigureCommand(name="Marie Curie"))

    s1 = await CreateStory(story_snippets, figures, storage).execute(
        CreateStoryCommand(figure_id=figure.id, title="Chapter 1")
    )
    await CreateStory(story_snippets, figures, storage).execute(
        CreateStoryCommand(figure_id=figure.id, title="Chapter 2")
    )

    result = await GetStoryDetail(story_snippets, figures).execute(s1.id)
    assert result.snippet.title == "Chapter 1"
    assert len(result.other_stories) == 1
    assert result.other_stories[0].title == "Chapter 2"


async def test_get_category_page_filters_by_slug() -> None:
    figures = FakeFigureRepository()
    categories = FakeCategoryRepository()
    story_snippets = FakeStorySnippetRepository()
    storage = FakeFileStorage()

    cat = await CreateCategory(categories).execute(CreateCategoryCommand(name="Science"))
    await CreateFigure(figures, storage).execute(
        CreateFigureCommand(name="Marie Curie", category_ids=[cat.id])
    )
    await CreateFigure(figures, storage).execute(CreateFigureCommand(name="Unrelated"))

    result = await GetCategoryPage(figures, categories, story_snippets).execute(cat.slug)
    assert result.category is not None
    assert result.total == 1
    assert result.figures[0].name == "Marie Curie"


async def test_get_category_page_missing_slug_raises() -> None:
    figures = FakeFigureRepository()
    categories = FakeCategoryRepository()
    story_snippets = FakeStorySnippetRepository()

    with pytest.raises(EntityNotFoundError):
        await GetCategoryPage(figures, categories, story_snippets).execute("nonexistent")


async def test_list_categories_public() -> None:
    categories = FakeCategoryRepository()
    await CreateCategory(categories).execute(CreateCategoryCommand(name="A"))
    result = await ListCategories(categories).execute()
    assert len(result) == 1


async def test_get_about_us_page() -> None:
    settings = FakeSettingRepository()
    result = await GetAboutUsPage(settings).execute()
    assert "hero" in result.data


async def test_get_contact_page_only_active() -> None:
    contacts = FakeContactRepository()
    await CreateContact(contacts).execute(
        CreateContactCommand(type="email", label="Active", value="a", is_active=True)
    )
    await CreateContact(contacts).execute(
        CreateContactCommand(type="email", label="Inactive", value="b", is_active=False)
    )

    result = await GetContactPage(contacts).execute()
    assert len(result.contacts) == 1
    assert result.contacts[0].label == "Active"
