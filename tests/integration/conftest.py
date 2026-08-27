from collections.abc import AsyncIterator, Iterator

import pytest
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, create_async_engine

from admirable.config import DbSettings
from tests.integration.sql_counter import SqlCounter


@pytest.fixture(scope="session")
def test_db_settings() -> DbSettings:
    return DbSettings(
        host="127.0.0.1", port=3306, user="admirable", password="secret", database="admirable_test"
    )


@pytest.fixture(scope="session")
async def engine(test_db_settings: DbSettings) -> AsyncIterator[AsyncEngine]:
    eng = create_async_engine(test_db_settings.dsn, pool_pre_ping=True)
    yield eng
    await eng.dispose()


@pytest.fixture
async def connection(engine: AsyncEngine) -> AsyncIterator[AsyncConnection]:
    async with engine.connect() as conn:
        yield conn


@pytest.fixture
async def db_session(connection: AsyncConnection) -> AsyncIterator[AsyncSession]:
    """Wraps each test in an outer transaction that is always rolled back —
    no test ever leaves data behind, and tables never need truncating."""
    outer_tx = await connection.begin()
    session = AsyncSession(bind=connection, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        await session.close()
        await outer_tx.rollback()


@pytest.fixture
def sql_counter(connection: AsyncConnection) -> Iterator[SqlCounter]:
    counter = SqlCounter()
    sync_engine = connection.engine.sync_engine

    def _before_cursor_execute(*_args: object, **_kwargs: object) -> None:
        counter.count += 1

    event.listen(sync_engine, "before_cursor_execute", _before_cursor_execute)
    try:
        yield counter
    finally:
        event.remove(sync_engine, "before_cursor_execute", _before_cursor_execute)
