from admirable.application.ports.file_storage_port import FileStoragePort
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository


class DeleteFigure:
    def __init__(
        self,
        figures: FigureRepository,
        story_snippets: StorySnippetRepository,
        storage: FileStoragePort,
    ) -> None:
        self._figures = figures
        self._story_snippets = story_snippets
        self._storage = storage

    async def execute(self, figure_id: int) -> None:
        figure = await self._figures.get_by_id(figure_id)
        if figure is None:
            raise EntityNotFoundError("Figure", figure_id)

        await self._storage.delete(figure.avatar_path)
        await self._storage.delete(figure.audio_path)

        page = await self._story_snippets.list_paginated(
            figure_id=figure_id, search=None, page=1, per_page=1_000_000
        )
        for snippet in page.items:
            await self._storage.delete(snippet.image_path)
            await self._storage.delete(snippet.audio_path)

        # DB cascade (ON DELETE CASCADE) removes story_snippets, category_figure,
        # and featured_figures rows for us.
        await self._figures.delete(figure_id)
