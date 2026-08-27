from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from admirable.config import AppSettings, DbSettings, MediaSettings, RedisSettings, Settings
from admirable.presentation.web.main import create_app


@pytest.fixture
def settings() -> Settings:
    return Settings(
        app=AppSettings(secret_key="a" * 32, env="testing", debug=True),
        db=DbSettings(),
        redis=RedisSettings(),
        media=MediaSettings(),
    )


@pytest.fixture
async def client(settings: Settings) -> AsyncIterator[AsyncClient]:
    app = create_app(settings)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
