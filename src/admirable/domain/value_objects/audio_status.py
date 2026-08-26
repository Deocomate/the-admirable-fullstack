from enum import StrEnum


class AudioStatus(StrEnum):
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


_VALID_TRANSITIONS: dict[AudioStatus, frozenset[AudioStatus]] = {
    AudioStatus.IDLE: frozenset({AudioStatus.PROCESSING}),
    AudioStatus.PROCESSING: frozenset(
        {AudioStatus.COMPLETED, AudioStatus.FAILED, AudioStatus.CANCELLED}
    ),
    AudioStatus.COMPLETED: frozenset({AudioStatus.PROCESSING}),
    AudioStatus.FAILED: frozenset({AudioStatus.PROCESSING}),
    AudioStatus.CANCELLED: frozenset({AudioStatus.PROCESSING}),
}


def can_transition(src: AudioStatus, dst: AudioStatus) -> bool:
    return dst in _VALID_TRANSITIONS[src]
