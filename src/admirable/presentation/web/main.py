"""FastAPI application factory."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from redis.asyncio import Redis, from_url
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from admirable.config import Settings, get_settings
from admirable.infrastructure.db.session import create_engine, create_session_factory
from admirable.presentation.web.middleware.csrf import CsrfMiddleware
from admirable.presentation.web.middleware.error_handler import register_exception_handlers
from admirable.presentation.web.middleware.method_override import MethodOverrideMiddleware
from admirable.presentation.web.middleware.session import RedisSessionMiddleware
from admirable.presentation.web.routers.admin.auth import auth_router, guest_router
from admirable.presentation.web.templating import build_templates

_STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings: Settings = app.state.settings
    engine: AsyncEngine = create_engine(settings.db)
    app.state.engine = engine
    app.state.session_factory = create_session_factory(engine)
    try:
        yield
    finally:
        await engine.dispose()
        await app.state.redis.aclose()


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title=settings.app.name, debug=settings.app.debug, lifespan=lifespan)
    app.state.settings = settings
    app.state.templates = build_templates(settings)

    # Constructed once here (not in lifespan) so the same client instance can
    # be handed to both the session middleware (added below) and app.state
    # (used by get_redis / healthz) — middleware is wired before lifespan runs.
    redis_client: Redis = from_url(settings.redis.url)
    app.state.redis = redis_client

    register_exception_handlers(app, app.state.templates)

    # Registered innermost-first: Starlette wraps each add_middleware call
    # around the previous stack, so the LAST one added runs FIRST on a
    # request. This order yields the required execution order:
    # Session (outer) -> MethodOverride -> CSRF -> router.
    app.add_middleware(CsrfMiddleware)
    app.add_middleware(MethodOverrideMiddleware)
    app.add_middleware(
        RedisSessionMiddleware,
        redis=redis_client,
        secret_key=settings.app.secret_key,
        cookie_name=settings.session.cookie_name,
        ttl_seconds=settings.session.lifetime_seconds,
        secure=settings.session.secure,
    )

    if _STATIC_DIR.is_dir():
        from starlette.staticfiles import StaticFiles

        app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")

    app.include_router(guest_router)
    app.include_router(auth_router)

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
