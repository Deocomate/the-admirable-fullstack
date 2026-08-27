import pytest

from admirable.application.dto.audio_dto import AudioActionCommand
from admirable.application.use_cases.audio.cancel_audio_generation import CancelAudioGeneration
from admirable.application.use_cases.audio.get_audio_status import GetAudioStatus
from admirable.application.use_cases.audio.request_audio_generation import RequestAudioGeneration
from admirable.domain.entities.figure import Figure
from admirable.domain.exceptions import InvalidAudioTransitionError
from admirable.domain.value_objects.audio_status import AudioStatus
from tests.fakes.fake_figure_repository import FakeFigureRepository
from tests.fakes.fake_story_snippet_repository import FakeStorySnippetRepository
from tests.fakes.fake_task_queue import FakeTaskQueue


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


async def test_request_audio_generation_enqueues() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    queue = FakeTaskQueue()
    figure = await _seed_figure(figures)

    await RequestAudioGeneration(figures, story_snippets, queue).execute(
        AudioActionCommand(kind="figure", entity_id=figure.id)  # type: ignore[arg-type]
    )

    updated = await figures.get_by_id(figure.id)  # type: ignore[arg-type]
    assert updated is not None
    assert updated.audio_status == AudioStatus.PROCESSING
    assert queue.enqueued == [("figure", figure.id)]


async def test_request_audio_generation_rejects_when_already_processing() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    queue = FakeTaskQueue()
    figure = await _seed_figure(figures)
    figure.request_audio_generation()
    await figures.update(figure)

    with pytest.raises(InvalidAudioTransitionError):
        await RequestAudioGeneration(figures, story_snippets, queue).execute(
            AudioActionCommand(kind="figure", entity_id=figure.id)  # type: ignore[arg-type]
        )


async def test_cancel_audio_generation() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    figure = await _seed_figure(figures)
    figure.request_audio_generation()
    await figures.update(figure)

    await CancelAudioGeneration(figures, story_snippets).execute(
        AudioActionCommand(kind="figure", entity_id=figure.id)  # type: ignore[arg-type]
    )

    updated = await figures.get_by_id(figure.id)  # type: ignore[arg-type]
    assert updated is not None
    assert updated.audio_status == AudioStatus.CANCELLED


async def test_cancel_audio_generation_rejects_when_idle() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    figure = await _seed_figure(figures)

    with pytest.raises(InvalidAudioTransitionError):
        await CancelAudioGeneration(figures, story_snippets).execute(
            AudioActionCommand(kind="figure", entity_id=figure.id)  # type: ignore[arg-type]
        )


async def test_get_audio_status_builds_url() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    figure = await _seed_figure(figures)
    figure.attach_audio_upload("uploads/audio/marie.mp3")
    await figures.update(figure)

    status = await GetAudioStatus(figures, story_snippets, "/media/").execute(
        AudioActionCommand(kind="figure", entity_id=figure.id)  # type: ignore[arg-type]
    )

    assert status.status == AudioStatus.COMPLETED
    assert status.audio_url == "/media/uploads/audio/marie.mp3"
