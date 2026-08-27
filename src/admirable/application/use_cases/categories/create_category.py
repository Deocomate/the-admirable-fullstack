from admirable.application.dto.category_dto import CategoryDTO, CreateCategoryCommand
from admirable.domain.entities.category import Category
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.value_objects.slug import Slug


class CreateCategory:
    def __init__(self, categories: CategoryRepository) -> None:
        self._categories = categories

    async def execute(self, cmd: CreateCategoryCommand) -> CategoryDTO:
        slug = Slug.from_text(cmd.name)
        created = await self._categories.add(Category(id=None, name=cmd.name, slug=slug.value))
        return CategoryDTO(id=created.id, name=created.name, slug=created.slug)  # type: ignore[arg-type]
