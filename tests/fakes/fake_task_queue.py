from admirable.application.ports.task_queue_port import AudioKind


class FakeTaskQueue:
    def __init__(self) -> None:
        self.enqueued: list[tuple[AudioKind, int]] = []

    async def enqueue_audio_generation(self, kind: AudioKind, entity_id: int) -> None:
        self.enqueued.append((kind, entity_id))
