from admirable.application.dto.public_dto import FigureDetailPageDTO, StorySummaryLite
from admirable.application.use_cases.figures._mapping import to_dto_blocks
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository

from ._figure_summary import category_name_map, to_summary

_RELATED_LIMIT = 3


class GetFigureDetail:
    def __init__(
        self,
        figures: FigureRepository,
        categories: CategoryRepository,
        story_snippets: StorySnippetRepository,
    ) -> None:
        self._figures = figures
        self._categories = categories
        self._story_snippets = story_snippets

    async def execute(self, slug: str) -> FigureDetailPageDTO:
        figure = await self._figures.get_by_slug(slug)
        if figure is None:
            raise EntityNotFoundError("Figure", slug)

        names = await category_name_map(self._categories)
        category_names = [names[cid] for cid in figure.category_ids if cid in names]

        snippets_page = await self._story_snippets.list_paginated(
            figure_id=figure.id, search=None, page=1, per_page=1_000_000
        )
        snippets = [
            StorySummaryLite(id=s.id, title=s.title, subtitle=s.subtitle, image_path=s.image_path)  # type: ignore[arg-type]
            for s in snippets_page.items
        ]

        related = await self._figures.list_related(figure.id, figure.category_ids, _RELATED_LIMIT)  # type: ignore[arg-type]
        related_dtos = [await to_summary(r, names, self._story_snippets) for r in related]

        return FigureDetailPageDTO(
            id=figure.id,  # type: ignore[arg-type]
            name=figure.name,
            slug=figure.slug,
            avatar_path=figure.avatar_path,
            short_description=figure.short_description,
            key_facts=[{"label": f.label, "value": f.value} for f in figure.key_facts],
            content_blocks=[b.model_dump() for b in to_dto_blocks(figure.content_blocks)],
            audio_path=figure.audio_path,
            youtube_url=figure.youtube_url,
            category_names=category_names,
            story_snippets=snippets,
            related_figures=related_dtos,
        )
