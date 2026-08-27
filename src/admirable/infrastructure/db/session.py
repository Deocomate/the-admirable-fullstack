from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from admirable.config import DbSettings


def create_engine(settings: DbSettings) -> AsyncEngine:
    return create_async_engine(
        settings.dsn,
        pool_size=settings.pool_size,
        max_overflow=10,
        pool_pre_ping=True,
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def session_scope(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    """One request = one session = one transaction."""
    async with session_factory() as session, session.begin():
        yield session


async def dispose_engine(engine: AsyncEngine) -> None:
    await engine.dispose()
