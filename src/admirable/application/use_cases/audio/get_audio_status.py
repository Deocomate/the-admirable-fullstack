from admirable.application.dto.audio_dto import AudioActionCommand, AudioStatusDTO
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository

from ._lookup import load_entity


class GetAudioStatus:
    def __init__(
        self,
        figures: FigureRepository,
        story_snippets: StorySnippetRepository,
        media_url_prefix: str,
    ) -> None:
        self._figures = figures
        self._story_snippets = story_snippets
        self._media_url_prefix = media_url_prefix

    async def execute(self, cmd: AudioActionCommand) -> AudioStatusDTO:
        entity = await load_entity(cmd.kind, cmd.entity_id, self._figures, self._story_snippets)
        audio_url = f"{self._media_url_prefix}{entity.audio_path}" if entity.audio_path else None
        return AudioStatusDTO(
            status=entity.audio_status, error=entity.audio_error, audio_url=audio_url
        )
