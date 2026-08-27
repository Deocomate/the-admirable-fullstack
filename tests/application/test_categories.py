import pytest

from admirable.application.dto.category_dto import CreateCategoryCommand, UpdateCategoryCommand
from admirable.application.use_cases.categories.create_category import CreateCategory
from admirable.application.use_cases.categories.delete_category import DeleteCategory
from admirable.application.use_cases.categories.get_category import GetCategory
from admirable.application.use_cases.categories.list_categories import (
    ListCategories,
    ListCategoriesQuery,
)
from admirable.application.use_cases.categories.update_category import UpdateCategory
from admirable.domain.exceptions import EntityNotFoundError
from tests.fakes.fake_category_repository import FakeCategoryRepository


async def test_create_category_generates_slug() -> None:
    categories = FakeCategoryRepository()
    result = await CreateCategory(categories).execute(CreateCategoryCommand(name="Nhà khoa học"))
    assert result.slug == "nha-khoa-hoc"


async def test_update_category() -> None:
    categories = FakeCategoryRepository()
    created = await CreateCategory(categories).execute(CreateCategoryCommand(name="Old Name"))
    updated = await UpdateCategory(categories).execute(
        UpdateCategoryCommand(category_id=created.id, name="New Name")
    )
    assert updated.name == "New Name"
    assert updated.slug == "new-name"


async def test_update_missing_category_raises() -> None:
    categories = FakeCategoryRepository()
    with pytest.raises(EntityNotFoundError):
        await UpdateCategory(categories).execute(UpdateCategoryCommand(category_id=999, name="X"))


async def test_get_category_includes_figure_count() -> None:
    categories = FakeCategoryRepository()
    created = await CreateCategory(categories).execute(CreateCategoryCommand(name="Cat"))
    categories.figure_counts[created.id] = 5
    result = await GetCategory(categories).execute(created.id)
    assert result.figures_count == 5


async def test_get_missing_category_raises() -> None:
    categories = FakeCategoryRepository()
    with pytest.raises(EntityNotFoundError):
        await GetCategory(categories).execute(999)


async def test_delete_category() -> None:
    categories = FakeCategoryRepository()
    created = await CreateCategory(categories).execute(CreateCategoryCommand(name="Cat"))
    await DeleteCategory(categories).execute(created.id)
    assert await categories.get_by_id(created.id) is None


async def test_list_categories() -> None:
    categories = FakeCategoryRepository()
    await CreateCategory(categories).execute(CreateCategoryCommand(name="A"))
    await CreateCategory(categories).execute(CreateCategoryCommand(name="B"))
    result = await ListCategories(categories).execute(ListCategoriesQuery(page=1, per_page=15))
    assert result.total == 2
    assert len(result.items) == 2
