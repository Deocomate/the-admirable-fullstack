from pydantic import BaseModel

from admirable.application.dto.category_dto import CategoryDTO
from admirable.application.dto.public_dto import SearchResultsDTO
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository

from ._figure_summary import category_name_map, to_summary

_TRENDING_LIMIT = 4


class SearchFiguresQuery(BaseModel):
    query: str = ""
    category_slug: str | None = None
    page: int = 1
    per_page: int = 12


class SearchFigures:
    def __init__(
        self,
        figures: FigureRepository,
        categories: CategoryRepository,
        story_snippets: StorySnippetRepository,
    ) -> None:
        self._figures = figures
        self._categories = categories
        self._story_snippets = story_snippets

    async def execute(self, query: SearchFiguresQuery) -> SearchResultsDTO:
        names = await category_name_map(self._categories)
        result_page = await self._figures.search(
            query.query, query.category_slug, query.page, query.per_page
        )
        figures = [await to_summary(f, names, self._story_snippets) for f in result_page.items]

        trending = await self._figures.list_trending(_TRENDING_LIMIT)
        trending_dtos = [await to_summary(f, names, self._story_snippets) for f in trending]

        categories = [
            CategoryDTO(id=c.id, name=c.name, slug=c.slug)  # type: ignore[arg-type]
            for c in await self._categories.list_all()
        ]

        return SearchResultsDTO(
            query=query.query,
            category_slug=query.category_slug,
            categories=categories,
            figures=figures,
            total=result_page.total,
            page=result_page.page,
            per_page=result_page.per_page,
            trending_figures=trending_dtos,
        )
