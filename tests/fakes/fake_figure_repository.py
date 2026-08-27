from admirable.domain.entities.figure import Figure
from admirable.domain.value_objects.pagination import Page


class FakeFigureRepository:
    def __init__(self) -> None:
        self._items: dict[int, Figure] = {}
        self._next_id = 1
        self.featured_ids: set[int] = set()
        """Test-only hook: mirrors what FeaturedFigureRepository would report,
        used by search()/get_top_featured() ordering."""

    async def list_all(self) -> list[Figure]:
        return sorted(self._items.values(), key=lambda f: f.name)

    async def get_by_id(self, figure_id: int) -> Figure | None:
        return self._items.get(figure_id)

    async def get_by_slug(self, slug: str) -> Figure | None:
        return next((f for f in self._items.values() if f.slug == slug), None)

    async def list_paginated(
        self, search: str | None, category_id: int | None, page: int, per_page: int
    ) -> Page[Figure]:
        items = list(self._items.values())
        if search:
            items = [f for f in items if search.lower() in f.name.lower()]
        if category_id is not None:
            items = [f for f in items if category_id in f.category_ids]
        items.sort(key=lambda f: f.id or 0, reverse=True)
        start = (page - 1) * per_page
        return Page(
            items=items[start : start + per_page], total=len(items), page=page, per_page=per_page
        )

    async def search(
        self, query: str, category_slug: str | None, page: int, per_page: int
    ) -> Page[Figure]:
        items = list(self._items.values())
        if query:
            items = [
                f
                for f in items
                if query.lower() in f.name.lower()
                or (f.short_description and query.lower() in f.short_description.lower())
                or query.lower() in f.search_text.lower()
            ]
        items.sort(key=lambda f: (0 if f.id in self.featured_ids else 1, -(f.id or 0)))
        start = (page - 1) * per_page
        return Page(
            items=items[start : start + per_page], total=len(items), page=page, per_page=per_page
        )

    async def list_latest(self, limit: int, exclude_ids: list[int]) -> list[Figure]:
        items = [f for f in self._items.values() if f.id not in exclude_ids]
        items.sort(key=lambda f: f.id or 0, reverse=True)
        return items[:limit]

    async def list_trending(self, limit: int) -> list[Figure]:
        items = list(self._items.values())
        return items[:limit]

    async def get_top_featured(self, category_id: int | None) -> Figure | None:
        candidates = [f for f in self._items.values() if f.id in self.featured_ids]
        if category_id is not None:
            candidates = [f for f in candidates if category_id in f.category_ids]
        return candidates[0] if candidates else None

    async def list_related(
        self, figure_id: int, category_ids: list[int], limit: int
    ) -> list[Figure]:
        items = [
            f
            for f in self._items.values()
            if f.id != figure_id and set(f.category_ids) & set(category_ids)
        ]
        return items[:limit]

    async def count(self) -> int:
        return len(self._items)

    async def slug_exists(self, slug: str, exclude_id: int | None = None) -> bool:
        return any(f.slug == slug and f.id != exclude_id for f in self._items.values())

    async def add(self, figure: Figure) -> Figure:
        figure.id = self._next_id
        self._next_id += 1
        self._items[figure.id] = figure
        return figure

    async def update(self, figure: Figure) -> Figure:
        assert figure.id is not None
        self._items[figure.id] = figure
        return figure

    async def delete(self, figure_id: int) -> None:
        self._items.pop(figure_id, None)

    async def sync_categories(self, figure_id: int, category_ids: list[int]) -> None:
        figure = self._items[figure_id]
        figure.category_ids = list(category_ids)
