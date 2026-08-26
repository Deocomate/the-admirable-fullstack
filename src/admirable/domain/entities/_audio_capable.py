"""Shared audio-generation state machine for `Figure` and `StorySnippet`.

Plain mixin (not a dataclass) so it contributes no dataclass fields — the
concrete entities declare `audio_path` / `audio_status` / `audio_error`
themselves and inherit these methods for the shared state machine.
"""

from admirable.domain.exceptions import InvalidAudioTransitionError
from admirable.domain.value_objects.audio_status import AudioStatus, can_transition

_ERROR_MESSAGE_LIMIT = 500


class AudioCapable:
    audio_path: str | None
    audio_status: AudioStatus
    audio_error: str | None

    def request_audio_generation(self) -> None:
        self._transition(AudioStatus.PROCESSING)
        self.audio_error = None

    def mark_audio_completed(self, path: str) -> None:
        self._transition(AudioStatus.COMPLETED)
        self.audio_path = path
        self.audio_error = None

    def mark_audio_failed(self, message: str) -> None:
        self._transition(AudioStatus.FAILED)
        self.audio_error = message[:_ERROR_MESSAGE_LIMIT]

    def cancel_audio(self) -> None:
        self._transition(AudioStatus.CANCELLED)
        self.audio_error = None

    def attach_audio_upload(self, path: str) -> None:
        """Manual admin upload: set straight to `completed` regardless of current state."""
        self.audio_path = path
        self.audio_status = AudioStatus.COMPLETED
        self.audio_error = None

    def _transition(self, dst: AudioStatus) -> None:
        if not can_transition(self.audio_status, dst):
            raise InvalidAudioTransitionError(self.audio_status, dst)
        self.audio_status = dst
