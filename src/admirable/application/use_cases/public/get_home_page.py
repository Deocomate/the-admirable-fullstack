"""Ports `HomeController::index`, including its "backfill" algorithm: the
top 7 featured records supply the hero + first 6 latest slots; if fewer than
6 remain, the newest non-featured figures fill the rest."""

from admirable.application.dto.category_dto import CategoryDTO
from admirable.application.dto.public_dto import HomePageDTO, HomeStatsDTO
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.featured_figure_repository import FeaturedFigureRepository
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository

from ._figure_summary import category_name_map, to_summary

_FEATURED_FETCH_LIMIT = 7
_LATEST_TARGET = 6


class GetHomePage:
    def __init__(
        self,
        figures: FigureRepository,
        categories: CategoryRepository,
        story_snippets: StorySnippetRepository,
        featured: FeaturedFigureRepository,
    ) -> None:
        self._figures = figures
        self._categories = categories
        self._story_snippets = story_snippets
        self._featured = featured

    async def execute(self) -> HomePageDTO:
        names = await category_name_map(self._categories)
        categories = [
            CategoryDTO(id=c.id, name=c.name, slug=c.slug)  # type: ignore[arg-type]
            for c in await self._categories.list_all()
        ]

        featured_pairs = await self._featured.list_ordered_with_figure(limit=_FEATURED_FETCH_LIMIT)
        featured_figures = [figure for _, figure in featured_pairs]

        featured_figure = None
        latest_figures = []
        if featured_figures:
            featured_figure = await to_summary(
                featured_figures[0], names, self._story_snippets, is_featured=True
            )
            for figure in featured_figures[1 : _LATEST_TARGET + 1]:
                summary = await to_summary(figure, names, self._story_snippets, is_featured=True)
                latest_figures.append(summary)

        if len(latest_figures) < _LATEST_TARGET:
            exclude_ids = [f.id for f in featured_figures if f.id is not None]
            fallback = await self._figures.list_latest(
                _LATEST_TARGET - len(latest_figures), exclude_ids
            )
            for figure in fallback:
                summary = await to_summary(figure, names, self._story_snippets, is_featured=False)
                latest_figures.append(summary)

        stats = HomeStatsDTO(
            figures=await self._figures.count(),
            categories=len(categories),
            stories=await self._story_snippets.count(),
        )

        return HomePageDTO(
            categories=categories,
            featured_figure=featured_figure,
            latest_figures=latest_figures,
            stats=stats,
        )
