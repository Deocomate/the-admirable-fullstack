import pytest

from admirable.domain.entities.figure import Figure
from admirable.domain.exceptions import InvalidAudioTransitionError
from admirable.domain.value_objects.audio_status import AudioStatus


def make_figure(**overrides: object) -> Figure:
    defaults: dict[str, object] = dict(
        id=1,
        name="Marie Curie",
        slug="marie-curie",
        short_description=None,
        key_facts=[],
        content_blocks=[],
        search_text="",
    )
    defaults.update(overrides)
    return Figure(**defaults)  # type: ignore[arg-type]


def test_request_audio_generation_from_idle() -> None:
    figure = make_figure()
    figure.request_audio_generation()
    assert figure.audio_status == AudioStatus.PROCESSING
    assert figure.audio_error is None


def test_request_audio_generation_while_processing_raises() -> None:
    figure = make_figure(audio_status=AudioStatus.PROCESSING)
    with pytest.raises(InvalidAudioTransitionError):
        figure.request_audio_generation()


def test_mark_audio_completed() -> None:
    figure = make_figure(audio_status=AudioStatus.PROCESSING)
    figure.mark_audio_completed("uploads/audio/marie-curie_123.mp3")
    assert figure.audio_status == AudioStatus.COMPLETED
    assert figure.audio_path == "uploads/audio/marie-curie_123.mp3"


def test_mark_audio_failed_truncates_message() -> None:
    figure = make_figure(audio_status=AudioStatus.PROCESSING)
    figure.mark_audio_failed("x" * 600)
    assert figure.audio_status == AudioStatus.FAILED
    assert figure.audio_error is not None
    assert len(figure.audio_error) == 500


def test_cancel_audio_requires_processing() -> None:
    figure = make_figure(audio_status=AudioStatus.IDLE)
    with pytest.raises(InvalidAudioTransitionError):
        figure.cancel_audio()


def test_cancel_audio() -> None:
    figure = make_figure(audio_status=AudioStatus.PROCESSING)
    figure.cancel_audio()
    assert figure.audio_status == AudioStatus.CANCELLED


def test_attach_audio_upload_forces_completed_from_any_state() -> None:
    figure = make_figure(audio_status=AudioStatus.FAILED, audio_error="boom")
    figure.attach_audio_upload("uploads/audio/manual.mp3")
    assert figure.audio_status == AudioStatus.COMPLETED
    assert figure.audio_path == "uploads/audio/manual.mp3"
    assert figure.audio_error is None
