from pydantic import BaseModel

from admirable.application.dto.figure_dto import FigureSummaryDTO
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository


class ListFiguresQuery(BaseModel):
    search: str | None = None
    category_id: int | None = None
    page: int = 1
    per_page: int = 15


class ListFiguresResult(BaseModel):
    items: list[FigureSummaryDTO]
    total: int
    page: int
    per_page: int


class ListFigures:
    def __init__(
        self,
        figures: FigureRepository,
        categories: CategoryRepository,
        story_snippets: StorySnippetRepository,
    ) -> None:
        self._figures = figures
        self._categories = categories
        self._story_snippets = story_snippets

    async def execute(self, query: ListFiguresQuery) -> ListFiguresResult:
        page = await self._figures.list_paginated(
            query.search, query.category_id, query.page, query.per_page
        )
        all_categories = {c.id: c.name for c in await self._categories.list_all()}

        items = []
        for figure in page.items:
            names = [all_categories[cid] for cid in figure.category_ids if cid in all_categories]
            count = await self._story_snippets.count_by_figure(figure.id)  # type: ignore[arg-type]
            items.append(
                FigureSummaryDTO(
                    id=figure.id,  # type: ignore[arg-type]
                    name=figure.name,
                    slug=figure.slug,
                    avatar_path=figure.avatar_path,
                    short_description=figure.short_description,
                    category_names=names,
                    story_snippets_count=count,
                )
            )
        return ListFiguresResult(
            items=items, total=page.total, page=page.page, per_page=page.per_page
        )
