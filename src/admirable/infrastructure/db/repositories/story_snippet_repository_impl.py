from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from admirable.domain.entities.story_snippet import StorySnippet
from admirable.domain.value_objects.pagination import Page
from admirable.infrastructure.clock import SystemClock
from admirable.infrastructure.db.mappers import story_snippet_mapper
from admirable.infrastructure.db.models.story_snippet import StorySnippetModel


class StorySnippetRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._clock = SystemClock()

    async def get_by_id(self, snippet_id: int) -> StorySnippet | None:
        model = await self._session.get(StorySnippetModel, snippet_id)
        return story_snippet_mapper.to_entity(model) if model else None

    async def list_paginated(
        self,
        figure_id: int | None,
        search: str | None,
        page: int,
        per_page: int,
    ) -> Page[StorySnippet]:
        stmt = select(StorySnippetModel)
        count_stmt = select(func.count()).select_from(StorySnippetModel)

        if figure_id is not None:
            stmt = stmt.where(StorySnippetModel.figure_id == figure_id)
            count_stmt = count_stmt.where(StorySnippetModel.figure_id == figure_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(StorySnippetModel.title.like(like))
            count_stmt = count_stmt.where(StorySnippetModel.title.like(like))

        stmt = (
            stmt.order_by(StorySnippetModel.created_at.desc())
            .limit(per_page)
            .offset((page - 1) * per_page)
        )

        total = (await self._session.execute(count_stmt)).scalar_one()
        models = (await self._session.execute(stmt)).scalars().all()
        return Page(
            items=[story_snippet_mapper.to_entity(m) for m in models],
            total=total,
            page=page,
            per_page=per_page,
        )

    async def count(self) -> int:
        stmt = select(func.count()).select_from(StorySnippetModel)
        return (await self._session.execute(stmt)).scalar_one()

    async def count_by_figure(self, figure_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(StorySnippetModel)
            .where(StorySnippetModel.figure_id == figure_id)
        )
        return (await self._session.execute(stmt)).scalar_one()

    async def list_other_by_figure(
        self, figure_id: int, exclude_id: int, limit: int
    ) -> list[StorySnippet]:
        stmt = (
            select(StorySnippetModel)
            .where(StorySnippetModel.figure_id == figure_id, StorySnippetModel.id != exclude_id)
            .limit(limit)
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [story_snippet_mapper.to_entity(m) for m in models]

    async def add(self, snippet: StorySnippet) -> StorySnippet:
        model = StorySnippetModel()
        story_snippet_mapper.apply_to_model(snippet, model)
        now = self._clock.now()
        model.created_at = now
        model.updated_at = now
        self._session.add(model)
        await self._session.flush()
        return story_snippet_mapper.to_entity(model)

    async def update(self, snippet: StorySnippet) -> StorySnippet:
        model = await self._session.get(StorySnippetModel, snippet.id)
        if model is None:
            raise ValueError(f"StorySnippet {snippet.id} not found")
        story_snippet_mapper.apply_to_model(snippet, model)
        model.updated_at = self._clock.now()
        await self._session.flush()
        return story_snippet_mapper.to_entity(model)

    async def delete(self, snippet_id: int) -> None:
        model = await self._session.get(StorySnippetModel, snippet_id)
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()
