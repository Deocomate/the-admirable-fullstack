import pytest

from admirable.domain.value_objects.audio_status import AudioStatus, can_transition

VALID = [
    (AudioStatus.IDLE, AudioStatus.PROCESSING),
    (AudioStatus.PROCESSING, AudioStatus.COMPLETED),
    (AudioStatus.PROCESSING, AudioStatus.FAILED),
    (AudioStatus.PROCESSING, AudioStatus.CANCELLED),
    (AudioStatus.COMPLETED, AudioStatus.PROCESSING),
    (AudioStatus.FAILED, AudioStatus.PROCESSING),
    (AudioStatus.CANCELLED, AudioStatus.PROCESSING),
]

INVALID = [
    (AudioStatus.IDLE, AudioStatus.COMPLETED),
    (AudioStatus.IDLE, AudioStatus.FAILED),
    (AudioStatus.IDLE, AudioStatus.CANCELLED),
    (AudioStatus.PROCESSING, AudioStatus.IDLE),
    (AudioStatus.COMPLETED, AudioStatus.COMPLETED),
    (AudioStatus.COMPLETED, AudioStatus.FAILED),
    (AudioStatus.COMPLETED, AudioStatus.CANCELLED),
    (AudioStatus.COMPLETED, AudioStatus.IDLE),
    (AudioStatus.FAILED, AudioStatus.COMPLETED),
    (AudioStatus.FAILED, AudioStatus.CANCELLED),
    (AudioStatus.FAILED, AudioStatus.IDLE),
    (AudioStatus.CANCELLED, AudioStatus.COMPLETED),
    (AudioStatus.CANCELLED, AudioStatus.FAILED),
    (AudioStatus.CANCELLED, AudioStatus.IDLE),
]


@pytest.mark.parametrize(("src", "dst"), VALID)
def test_valid_transitions(src: AudioStatus, dst: AudioStatus) -> None:
    assert can_transition(src, dst) is True


@pytest.mark.parametrize(("src", "dst"), INVALID)
def test_invalid_transitions(src: AudioStatus, dst: AudioStatus) -> None:
    assert can_transition(src, dst) is False
