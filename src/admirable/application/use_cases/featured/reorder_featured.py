from admirable.domain.repositories.featured_figure_repository import FeaturedFigureRepository


class ReorderFeatured:
    def __init__(self, featured: FeaturedFigureRepository) -> None:
        self._featured = featured

    async def execute(self, figure_ids_in_order: list[int]) -> None:
        await self._featured.reorder(figure_ids_in_order)
