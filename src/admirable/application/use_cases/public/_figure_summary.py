from admirable.application.dto.figure_dto import FigureSummaryDTO
from admirable.domain.entities.figure import Figure
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository


async def to_summary(
    figure: Figure,
    all_category_names: dict[int, str],
    story_snippets: StorySnippetRepository,
    is_featured: bool = False,
) -> FigureSummaryDTO:
    names = [all_category_names[cid] for cid in figure.category_ids if cid in all_category_names]
    count = await story_snippets.count_by_figure(figure.id)  # type: ignore[arg-type]
    return FigureSummaryDTO(
        id=figure.id,  # type: ignore[arg-type]
        name=figure.name,
        slug=figure.slug,
        avatar_path=figure.avatar_path,
        short_description=figure.short_description,
        category_names=names,
        story_snippets_count=count,
        is_featured=is_featured,
    )


async def category_name_map(categories: CategoryRepository) -> dict[int, str]:
    return {c.id: c.name for c in await categories.list_all()}  # type: ignore[misc]
