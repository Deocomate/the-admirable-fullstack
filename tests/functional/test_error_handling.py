"""Confirms unhandled exceptions never leak a traceback to the client,
regardless of debug/production settings."""

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from admirable.config import AppSettings, DbSettings, MediaSettings, RedisSettings, Settings
from admirable.presentation.web.middleware.error_handler import register_exception_handlers
from admirable.presentation.web.templating import build_templates


async def test_unhandled_exception_returns_generic_500_without_traceback() -> None:
    settings = Settings(
        app=AppSettings(secret_key="a" * 32, env="production", debug=False),
        db=DbSettings(),
        redis=RedisSettings(),
        media=MediaSettings(),
    )
    app = FastAPI()
    register_exception_handlers(app, build_templates(settings))

    @app.get("/boom")
    async def boom() -> None:
        raise RuntimeError("some internal secret detail that must not leak")

    # raise_app_exceptions=False: a real ASGI server (uvicorn) only logs the
    # exception ServerErrorMiddleware re-raises after sending the response —
    # it doesn't affect what the client receives. httpx's default transport
    # would otherwise propagate that re-raise into the test itself.
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/boom")

    assert response.status_code == 500
    assert "some internal secret detail" not in response.text
    assert "Traceback" not in response.text
    assert "RuntimeError" not in response.text
