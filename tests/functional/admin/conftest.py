"""Shared fixtures for admin functional tests. Reuses the parent
`tests/functional/conftest.py` `client` fixture (real dev DB + isolated Redis
DB 2)."""

import re

import pytest
from httpx import AsyncClient

SUPERADMIN_EMAIL = "admin@gmail.com"
SUPERADMIN_PASSWORD = "Admin@123"

_TOKEN_RE = re.compile(r'name="_token" value="([^"]+)"')


def csrf_token(html: str) -> str:
    match = _TOKEN_RE.search(html)
    assert match is not None, "csrf token input not found in page"
    return match.group(1)


async def login(client: AsyncClient, email: str, password: str) -> None:
    page = await client.get("/admin/login")
    token = csrf_token(page.text)
    response = await client.post(
        "/admin/login",
        data={"_token": token, "email": email, "password": password},
        follow_redirects=False,
    )
    assert response.status_code == 303, f"login failed: {response.text[:300]}"


@pytest.fixture
async def admin_client(client: AsyncClient) -> AsyncClient:
    """`client` already logged in as the real migrated superadmin."""
    await login(client, SUPERADMIN_EMAIL, SUPERADMIN_PASSWORD)
    return client
