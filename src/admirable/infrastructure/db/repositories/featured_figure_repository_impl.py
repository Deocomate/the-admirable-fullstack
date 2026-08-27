from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from admirable.domain.entities.featured_figure import FeaturedFigure
from admirable.domain.entities.figure import Figure
from admirable.infrastructure.clock import SystemClock
from admirable.infrastructure.db.mappers import featured_figure_mapper, figure_mapper
from admirable.infrastructure.db.models.featured_figure import FeaturedFigureModel
from admirable.infrastructure.db.models.figure import FigureModel


class FeaturedFigureRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._clock = SystemClock()

    async def list_ordered_with_figure(
        self, limit: int | None = None
    ) -> list[tuple[FeaturedFigure, Figure]]:
        stmt = (
            select(FeaturedFigureModel)
            .join(FeaturedFigureModel.figure)
            .options(selectinload(FeaturedFigureModel.figure).selectinload(FigureModel.categories))
            .order_by(FeaturedFigureModel.priority, FeaturedFigureModel.id)
        )
        if limit is not None:
            stmt = stmt.limit(limit)
        models = (await self._session.execute(stmt)).scalars().all()
        return [
            (featured_figure_mapper.to_entity(m), figure_mapper.to_entity(m.figure)) for m in models
        ]

    async def get_by_id(self, featured_figure_id: int) -> FeaturedFigure | None:
        model = await self._session.get(FeaturedFigureModel, featured_figure_id)
        return featured_figure_mapper.to_entity(model) if model else None

    async def get_by_figure_id(self, figure_id: int) -> FeaturedFigure | None:
        stmt = select(FeaturedFigureModel).where(FeaturedFigureModel.figure_id == figure_id)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return featured_figure_mapper.to_entity(model) if model else None

    async def max_priority(self) -> int:
        stmt = select(func.max(FeaturedFigureModel.priority))
        return (await self._session.execute(stmt)).scalar_one() or 0

    async def list_available_figures(self, search: str | None, limit: int) -> list[Figure]:
        featured_subq = select(FeaturedFigureModel.figure_id)
        stmt = select(FigureModel).where(FigureModel.id.notin_(featured_subq))
        if search:
            stmt = stmt.where(FigureModel.name.like(f"%{search}%"))
        stmt = stmt.order_by(FigureModel.name).limit(limit)
        models = (await self._session.execute(stmt)).scalars().all()
        return [figure_mapper.to_entity(m) for m in models]

    async def add(self, featured_figure: FeaturedFigure) -> FeaturedFigure:
        model = FeaturedFigureModel()
        featured_figure_mapper.apply_to_model(featured_figure, model)
        now = self._clock.now()
        model.created_at = now
        model.updated_at = now
        self._session.add(model)
        await self._session.flush()
        return featured_figure_mapper.to_entity(model)

    async def remove(self, featured_figure_id: int) -> None:
        model = await self._session.get(FeaturedFigureModel, featured_figure_id)
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()

    async def reorder(self, figure_ids_in_order: list[int]) -> None:
        stmt = select(FeaturedFigureModel).where(
            FeaturedFigureModel.figure_id.in_(figure_ids_in_order)
        )
        models = {m.figure_id: m for m in (await self._session.execute(stmt)).scalars().all()}
        for priority, figure_id in enumerate(figure_ids_in_order):
            if figure_id in models:
                models[figure_id].priority = priority
        await self._session.flush()
