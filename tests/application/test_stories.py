import pytest

from admirable.application.dto.story_dto import CreateStoryCommand, UpdateStoryCommand
from admirable.application.use_cases.stories.create_story import CreateStory
from admirable.application.use_cases.stories.delete_story import DeleteStory
from admirable.application.use_cases.stories.get_story import GetStory
from admirable.application.use_cases.stories.list_stories import ListStories, ListStoriesQuery
from admirable.application.use_cases.stories.update_story import UpdateStory
from admirable.domain.entities.figure import Figure
from admirable.domain.exceptions import EntityNotFoundError
from tests.fakes.fake_figure_repository import FakeFigureRepository
from tests.fakes.fake_file_storage import FakeFileStorage
from tests.fakes.fake_story_snippet_repository import FakeStorySnippetRepository


async def _seed_figure(figures: FakeFigureRepository) -> Figure:
    return await figures.add(
        Figure(
            id=None,
            name="Marie Curie",
            slug="marie-curie",
            short_description=None,
            key_facts=[],
            content_blocks=[],
            search_text="",
        )
    )


async def test_create_story_requires_existing_figure() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    storage = FakeFileStorage()

    with pytest.raises(EntityNotFoundError):
        await CreateStory(story_snippets, figures, storage).execute(
            CreateStoryCommand(figure_id=999, title="Chapter 1")
        )


async def test_create_get_update_delete_story() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    storage = FakeFileStorage()
    figure = await _seed_figure(figures)

    created = await CreateStory(story_snippets, figures, storage).execute(
        CreateStoryCommand(figure_id=figure.id, title="Chapter 1")  # type: ignore[arg-type]
    )
    assert created.figure_name == "Marie Curie"

    fetched = await GetStory(story_snippets, figures).execute(created.id)
    assert fetched.title == "Chapter 1"

    updated = await UpdateStory(story_snippets, figures, storage).execute(
        UpdateStoryCommand(story_id=created.id, figure_id=figure.id, title="Chapter 1 Revised")  # type: ignore[arg-type]
    )
    assert updated.title == "Chapter 1 Revised"

    await DeleteStory(story_snippets, storage).execute(created.id)
    assert await story_snippets.get_by_id(created.id) is None


async def test_list_stories() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    storage = FakeFileStorage()
    figure = await _seed_figure(figures)
    await CreateStory(story_snippets, figures, storage).execute(
        CreateStoryCommand(figure_id=figure.id, title="A")  # type: ignore[arg-type]
    )
    await CreateStory(story_snippets, figures, storage).execute(
        CreateStoryCommand(figure_id=figure.id, title="B")  # type: ignore[arg-type]
    )

    result = await ListStories(story_snippets, figures).execute(
        ListStoriesQuery(figure_id=figure.id, page=1, per_page=15)
    )
    assert result.total == 2
    assert all(item.figure_name == "Marie Curie" for item in result.items)
