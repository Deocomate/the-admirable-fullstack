from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Page[T]:
    """Replaces Laravel's `LengthAwarePaginator`."""

    items: Sequence[T]
    total: int
    page: int
    per_page: int

    @property
    def last_page(self) -> int:
        if self.per_page <= 0:
            return 1
        return max(1, -(-self.total // self.per_page))

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def has_next(self) -> bool:
        return self.page < self.last_page

    def window(self, size: int = 5) -> list[int]:
        """Page numbers to render around the current page (pagination macro)."""
        half = size // 2
        start = max(1, self.page - half)
        end = min(self.last_page, start + size - 1)
        start = max(1, end - size + 1)
        return list(range(start, end + 1))
