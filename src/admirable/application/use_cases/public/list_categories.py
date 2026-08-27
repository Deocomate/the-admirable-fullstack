from admirable.application.dto.category_dto import CategoryDTO
from admirable.domain.repositories.category_repository import CategoryRepository


class ListCategories:
    def __init__(self, categories: CategoryRepository) -> None:
        self._categories = categories

    async def execute(self) -> list[CategoryDTO]:
        return [
            CategoryDTO(id=c.id, name=c.name, slug=c.slug)  # type: ignore[arg-type]
            for c in await self._categories.list_all()
        ]
