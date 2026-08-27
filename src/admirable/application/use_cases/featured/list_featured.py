from admirable.application.dto.featured_dto import FeaturedFigureDTO
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.featured_figure_repository import FeaturedFigureRepository


class ListFeatured:
    def __init__(self, featured: FeaturedFigureRepository, categories: CategoryRepository) -> None:
        self._featured = featured
        self._categories = categories

    async def execute(self) -> list[FeaturedFigureDTO]:
        pairs = await self._featured.list_ordered_with_figure()
        all_categories = {c.id: c.name for c in await self._categories.list_all()}
        return [
            FeaturedFigureDTO(
                id=ff.id,  # type: ignore[arg-type]
                figure_id=figure.id,  # type: ignore[arg-type]
                figure_name=figure.name,
                figure_slug=figure.slug,
                figure_avatar_path=figure.avatar_path,
                figure_short_description=figure.short_description,
                figure_category_names=[
                    all_categories[cid] for cid in figure.category_ids if cid in all_categories
                ],
                priority=ff.priority,
            )
            for ff, figure in pairs
        ]
