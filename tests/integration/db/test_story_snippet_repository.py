from sqlalchemy.ext.asyncio import AsyncSession

from admirable.domain.entities.figure import Figure
from admirable.domain.entities.story_snippet import StorySnippet
from admirable.domain.value_objects.content_block import parse_content_blocks
from admirable.infrastructure.db.repositories.figure_repository_impl import FigureRepositoryImpl
from admirable.infrastructure.db.repositories.story_snippet_repository_impl import (
    StorySnippetRepositoryImpl,
)


def make_figure(slug: str) -> Figure:
    return Figure(
        id=None, name="Story Figure", slug=slug, short_description=None, key_facts=[],
        content_blocks=[], search_text="",
    )


async def test_add_and_list_other_by_figure(db_session: AsyncSession) -> None:
    figure_repo = FigureRepositoryImpl(db_session)
    snippet_repo = StorySnippetRepositoryImpl(db_session)

    figure = await figure_repo.add(make_figure("story-figure-it"))
    blocks = parse_content_blocks([{"type": "heading", "text_en": "Chapter 1"}])
    s1 = await snippet_repo.add(
        StorySnippet(
            id=None, figure_id=figure.id, title="First", subtitle=None,  # type: ignore[arg-type]
            content_blocks=blocks, search_text="Chapter 1",
        )
    )
    s2 = await snippet_repo.add(
        StorySnippet(
            id=None, figure_id=figure.id, title="Second", subtitle=None,  # type: ignore[arg-type]
            content_blocks=blocks, search_text="Chapter 1",
        )
    )

    others = await snippet_repo.list_other_by_figure(figure.id, exclude_id=s1.id, limit=10)  # type: ignore[arg-type]
    assert [o.id for o in others] == [s2.id]

    assert await snippet_repo.count_by_figure(figure.id) == 2  # type: ignore[arg-type]
