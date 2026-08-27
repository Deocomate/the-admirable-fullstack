from admirable.application.dto.story_dto import StoryDetailDTO, UpdateStoryCommand
from admirable.application.ports.file_storage_port import FileStoragePort
from admirable.application.use_cases.figures._mapping import to_domain_blocks
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository
from admirable.domain.value_objects.content_block import build_search_text

from ._mapping import to_story_detail_dto


class UpdateStory:
    def __init__(
        self,
        story_snippets: StorySnippetRepository,
        figures: FigureRepository,
        storage: FileStoragePort,
    ) -> None:
        self._story_snippets = story_snippets
        self._figures = figures
        self._storage = storage

    async def execute(self, cmd: UpdateStoryCommand) -> StoryDetailDTO:
        snippet = await self._story_snippets.get_by_id(cmd.story_id)
        if snippet is None:
            raise EntityNotFoundError("StorySnippet", cmd.story_id)
        figure = await self._figures.get_by_id(cmd.figure_id)
        if figure is None:
            raise EntityNotFoundError("Figure", cmd.figure_id)

        snippet.figure_id = cmd.figure_id
        snippet.title = cmd.title
        snippet.subtitle = cmd.subtitle
        snippet.content_blocks = to_domain_blocks(cmd.content_blocks)
        snippet.search_text = build_search_text(snippet.content_blocks)
        snippet.youtube_url = cmd.youtube_url

        if cmd.image is not None:
            await self._storage.delete(snippet.image_path)
            snippet.image_path = await self._storage.save(cmd.image, "uploads/stories/images", "")
        if cmd.audio is not None:
            await self._storage.delete(snippet.audio_path)
            path = await self._storage.save(cmd.audio, "uploads/stories/audio", "")
            snippet.attach_audio_upload(path)

        updated = await self._story_snippets.update(snippet)
        return to_story_detail_dto(updated, figure_name=figure.name)
