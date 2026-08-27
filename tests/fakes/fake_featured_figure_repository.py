from admirable.domain.entities.featured_figure import FeaturedFigure
from admirable.domain.entities.figure import Figure
from tests.fakes.fake_figure_repository import FakeFigureRepository


class FakeFeaturedFigureRepository:
    def __init__(self, figures: FakeFigureRepository) -> None:
        self._items: dict[int, FeaturedFigure] = {}
        self._next_id = 1
        self._figures = figures

    async def list_ordered_with_figure(
        self, limit: int | None = None
    ) -> list[tuple[FeaturedFigure, Figure]]:
        ordered = sorted(self._items.values(), key=lambda ff: (ff.priority, ff.id or 0))
        if limit is not None:
            ordered = ordered[:limit]
        result = []
        for ff in ordered:
            figure = await self._figures.get_by_id(ff.figure_id)
            if figure is not None:
                result.append((ff, figure))
        return result

    async def get_by_id(self, featured_figure_id: int) -> FeaturedFigure | None:
        return self._items.get(featured_figure_id)

    async def get_by_figure_id(self, figure_id: int) -> FeaturedFigure | None:
        return next((ff for ff in self._items.values() if ff.figure_id == figure_id), None)

    async def max_priority(self) -> int:
        if not self._items:
            return -1
        return max(ff.priority for ff in self._items.values())

    async def list_available_figures(self, search: str | None, limit: int) -> list[Figure]:
        featured_ids = {ff.figure_id for ff in self._items.values()}
        items = [f for f in self._figures._items.values() if f.id not in featured_ids]
        if search:
            items = [f for f in items if search.lower() in f.name.lower()]
        return items[:limit]

    async def add(self, featured_figure: FeaturedFigure) -> FeaturedFigure:
        featured_figure.id = self._next_id
        self._next_id += 1
        self._items[featured_figure.id] = featured_figure
        self._figures.featured_ids.add(featured_figure.figure_id)
        return featured_figure

    async def remove(self, featured_figure_id: int) -> None:
        item = self._items.pop(featured_figure_id, None)
        if item is not None:
            self._figures.featured_ids.discard(item.figure_id)

    async def reorder(self, figure_ids_in_order: list[int]) -> None:
        by_figure = {ff.figure_id: ff for ff in self._items.values()}
        for priority, figure_id in enumerate(figure_ids_in_order):
            if figure_id in by_figure:
                by_figure[figure_id].priority = priority
