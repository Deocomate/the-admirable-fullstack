import pytest

from admirable.domain.entities.story_snippet import StorySnippet
from admirable.domain.exceptions import InvalidAudioTransitionError
from admirable.domain.value_objects.audio_status import AudioStatus


def make_snippet(**overrides: object) -> StorySnippet:
    defaults: dict[str, object] = dict(
        id=1,
        figure_id=1,
        title="Growing up in Warsaw",
        subtitle=None,
        content_blocks=[],
        search_text="",
    )
    defaults.update(overrides)
    return StorySnippet(**defaults)  # type: ignore[arg-type]


def test_request_audio_generation_from_idle() -> None:
    snippet = make_snippet()
    snippet.request_audio_generation()
    assert snippet.audio_status == AudioStatus.PROCESSING


def test_request_audio_generation_while_processing_raises() -> None:
    snippet = make_snippet(audio_status=AudioStatus.PROCESSING)
    with pytest.raises(InvalidAudioTransitionError):
        snippet.request_audio_generation()


def test_mark_audio_completed() -> None:
    snippet = make_snippet(audio_status=AudioStatus.PROCESSING)
    snippet.mark_audio_completed("uploads/stories/audio/x.mp3")
    assert snippet.audio_status == AudioStatus.COMPLETED
    assert snippet.audio_path == "uploads/stories/audio/x.mp3"


def test_mark_audio_failed() -> None:
    snippet = make_snippet(audio_status=AudioStatus.PROCESSING)
    snippet.mark_audio_failed("synthesis error")
    assert snippet.audio_status == AudioStatus.FAILED
    assert snippet.audio_error == "synthesis error"


def test_cancel_audio() -> None:
    snippet = make_snippet(audio_status=AudioStatus.PROCESSING)
    snippet.cancel_audio()
    assert snippet.audio_status == AudioStatus.CANCELLED


def test_attach_audio_upload() -> None:
    snippet = make_snippet(audio_status=AudioStatus.IDLE)
    snippet.attach_audio_upload("uploads/stories/audio/manual.mp3")
    assert snippet.audio_status == AudioStatus.COMPLETED


def test_rebuild_search_text() -> None:
    from admirable.domain.value_objects.content_block import parse_content_blocks

    raw_blocks: list[dict[str, object]] = [{"type": "heading", "text_en": "Title"}]
    snippet = make_snippet(content_blocks=parse_content_blocks(raw_blocks))
    snippet.rebuild_search_text()
    assert snippet.search_text == "Title"
