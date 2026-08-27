from admirable.application.dto.category_dto import CategoryDTO
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.category_repository import CategoryRepository


class GetCategory:
    def __init__(self, categories: CategoryRepository) -> None:
        self._categories = categories

    async def execute(self, category_id: int) -> CategoryDTO:
        category = await self._categories.get_by_id(category_id)
        if category is None:
            raise EntityNotFoundError("Category", category_id)
        figures_count = await self._categories.count_figures(category_id)
        return CategoryDTO(
            id=category.id, name=category.name, slug=category.slug, figures_count=figures_count  # type: ignore[arg-type]
        )
