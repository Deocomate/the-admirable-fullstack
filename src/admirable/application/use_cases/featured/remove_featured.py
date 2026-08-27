from admirable.domain.repositories.featured_figure_repository import FeaturedFigureRepository


class RemoveFeatured:
    def __init__(self, featured: FeaturedFigureRepository) -> None:
        self._featured = featured

    async def execute(self, featured_figure_id: int) -> None:
        await self._featured.remove(featured_figure_id)
