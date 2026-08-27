from typing import Literal, Protocol

AudioKind = Literal["figure", "story"]


class TaskQueuePort(Protocol):
    async def enqueue_audio_generation(self, kind: AudioKind, entity_id: int) -> None: ...
