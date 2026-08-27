from typing import Protocol

from admirable.domain.entities.figure import Figure
from admirable.domain.value_objects.pagination import Page


class FigureRepository(Protocol):
    async def list_all(self) -> list[Figure]:
        """Full figure list ordered by name — used to populate admin select
        dropdowns (stories/figures forms)."""
        ...

    async def get_by_id(self, figure_id: int) -> Figure | None: ...

    async def get_by_slug(self, slug: str) -> Figure | None: ...

    async def list_paginated(
        self,
        search: str | None,
        category_id: int | None,
        page: int,
        per_page: int,
    ) -> Page[Figure]:
        """Featured figures sort first (by priority), then newest first — matches
        `CategoryController::index`/`show`."""
        ...

    async def get_top_featured(self, category_id: int | None) -> Figure | None:
        """Highest-priority featured figure, optionally scoped to one category."""
        ...

    async def list_related(
        self, figure_id: int, category_ids: list[int], limit: int
    ) -> list[Figure]:
        """Other figures sharing at least one category, excluding `figure_id`."""
        ...

    async def search(
        self,
        query: str,
        category_slug: str | None,
        page: int,
        per_page: int,
    ) -> Page[Figure]:
        """Same featured-first ordering — matches `SearchController::index`."""
        ...

    async def list_latest(self, limit: int, exclude_ids: list[int]) -> list[Figure]: ...

    async def list_trending(self, limit: int) -> list[Figure]:
        """Ordered by story snippet count descending."""
        ...

    async def count(self) -> int: ...

    async def slug_exists(self, slug: str, exclude_id: int | None = None) -> bool: ...

    async def add(self, figure: Figure) -> Figure: ...

    async def update(self, figure: Figure) -> Figure: ...

    async def delete(self, figure_id: int) -> None: ...

    async def sync_categories(self, figure_id: int, category_ids: list[int]) -> None: ...
