from admirable.domain.entities.story_snippet import StorySnippet
from admirable.domain.value_objects.pagination import Page


class FakeStorySnippetRepository:
    def __init__(self) -> None:
        self._items: dict[int, StorySnippet] = {}
        self._next_id = 1

    async def get_by_id(self, snippet_id: int) -> StorySnippet | None:
        return self._items.get(snippet_id)

    async def list_paginated(
        self, figure_id: int | None, search: str | None, page: int, per_page: int
    ) -> Page[StorySnippet]:
        items = list(self._items.values())
        if figure_id is not None:
            items = [s for s in items if s.figure_id == figure_id]
        if search:
            items = [s for s in items if search.lower() in s.title.lower()]
        items.sort(key=lambda s: s.id or 0, reverse=True)
        start = (page - 1) * per_page
        return Page(
            items=items[start : start + per_page], total=len(items), page=page, per_page=per_page
        )

    async def count(self) -> int:
        return len(self._items)

    async def count_by_figure(self, figure_id: int) -> int:
        return sum(1 for s in self._items.values() if s.figure_id == figure_id)

    async def list_other_by_figure(
        self, figure_id: int, exclude_id: int, limit: int
    ) -> list[StorySnippet]:
        items = [s for s in self._items.values() if s.figure_id == figure_id and s.id != exclude_id]
        return items[:limit]

    async def add(self, snippet: StorySnippet) -> StorySnippet:
        snippet.id = self._next_id
        self._next_id += 1
        self._items[snippet.id] = snippet
        return snippet

    async def update(self, snippet: StorySnippet) -> StorySnippet:
        assert snippet.id is not None
        self._items[snippet.id] = snippet
        return snippet

    async def delete(self, snippet_id: int) -> None:
        self._items.pop(snippet_id, None)
