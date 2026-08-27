from admirable.application.ports.file_storage_port import FileStoragePort
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository


class DeleteStory:
    def __init__(self, story_snippets: StorySnippetRepository, storage: FileStoragePort) -> None:
        self._story_snippets = story_snippets
        self._storage = storage

    async def execute(self, story_id: int) -> None:
        snippet = await self._story_snippets.get_by_id(story_id)
        if snippet is None:
            raise EntityNotFoundError("StorySnippet", story_id)

        await self._storage.delete(snippet.image_path)
        await self._storage.delete(snippet.audio_path)
        await self._story_snippets.delete(story_id)
