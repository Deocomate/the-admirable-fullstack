from admirable.application.dto.category_dto import CategoryDTO, CreateCategoryCommand
from admirable.domain.entities.category import Category
from admirable.domain.exceptions import DuplicateValueError
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.value_objects.slug import Slug


class CreateCategory:
    def __init__(self, categories: CategoryRepository) -> None:
        self._categories = categories

    async def execute(self, cmd: CreateCategoryCommand) -> CategoryDTO:
        if await self._categories.get_by_name(cmd.name) is not None:
            raise DuplicateValueError("name", cmd.name)
        slug = Slug.from_text(cmd.name)
        created = await self._categories.add(Category(id=None, name=cmd.name, slug=slug.value))
        return CategoryDTO(
            id=created.id,  # type: ignore[arg-type]
            name=created.name,
            slug=created.slug,
            created_at=created.created_at,
        )
