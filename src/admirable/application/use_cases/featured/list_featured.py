from admirable.application.dto.featured_dto import FeaturedFigureDTO
from admirable.domain.repositories.featured_figure_repository import FeaturedFigureRepository


class ListFeatured:
    def __init__(self, featured: FeaturedFigureRepository) -> None:
        self._featured = featured

    async def execute(self) -> list[FeaturedFigureDTO]:
        pairs = await self._featured.list_ordered_with_figure()
        return [
            FeaturedFigureDTO(
                id=ff.id,  # type: ignore[arg-type]
                figure_id=figure.id,  # type: ignore[arg-type]
                figure_name=figure.name,
                figure_slug=figure.slug,
                figure_avatar_path=figure.avatar_path,
                priority=ff.priority,
            )
            for ff, figure in pairs
        ]
