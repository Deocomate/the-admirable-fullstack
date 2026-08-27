from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from admirable.domain.entities.category import Category
from admirable.domain.value_objects.pagination import Page
from admirable.infrastructure.db.mappers import category_mapper
from admirable.infrastructure.db.models.associations import category_figure_table
from admirable.infrastructure.db.models.category import CategoryModel


class CategoryRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, category_id: int) -> Category | None:
        model = await self._session.get(CategoryModel, category_id)
        return category_mapper.to_entity(model) if model else None

    async def list_paginated(self, page: int, per_page: int) -> Page[Category]:
        count_stmt = select(func.count()).select_from(CategoryModel)
        stmt = (
            select(CategoryModel)
            .order_by(CategoryModel.created_at.desc())
            .limit(per_page)
            .offset((page - 1) * per_page)
        )
        total = (await self._session.execute(count_stmt)).scalar_one()
        models = (await self._session.execute(stmt)).scalars().all()
        items = [category_mapper.to_entity(m) for m in models]
        return Page(items=items, total=total, page=page, per_page=per_page)

    async def list_all(self) -> list[Category]:
        stmt = select(CategoryModel).order_by(CategoryModel.name)
        models = (await self._session.execute(stmt)).scalars().all()
        return [category_mapper.to_entity(m) for m in models]

    async def count_figures(self, category_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(category_figure_table)
            .where(category_figure_table.c.category_id == category_id)
        )
        return (await self._session.execute(stmt)).scalar_one()

    async def add(self, category: Category) -> Category:
        model = CategoryModel()
        category_mapper.apply_to_model(category, model)
        self._session.add(model)
        await self._session.flush()
        return category_mapper.to_entity(model)

    async def update(self, category: Category) -> Category:
        model = await self._session.get(CategoryModel, category.id)
        if model is None:
            raise ValueError(f"Category {category.id} not found")
        category_mapper.apply_to_model(category, model)
        await self._session.flush()
        return category_mapper.to_entity(model)

    async def delete(self, category_id: int) -> None:
        model = await self._session.get(CategoryModel, category_id)
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()
