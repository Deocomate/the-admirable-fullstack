from collections.abc import AsyncIterator

from admirable.application.dto.figure_dto import CreateFigureCommand, UpdateFigureCommand
from admirable.application.dto.files import UploadedFileDTO
from admirable.application.dto.story_dto import CreateStoryCommand, UpdateStoryCommand
from admirable.application.use_cases.figures.create_figure import CreateFigure
from admirable.application.use_cases.figures.update_figure import UpdateFigure
from admirable.application.use_cases.stories.create_story import CreateStory
from admirable.application.use_cases.stories.update_story import UpdateStory
from tests.fakes.fake_figure_repository import FakeFigureRepository
from tests.fakes.fake_file_storage import FakeFileStorage
from tests.fakes.fake_story_snippet_repository import FakeStorySnippetRepository


async def _empty_upload(filename: str) -> UploadedFileDTO:
    async def _stream() -> AsyncIterator[bytes]:
        yield b""

    return UploadedFileDTO(filename=filename, content_type="image/jpeg", stream=_stream())


async def test_update_figure_replaces_avatar_and_audio_deleting_old_files() -> None:
    figures = FakeFigureRepository()
    storage = FakeFileStorage()
    created = await CreateFigure(figures, storage).execute(
        CreateFigureCommand(name="Marie Curie", avatar=await _empty_upload("old.jpg"))
    )
    figure = await figures.get_by_id(created.id)
    assert figure is not None
    old_avatar_path = figure.avatar_path

    result = await UpdateFigure(figures, storage).execute(
        UpdateFigureCommand(
            figure_id=created.id, name="Marie Curie", avatar=await _empty_upload("new.jpg")
        )
    )

    assert old_avatar_path in storage.deleted
    assert result.avatar_path != old_avatar_path


async def test_update_story_replaces_image_and_audio() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    storage = FakeFileStorage()

    figure = await CreateFigure(figures, storage).execute(CreateFigureCommand(name="Marie Curie"))
    created = await CreateStory(story_snippets, figures, storage).execute(
        CreateStoryCommand(
            figure_id=figure.id, title="Ch1", image=await _empty_upload("old.jpg")
        )
    )
    stored = await story_snippets.get_by_id(created.id)
    assert stored is not None
    old_image_path = stored.image_path

    updated = await UpdateStory(story_snippets, figures, storage).execute(
        UpdateStoryCommand(
            story_id=created.id, figure_id=figure.id, title="Ch1",
            image=await _empty_upload("new.jpg"),
        )
    )

    assert old_image_path in storage.deleted
    assert updated.image_path != old_image_path
