from pydantic import BaseModel

from admirable.application.dto.category_dto import CategoryDTO
from admirable.domain.repositories.category_repository import CategoryRepository


class ListCategoriesQuery(BaseModel):
    page: int = 1
    per_page: int = 15


class ListCategoriesResult(BaseModel):
    items: list[CategoryDTO]
    total: int
    page: int
    per_page: int


class ListCategories:
    def __init__(self, categories: CategoryRepository) -> None:
        self._categories = categories

    async def execute(self, query: ListCategoriesQuery) -> ListCategoriesResult:
        page = await self._categories.list_paginated(query.page, query.per_page)
        items = []
        for category in page.items:
            count = await self._categories.count_figures(category.id)  # type: ignore[arg-type]
            items.append(
                CategoryDTO(
                    id=category.id,  # type: ignore[arg-type]
                    name=category.name,
                    slug=category.slug,
                    figures_count=count,
                )
            )
        return ListCategoriesResult(
            items=items, total=page.total, page=page.page, per_page=page.per_page
        )
