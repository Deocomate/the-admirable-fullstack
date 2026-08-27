from datetime import UTC, datetime

from admirable.application.dto.audio_dto import AudioActionCommand
from admirable.application.use_cases.audio.generate_audio import GenerateAudio
from admirable.domain.entities.figure import Figure
from admirable.domain.value_objects.audio_status import AudioStatus
from admirable.domain.value_objects.content_block import parse_content_blocks
from tests.fakes.fake_clock import FakeClock
from tests.fakes.fake_figure_repository import FakeFigureRepository
from tests.fakes.fake_file_storage import FakeFileStorage
from tests.fakes.fake_story_snippet_repository import FakeStorySnippetRepository
from tests.fakes.fake_text_to_speech import FakeTextToSpeech


async def _seed_processing_figure(figures: FakeFigureRepository) -> Figure:
    blocks = parse_content_blocks([{"type": "heading", "text_en": "Hello"}])
    figure = Figure(
        id=None, name="Marie Curie", slug="marie-curie", short_description=None,
        key_facts=[], content_blocks=blocks, search_text="Hello",
    )
    created = await figures.add(figure)
    created.request_audio_generation()
    await figures.update(created)
    return created


async def test_generate_audio_happy_path() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    figure = await _seed_processing_figure(figures)

    tts = FakeTextToSpeech()
    storage = FakeFileStorage()
    clock = FakeClock(datetime(2026, 1, 1, tzinfo=UTC))

    await GenerateAudio(figures, story_snippets, tts, storage, clock).execute(
        AudioActionCommand(kind="figure", entity_id=figure.id)  # type: ignore[arg-type]
    )

    updated = await figures.get_by_id(figure.id)  # type: ignore[arg-type]
    assert updated is not None
    assert updated.audio_status == AudioStatus.COMPLETED
    assert updated.audio_path is not None
    assert updated.audio_error is None


async def test_generate_audio_not_processing_is_noop() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    blocks = parse_content_blocks([{"type": "heading", "text_en": "Hello"}])
    figure = await figures.add(
        Figure(
            id=None, name="Idle Figure", slug="idle-figure", short_description=None,
            key_facts=[], content_blocks=blocks, search_text="Hello",
        )
    )
    tts = FakeTextToSpeech()

    await GenerateAudio(
        figures, story_snippets, tts, FakeFileStorage(), FakeClock(datetime.now(UTC))
    ).execute(AudioActionCommand(kind="figure", entity_id=figure.id))  # type: ignore[arg-type]

    assert tts.calls == []


async def test_generate_audio_tts_failure_marks_failed() -> None:
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    figure = await _seed_processing_figure(figures)
    tts = FakeTextToSpeech(raises=RuntimeError("synthesis exploded"))

    await GenerateAudio(
        figures, story_snippets, tts, FakeFileStorage(), FakeClock(datetime.now(UTC))
    ).execute(AudioActionCommand(kind="figure", entity_id=figure.id))  # type: ignore[arg-type]

    updated = await figures.get_by_id(figure.id)  # type: ignore[arg-type]
    assert updated is not None
    assert updated.audio_status == AudioStatus.FAILED
    assert updated.audio_error == "synthesis exploded"


async def test_generate_audio_cancelled_after_tts_before_write_is_noop() -> None:
    """Cancel lands between the TTS call returning and the file being written.
    The synthesized audio is simply discarded — nothing is stored."""
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    figure = await _seed_processing_figure(figures)

    class CancellingTts:
        async def synthesize(self, text: str) -> bytes:
            live = await figures.get_by_id(figure.id)  # type: ignore[arg-type]
            assert live is not None
            live.cancel_audio()
            await figures.update(live)
            return b"audio-bytes"

    storage = FakeFileStorage()
    await GenerateAudio(
        figures, story_snippets, CancellingTts(), storage, FakeClock(datetime.now(UTC))
    ).execute(AudioActionCommand(kind="figure", entity_id=figure.id))  # type: ignore[arg-type]

    updated = await figures.get_by_id(figure.id)  # type: ignore[arg-type]
    assert updated is not None
    assert updated.audio_status == AudioStatus.CANCELLED
    assert updated.audio_path is None
    assert storage.saved == []


async def test_generate_audio_cancelled_after_write_before_db_update_deletes_file() -> None:
    """Required by Phase 5 success criteria: cancel after the file is written
    but before the DB is updated -> the just-written temp file is deleted and
    audio_path is left untouched."""
    figures = FakeFigureRepository()
    story_snippets = FakeStorySnippetRepository()
    figure = await _seed_processing_figure(figures)
    original_audio_path = figure.audio_path

    storage = FakeFileStorage()
    real_save = storage.save

    async def save_then_cancel(file: object, directory: str, slug: str) -> str:
        path = await real_save(file, directory, slug)  # type: ignore[arg-type]
        live = await figures.get_by_id(figure.id)  # type: ignore[arg-type]
        assert live is not None
        live.cancel_audio()
        await figures.update(live)
        return path

    storage.save = save_then_cancel  # type: ignore[method-assign]

    await GenerateAudio(
        figures, story_snippets, FakeTextToSpeech(), storage, FakeClock(datetime.now(UTC))
    ).execute(AudioActionCommand(kind="figure", entity_id=figure.id))  # type: ignore[arg-type]

    updated = await figures.get_by_id(figure.id)  # type: ignore[arg-type]
    assert updated is not None
    assert updated.audio_status == AudioStatus.CANCELLED
    assert updated.audio_path == original_audio_path  # untouched
    assert len(storage.saved) == 1
    written_path = storage.saved[0][0]
    assert written_path in storage.deleted  # the temp file was cleaned up
