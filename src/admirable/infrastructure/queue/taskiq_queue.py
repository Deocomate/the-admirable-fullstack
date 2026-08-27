"""Implements TaskQueuePort. Only passes identifiers (kind, entity_id) to the
task — mirrors GenerateAudioJob, which held only `type` and `id`, never the
model itself, avoiding serialization and stale-data pitfalls."""

from admirable.application.ports.task_queue_port import AudioKind


class TaskiqQueue:
    async def enqueue_audio_generation(self, kind: AudioKind, entity_id: int) -> None:
        from admirable.infrastructure.queue.tasks import generate_audio_task

        await generate_audio_task.kiq(kind, entity_id)
