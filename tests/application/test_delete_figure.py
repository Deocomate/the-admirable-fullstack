from admirable.application.dto.figure_dto import CreateFigureCommand
from admirable.application.dto.story_dto import CreateStoryCommand
from admirable.application.use_cases.figures.create_figure import CreateFigure
from admirable.application.use_cases.figures.delete_figure import DeleteFigure
from admirable.application.use_cases.stories.create_story import CreateStory
from tests.fakes.fake_figure_repository import FakeFigureRepository
from tests.fakes.fake_file_storage import FakeFileStorage
from tests.fakes.fake_story_snippet_repository import FakeStorySnippetRepository


async def test_delete_figure_deletes_avatar_audio_and_snippet_files() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    storage = FakeFileStorage()

    created = await CreateFigure(figures, storage).execute(CreateFigureCommand(name="Marie Curie"))
    figure = await figures.get_by_id(created.id)
    assert figure is not None
    figure.avatar_path = "uploads/avatars/marie.jpg"
    figure.audio_path = "uploads/audio/marie.mp3"
    await figures.update(figure)

    snippet = await CreateStory(story_snippets, figures, storage).execute(
        CreateStoryCommand(figure_id=created.id, title="Chapter 1")
    )
    stored_snippet = await story_snippets.get_by_id(snippet.id)
    assert stored_snippet is not None
    stored_snippet.image_path = "uploads/stories/images/ch1.jpg"
    stored_snippet.audio_path = "uploads/stories/audio/ch1.mp3"
    await story_snippets.update(stored_snippet)

    await DeleteFigure(figures, story_snippets, storage).execute(created.id)

    assert set(storage.deleted) == {
        "uploads/avatars/marie.jpg",
        "uploads/audio/marie.mp3",
        "uploads/stories/images/ch1.jpg",
        "uploads/stories/audio/ch1.mp3",
    }
    assert await figures.get_by_id(created.id) is None
