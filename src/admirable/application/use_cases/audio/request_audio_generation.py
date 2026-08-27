from admirable.application.dto.audio_dto import AudioActionCommand
from admirable.application.ports.task_queue_port import TaskQueuePort
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository

from ._lookup import load_entity, save_entity


class RequestAudioGeneration:
    """No Azure-key check here — edge-tts needs no API key at all."""

    def __init__(
        self,
        figures: FigureRepository,
        story_snippets: StorySnippetRepository,
        queue: TaskQueuePort,
    ) -> None:
        self._figures = figures
        self._story_snippets = story_snippets
        self._queue = queue

    async def execute(self, cmd: AudioActionCommand) -> None:
        entity = await load_entity(cmd.kind, cmd.entity_id, self._figures, self._story_snippets)
        # Raises InvalidAudioTransitionError if generation is already processing.
        entity.request_audio_generation()
        await save_entity(cmd.kind, entity, self._figures, self._story_snippets)
        await self._queue.enqueue_audio_generation(cmd.kind, cmd.entity_id)
