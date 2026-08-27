from admirable.application.dto.figure_dto import FigureDetailDTO
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.figure_repository import FigureRepository

from ._mapping import to_figure_detail_dto


class GetFigure:
    def __init__(self, figures: FigureRepository, categories: CategoryRepository) -> None:
        self._figures = figures
        self._categories = categories

    async def execute(self, figure_id: int) -> FigureDetailDTO:
        figure = await self._figures.get_by_id(figure_id)
        if figure is None:
            raise EntityNotFoundError("Figure", figure_id)

        all_categories = {c.id: c.name for c in await self._categories.list_all()}
        names = [all_categories[cid] for cid in figure.category_ids if cid in all_categories]
        return to_figure_detail_dto(figure, category_names=names)
