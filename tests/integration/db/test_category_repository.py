from sqlalchemy.ext.asyncio import AsyncSession

from admirable.domain.entities.category import Category
from admirable.infrastructure.db.repositories.category_repository_impl import CategoryRepositoryImpl


async def test_add_list_update_delete(db_session: AsyncSession) -> None:
    repo = CategoryRepositoryImpl(db_session)
    category = await repo.add(Category(id=None, name="Cat IT", slug="cat-it"))
    assert category.id is not None

    all_categories = await repo.list_all()
    assert any(c.slug == "cat-it" for c in all_categories)

    category.name = "Cat IT Renamed"
    updated = await repo.update(category)
    assert updated.name == "Cat IT Renamed"

    await repo.delete(category.id)
    assert await repo.get_by_id(category.id) is None
