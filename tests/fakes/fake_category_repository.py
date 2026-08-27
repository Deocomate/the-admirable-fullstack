from admirable.domain.entities.category import Category
from admirable.domain.value_objects.pagination import Page


class FakeCategoryRepository:
    def __init__(self) -> None:
        self._items: dict[int, Category] = {}
        self._next_id = 1
        self.figure_counts: dict[int, int] = {}

    async def get_by_id(self, category_id: int) -> Category | None:
        return self._items.get(category_id)

    async def get_by_name(self, name: str) -> Category | None:
        return next((c for c in self._items.values() if c.name == name), None)

    async def list_paginated(self, page: int, per_page: int) -> Page[Category]:
        items = list(self._items.values())
        start = (page - 1) * per_page
        return Page(
            items=items[start : start + per_page], total=len(items), page=page, per_page=per_page
        )

    async def list_all(self) -> list[Category]:
        return sorted(self._items.values(), key=lambda c: c.name)

    async def count(self) -> int:
        return len(self._items)

    async def count_figures(self, category_id: int) -> int:
        return self.figure_counts.get(category_id, 0)

    async def add(self, category: Category) -> Category:
        category.id = self._next_id
        self._next_id += 1
        self._items[category.id] = category
        return category

    async def update(self, category: Category) -> Category:
        assert category.id is not None
        self._items[category.id] = category
        return category

    async def delete(self, category_id: int) -> None:
        self._items.pop(category_id, None)
