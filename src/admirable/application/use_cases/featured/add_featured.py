from admirable.domain.entities.featured_figure import FeaturedFigure
from admirable.domain.exceptions import BusinessRuleViolationError, EntityNotFoundError
from admirable.domain.repositories.featured_figure_repository import FeaturedFigureRepository
from admirable.domain.repositories.figure_repository import FigureRepository


class AddFeatured:
    def __init__(self, featured: FeaturedFigureRepository, figures: FigureRepository) -> None:
        self._featured = featured
        self._figures = figures

    async def execute(self, figure_id: int) -> FeaturedFigure:
        if await self._figures.get_by_id(figure_id) is None:
            raise EntityNotFoundError("Figure", figure_id)
        if await self._featured.get_by_figure_id(figure_id) is not None:
            raise BusinessRuleViolationError("Figure is already featured")

        next_priority = await self._featured.max_priority() + 1
        return await self._featured.add(
            FeaturedFigure(id=None, figure_id=figure_id, priority=next_priority)
        )
