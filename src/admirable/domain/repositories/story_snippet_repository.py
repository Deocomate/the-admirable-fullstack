from typing import Protocol

from admirable.domain.entities.story_snippet import StorySnippet
from admirable.domain.value_objects.pagination import Page


class StorySnippetRepository(Protocol):
    async def get_by_id(self, snippet_id: int) -> StorySnippet | None: ...

    async def list_paginated(
        self,
        figure_id: int | None,
        search: str | None,
        page: int,
        per_page: int,
    ) -> Page[StorySnippet]: ...

    async def count(self) -> int: ...

    async def count_by_figure(self, figure_id: int) -> int: ...

    async def list_other_by_figure(
        self, figure_id: int, exclude_id: int, limit: int
    ) -> list[StorySnippet]:
        """Other snippets from the same figure, excluding the current one."""
        ...

    async def add(self, snippet: StorySnippet) -> StorySnippet: ...

    async def update(self, snippet: StorySnippet) -> StorySnippet: ...

    async def delete(self, snippet_id: int) -> None: ...
