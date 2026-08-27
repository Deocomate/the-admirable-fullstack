from admirable.application.dto.category_dto import CategoryDTO, UpdateCategoryCommand
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.value_objects.slug import Slug


class UpdateCategory:
    def __init__(self, categories: CategoryRepository) -> None:
        self._categories = categories

    async def execute(self, cmd: UpdateCategoryCommand) -> CategoryDTO:
        category = await self._categories.get_by_id(cmd.category_id)
        if category is None:
            raise EntityNotFoundError("Category", cmd.category_id)
        category.name = cmd.name
        category.slug = Slug.from_text(cmd.name).value
        updated = await self._categories.update(category)
        return CategoryDTO(id=updated.id, name=updated.name, slug=updated.slug)  # type: ignore[arg-type]
