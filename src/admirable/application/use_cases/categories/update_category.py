from admirable.application.dto.category_dto import CategoryDTO, UpdateCategoryCommand
from admirable.domain.exceptions import DuplicateValueError, EntityNotFoundError
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.value_objects.slug import Slug


class UpdateCategory:
    def __init__(self, categories: CategoryRepository) -> None:
        self._categories = categories

    async def execute(self, cmd: UpdateCategoryCommand) -> CategoryDTO:
        category = await self._categories.get_by_id(cmd.category_id)
        if category is None:
            raise EntityNotFoundError("Category", cmd.category_id)
        existing = await self._categories.get_by_name(cmd.name)
        if existing is not None and existing.id != cmd.category_id:
            raise DuplicateValueError("name", cmd.name)
        category.name = cmd.name
        category.slug = Slug.from_text(cmd.name).value
        updated = await self._categories.update(category)
        return CategoryDTO(
            id=updated.id,  # type: ignore[arg-type]
            name=updated.name,
            slug=updated.slug,
            created_at=updated.created_at,
        )
