from admirable.application.dto.story_dto import CreateStoryCommand, StoryDetailDTO
from admirable.application.ports.file_storage_port import FileStoragePort
from admirable.application.use_cases.figures._mapping import to_domain_blocks
from admirable.domain.entities.story_snippet import StorySnippet
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository
from admirable.domain.value_objects.content_block import build_search_text

from ._mapping import to_story_detail_dto


class CreateStory:
    def __init__(
        self,
        story_snippets: StorySnippetRepository,
        figures: FigureRepository,
        storage: FileStoragePort,
    ) -> None:
        self._story_snippets = story_snippets
        self._figures = figures
        self._storage = storage

    async def execute(self, cmd: CreateStoryCommand) -> StoryDetailDTO:
        figure = await self._figures.get_by_id(cmd.figure_id)
        if figure is None:
            raise EntityNotFoundError("Figure", cmd.figure_id)

        blocks = to_domain_blocks(cmd.content_blocks)
        snippet = StorySnippet(
            id=None,
            figure_id=cmd.figure_id,
            title=cmd.title,
            subtitle=cmd.subtitle,
            content_blocks=blocks,
            search_text=build_search_text(blocks),
            youtube_url=cmd.youtube_url,
        )

        if cmd.image is not None:
            snippet.image_path = await self._storage.save(cmd.image, "uploads/stories/images", "")
        if cmd.audio is not None:
            path = await self._storage.save(cmd.audio, "uploads/stories/audio", "")
            snippet.attach_audio_upload(path)

        created = await self._story_snippets.add(snippet)
        return to_story_detail_dto(created, figure_name=figure.name)
