"""Fixtures for HTTP-level client route tests. Reuses the parent
`tests/functional/conftest.py` `client` fixture (real dev DB + isolated Redis
DB 2). `story` additionally seeds one real `story_snippets` row — the
migrated dev DB currently has zero rows in that table — and deletes it in
teardown so the fixture is repeatable and leaves no residue."""

from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from admirable.config import Settings
from admirable.domain.entities.story_snippet import StorySnippet
from admirable.domain.value_objects.content_block import parse_content_blocks
from admirable.infrastructure.db.repositories.figure_repository_impl import FigureRepositoryImpl
from admirable.infrastructure.db.repositories.story_snippet_repository_impl import (
    StorySnippetRepositoryImpl,
)
from admirable.infrastructure.db.session import create_engine, create_session_factory


@pytest.fixture
async def db_session(functional_settings: Settings) -> AsyncIterator[AsyncSession]:
    """A plain session with no wrapping `session.begin()` (unlike
    `session_scope`, which only commits at generator-close time — too late
    for a row that must be visible to the live app mid-test): the `story`
    fixture commits explicitly right after insert, and again after its own
    cleanup delete."""
    engine = create_engine(functional_settings.db)
    factory = create_session_factory(engine)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest.fixture
async def story(db_session: AsyncSession) -> AsyncIterator[StorySnippet]:
    figures = FigureRepositoryImpl(db_session)
    snippets = StorySnippetRepositoryImpl(db_session)

    # A specific, known-categorized figure (not "first in an arbitrary list")
    # so `article:section`/`article:tag` assertions in test_seo.py are
    # deterministic regardless of what else exists in the dev DB.
    figure = await figures.get_by_slug("mark-zuckerberg")
    assert figure is not None, "dev DB seed figure 'mark-zuckerberg' not found"
    figure_id = figure.id
    assert figure_id is not None

    blocks = parse_content_blocks(
        [{"type": "paragraph", "text_en": "A functional-test story.", "text_vi": "Chuyện thử."}]
    )
    created = await snippets.add(
        StorySnippet(
            id=None,
            figure_id=figure_id,
            title="Functional Test Story",
            subtitle="A subtitle for testing",
            content_blocks=blocks,
            search_text="A functional-test story",
        )
    )
    await db_session.commit()
    try:
        yield created
    finally:
        assert created.id is not None
        await snippets.delete(created.id)
        await db_session.commit()
