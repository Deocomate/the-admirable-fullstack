from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from admirable.domain.entities.figure import Figure
from admirable.domain.value_objects.pagination import Page
from admirable.infrastructure.db.mappers import figure_mapper
from admirable.infrastructure.db.models.associations import category_figure_table
from admirable.infrastructure.db.models.category import CategoryModel
from admirable.infrastructure.db.models.featured_figure import FeaturedFigureModel
from admirable.infrastructure.db.models.figure import FigureModel
from admirable.infrastructure.db.models.story_snippet import StorySnippetModel


class FigureRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, figure_id: int) -> Figure | None:
        stmt = (
            select(FigureModel)
            .where(FigureModel.id == figure_id)
            .options(selectinload(FigureModel.categories))
        )
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return figure_mapper.to_entity(model) if model else None

    async def get_by_slug(self, slug: str) -> Figure | None:
        stmt = (
            select(FigureModel)
            .where(FigureModel.slug == slug)
            .options(selectinload(FigureModel.categories))
        )
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return figure_mapper.to_entity(model) if model else None

    async def list_paginated(
        self,
        search: str | None,
        category_id: int | None,
        page: int,
        per_page: int,
    ) -> Page[Figure]:
        stmt = select(FigureModel).options(selectinload(FigureModel.categories))
        count_stmt = select(func.count()).select_from(FigureModel)

        if search:
            like = f"%{search}%"
            stmt = stmt.where(FigureModel.name.like(like))
            count_stmt = count_stmt.where(FigureModel.name.like(like))
        if category_id is not None:
            category_match = category_figure_table.c.category_id == category_id
            stmt = stmt.join(FigureModel.categories).where(category_match)
            count_stmt = count_stmt.join(
                category_figure_table, category_figure_table.c.figure_id == FigureModel.id
            ).where(category_match)

        offset = (page - 1) * per_page
        stmt = stmt.order_by(FigureModel.created_at.desc()).limit(per_page).offset(offset)

        total = (await self._session.execute(count_stmt)).scalar_one()
        models = (await self._session.execute(stmt)).scalars().all()
        items = [figure_mapper.to_entity(m) for m in models]
        return Page(items=items, total=total, page=page, per_page=per_page)

    async def search(
        self,
        query: str,
        category_slug: str | None,
        page: int,
        per_page: int,
    ) -> Page[Figure]:
        base = select(FigureModel).outerjoin(
            FeaturedFigureModel, FeaturedFigureModel.figure_id == FigureModel.id
        )
        count_base = (
            select(func.count(func.distinct(FigureModel.id)))
            .select_from(FigureModel)
            .outerjoin(FeaturedFigureModel, FeaturedFigureModel.figure_id == FigureModel.id)
        )

        if query:
            like = f"%{query}%"
            condition = (
                FigureModel.name.like(like)
                | FigureModel.short_description.like(like)
                | FigureModel.search_text.like(like)
            )
            base = base.where(condition)
            count_base = count_base.where(condition)

        if category_slug:
            slug_match = CategoryModel.slug == category_slug
            base = base.join(FigureModel.categories).where(slug_match)
            count_base = count_base.join(FigureModel.categories).where(slug_match)

        stmt = (
            base.options(selectinload(FigureModel.categories))
            .order_by(
                FeaturedFigureModel.id.is_(None),
                FeaturedFigureModel.priority,
                FigureModel.created_at.desc(),
            )
            .limit(per_page)
            .offset((page - 1) * per_page)
        )

        total = (await self._session.execute(count_base)).scalar_one()
        models = (await self._session.execute(stmt)).scalars().unique().all()
        items = [figure_mapper.to_entity(m) for m in models]
        return Page(items=items, total=total, page=page, per_page=per_page)

    async def list_latest(self, limit: int, exclude_ids: list[int]) -> list[Figure]:
        stmt = select(FigureModel).options(selectinload(FigureModel.categories))
        if exclude_ids:
            stmt = stmt.where(FigureModel.id.notin_(exclude_ids))
        stmt = stmt.order_by(FigureModel.created_at.desc()).limit(limit)
        models = (await self._session.execute(stmt)).scalars().all()
        return [figure_mapper.to_entity(m) for m in models]

    async def list_trending(self, limit: int) -> list[Figure]:
        story_count = func.count(StorySnippetModel.id).label("story_snippets_count")
        stmt = (
            select(FigureModel)
            .outerjoin(StorySnippetModel, StorySnippetModel.figure_id == FigureModel.id)
            .options(selectinload(FigureModel.categories))
            .group_by(FigureModel.id)
            .order_by(story_count.desc())
            .limit(limit)
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [figure_mapper.to_entity(m) for m in models]

    async def get_top_featured(self, category_id: int | None) -> Figure | None:
        stmt = (
            select(FigureModel)
            .join(FeaturedFigureModel, FeaturedFigureModel.figure_id == FigureModel.id)
            .options(selectinload(FigureModel.categories))
            .order_by(FeaturedFigureModel.priority)
        )
        if category_id is not None:
            stmt = stmt.join(FigureModel.categories).where(CategoryModel.id == category_id)
        model = (await self._session.execute(stmt.limit(1))).scalars().first()
        return figure_mapper.to_entity(model) if model else None

    async def list_related(
        self, figure_id: int, category_ids: list[int], limit: int
    ) -> list[Figure]:
        if not category_ids:
            return []
        category_match = category_figure_table.c.category_id.in_(category_ids)
        stmt = (
            select(FigureModel)
            .join(FigureModel.categories)
            .where(FigureModel.id != figure_id, category_match)
            .options(selectinload(FigureModel.categories))
            .distinct()
            .limit(limit)
        )
        models = (await self._session.execute(stmt)).scalars().unique().all()
        return [figure_mapper.to_entity(m) for m in models]

    async def count(self) -> int:
        stmt = select(func.count()).select_from(FigureModel)
        return (await self._session.execute(stmt)).scalar_one()

    async def slug_exists(self, slug: str, exclude_id: int | None = None) -> bool:
        stmt = select(func.count()).select_from(FigureModel).where(FigureModel.slug == slug)
        if exclude_id is not None:
            stmt = stmt.where(FigureModel.id != exclude_id)
        return (await self._session.execute(stmt)).scalar_one() > 0

    async def add(self, figure: Figure) -> Figure:
        model = FigureModel()
        figure_mapper.apply_to_model(figure, model)
        self._session.add(model)
        await self._session.flush()
        return figure_mapper.to_entity(model)

    async def update(self, figure: Figure) -> Figure:
        model = await self._session.get(FigureModel, figure.id)
        if model is None:
            raise ValueError(f"Figure {figure.id} not found")
        figure_mapper.apply_to_model(figure, model)
        await self._session.flush()
        return figure_mapper.to_entity(model)

    async def delete(self, figure_id: int) -> None:
        model = await self._session.get(FigureModel, figure_id)
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()

    async def sync_categories(self, figure_id: int, category_ids: list[int]) -> None:
        model = await self._session.get(
            FigureModel, figure_id, options=[selectinload(FigureModel.categories)]
        )
        if model is None:
            raise ValueError(f"Figure {figure_id} not found")

        wanted = set(category_ids)
        current = {c.id for c in model.categories}
        to_remove = current - wanted
        to_add = wanted - current
        model.categories = [c for c in model.categories if c.id not in to_remove]
        if to_add:
            add_stmt = select(CategoryModel).where(CategoryModel.id.in_(to_add))
            new_categories = (await self._session.execute(add_stmt)).scalars().all()
            model.categories.extend(new_categories)
        await self._session.flush()
