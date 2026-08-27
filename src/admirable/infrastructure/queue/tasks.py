"""Taskiq task definitions. The task itself stays exception-safe — GenerateAudio
already handles its own failure path (marks audio_status=failed), so a bug
here must not crash the worker process."""

import logging

from admirable.application.use_cases.audio.generate_audio import GenerateAudio
from admirable.config import get_settings
from admirable.infrastructure.container import build_worker_scope
from admirable.infrastructure.queue.broker import broker

logger = logging.getLogger("admirable.worker")


@broker.task(task_name="generate_audio")
async def generate_audio_task(kind: str, entity_id: int) -> None:
    from admirable.application.dto.audio_dto import AudioActionCommand

    settings = get_settings()
    try:
        async with build_worker_scope(settings) as container:
            use_case = GenerateAudio(
                container.figures, container.story_snippets, container.tts,
                container.storage, container.clock,
            )
            await use_case.execute(AudioActionCommand(kind=kind, entity_id=entity_id))  # type: ignore[arg-type]
    except Exception:
        logger.exception("generate_audio task failed for kind=%s entity_id=%s", kind, entity_id)
