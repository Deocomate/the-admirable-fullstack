from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from redis.asyncio import from_url

from admirable.config import (
    AppSettings,
    DbSettings,
    MediaSettings,
    RedisSettings,
    SessionSettings,
    Settings,
)
from admirable.presentation.web.main import create_app

_TEST_REDIS_URL = "redis://127.0.0.1:6379/2"  # isolated DB, away from the live dev session (0)


@pytest.fixture
def functional_settings() -> Settings:
    return Settings(
        app=AppSettings(secret_key="a" * 32, env="testing", debug=True, base_url="http://test"),
        db=DbSettings(
            host="127.0.0.1", port=3306, user="admirable", password="secret", database="admirable"
        ),
        redis=RedisSettings(url=_TEST_REDIS_URL),
        media=MediaSettings(),
        session=SessionSettings(secure=False),
    )


@pytest.fixture
async def client(functional_settings: Settings) -> AsyncIterator[AsyncClient]:
    app = create_app(functional_settings)
    transport = ASGITransport(app=app)
    client_cm = AsyncClient(transport=transport, base_url="http://test")
    async with app.router.lifespan_context(app), client_cm as ac:
        yield ac
    redis = from_url(_TEST_REDIS_URL)
    await redis.flushdb()
    await redis.aclose()
