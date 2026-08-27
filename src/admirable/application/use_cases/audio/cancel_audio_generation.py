from admirable.application.dto.audio_dto import AudioActionCommand
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository

from ._lookup import load_entity, save_entity


class CancelAudioGeneration:
    def __init__(self, figures: FigureRepository, story_snippets: StorySnippetRepository) -> None:
        self._figures = figures
        self._story_snippets = story_snippets

    async def execute(self, cmd: AudioActionCommand) -> None:
        entity = await load_entity(cmd.kind, cmd.entity_id, self._figures, self._story_snippets)
        entity.cancel_audio()  # raises InvalidAudioTransitionError unless currently processing
        await save_entity(cmd.kind, entity, self._figures, self._story_snippets)
