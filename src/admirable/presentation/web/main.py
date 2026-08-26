"""FastAPI application factory."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis, from_url
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from admirable.config import Settings, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings: Settings = app.state.settings
    engine: AsyncEngine = create_async_engine(settings.db.dsn, pool_size=settings.db.pool_size)
    redis: Redis = from_url(settings.redis.url)
    app.state.engine = engine
    app.state.redis = redis
    try:
        yield
    finally:
        await engine.dispose()
        await redis.aclose()


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title=settings.app.name, debug=settings.app.debug, lifespan=lifespan)
    app.state.settings = settings

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        db_status = "ok"
        redis_status = "ok"
        try:
            engine: AsyncEngine = app.state.engine
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception:
            db_status = "error"
        try:
            redis: Redis = app.state.redis
            await redis.ping()
        except Exception:
            redis_status = "error"
        return {"db": db_status, "redis": redis_status}

    return app


app = create_app()
