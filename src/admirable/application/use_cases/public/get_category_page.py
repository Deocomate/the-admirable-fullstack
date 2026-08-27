from admirable.application.dto.category_dto import CategoryDTO
from admirable.application.dto.public_dto import CategoryPageDTO
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository

from ._figure_summary import category_name_map, to_summary

_PER_PAGE = 12


class GetCategoryPage:
    def __init__(
        self,
        figures: FigureRepository,
        categories: CategoryRepository,
        story_snippets: StorySnippetRepository,
    ) -> None:
        self._figures = figures
        self._categories = categories
        self._story_snippets = story_snippets

    async def execute(self, slug: str | None, page: int = 1) -> CategoryPageDTO:
        names = await category_name_map(self._categories)
        all_categories = [
            CategoryDTO(id=c.id, name=c.name, slug=c.slug)  # type: ignore[arg-type]
            for c in await self._categories.list_all()
        ]

        category_dto = None
        category_id = None
        if slug is not None:
            category = None
            for c in await self._categories.list_all():
                if c.slug == slug:
                    category = c
                    break
            if category is None:
                raise EntityNotFoundError("Category", slug)
            category_id = category.id
            category_dto = CategoryDTO(id=category.id, name=category.name, slug=category.slug)  # type: ignore[arg-type]

        top_featured = await self._figures.get_top_featured(category_id)
        featured_dto = (
            await to_summary(top_featured, names, self._story_snippets, is_featured=True)
            if top_featured
            else None
        )

        result_page = await self._figures.list_paginated(None, category_id, page, _PER_PAGE)
        figures = [await to_summary(f, names, self._story_snippets) for f in result_page.items]

        return CategoryPageDTO(
            categories=all_categories,
            category=category_dto,
            featured_figure=featured_dto,
            figures=figures,
            total=result_page.total,
            page=result_page.page,
            per_page=result_page.per_page,
        )
