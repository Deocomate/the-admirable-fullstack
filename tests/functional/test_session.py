import re

from httpx import AsyncClient
from redis.asyncio import from_url

_TEST_REDIS_URL = "redis://127.0.0.1:6379/2"
_SUPERADMIN_EMAIL = "admin@gmail.com"
_SUPERADMIN_PASSWORD = "Admin@123"


def _extract_csrf_token(html: str) -> str:
    match = re.search(r'name="_token" value="([^"]+)"', html)
    assert match is not None
    return match.group(1)


async def test_logout_deletes_redis_key(client: AsyncClient) -> None:
    page = await client.get("/admin/login")
    token = _extract_csrf_token(page.text)
    await client.post(
        "/admin/login",
        data={"_token": token, "email": _SUPERADMIN_EMAIL, "password": _SUPERADMIN_PASSWORD},
        follow_redirects=False,
    )

    redis = from_url(_TEST_REDIS_URL)
    try:
        keys_before = await redis.keys("sess:*")
        assert len(keys_before) >= 1

        dashboard = await client.get("/admin/dashboard")
        logout_token = _extract_csrf_token(dashboard.text)
        await client.post("/admin/logout", data={"_token": logout_token})

        keys_after = await redis.keys("sess:*")
        assert len(keys_after) < len(keys_before)
    finally:
        await redis.aclose()


async def test_flash_message_visible_once_then_gone(client: AsyncClient) -> None:
    page = await client.get("/admin/login")
    token = _extract_csrf_token(page.text)
    await client.post(
        "/admin/login",
        data={"_token": token, "email": _SUPERADMIN_EMAIL, "password": "wrong"},
        follow_redirects=False,
    )

    first_view = await client.get("/admin/login")
    assert "không đúng" in first_view.text

    second_view = await client.get("/admin/login")
    assert "không đúng" not in second_view.text
