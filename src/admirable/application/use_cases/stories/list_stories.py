from pydantic import BaseModel

from admirable.application.dto.story_dto import StorySummaryDTO
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository


class ListStoriesQuery(BaseModel):
    figure_id: int | None = None
    search: str | None = None
    page: int = 1
    per_page: int = 15


class ListStoriesResult(BaseModel):
    items: list[StorySummaryDTO]
    total: int
    page: int
    per_page: int


class ListStories:
    def __init__(self, story_snippets: StorySnippetRepository, figures: FigureRepository) -> None:
        self._story_snippets = story_snippets
        self._figures = figures

    async def execute(self, query: ListStoriesQuery) -> ListStoriesResult:
        page = await self._story_snippets.list_paginated(
            query.figure_id, query.search, query.page, query.per_page
        )
        figure_names: dict[int, str] = {}
        items = []
        for snippet in page.items:
            if snippet.figure_id not in figure_names:
                figure = await self._figures.get_by_id(snippet.figure_id)
                figure_names[snippet.figure_id] = figure.name if figure else ""
            items.append(
                StorySummaryDTO(
                    id=snippet.id,  # type: ignore[arg-type]
                    figure_id=snippet.figure_id,
                    figure_name=figure_names[snippet.figure_id],
                    title=snippet.title,
                    subtitle=snippet.subtitle,
                )
            )
        return ListStoriesResult(
            items=items, total=page.total, page=page.page, per_page=page.per_page
        )
