"""Full end-to-end auth flow against the real dev DB (admin@gmail.com's
actual migrated bcrypt hash) and an isolated Redis DB (2)."""

import re

from httpx import AsyncClient

_SUPERADMIN_EMAIL = "admin@gmail.com"
_SUPERADMIN_PASSWORD = "Admin@123"


def _extract_csrf_token(html: str) -> str:
    match = re.search(r'name="_token" value="([^"]+)"', html)
    assert match is not None, "csrf token input not found in page"
    return match.group(1)


async def test_login_page_renders_with_csrf_meta_and_cookie(client: AsyncClient) -> None:
    response = await client.get("/admin/login")
    assert response.status_code == 200
    assert 'name="csrf-token"' in response.text
    assert "admirable_session" in response.headers.get("set-cookie", "")


async def test_wrong_password_redirects_with_error_and_keeps_old_email(client: AsyncClient) -> None:
    page = await client.get("/admin/login")
    token = _extract_csrf_token(page.text)

    response = await client.post(
        "/admin/login",
        data={"_token": token, "email": _SUPERADMIN_EMAIL, "password": "wrong-password"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"].endswith("/admin/login")

    retry_page = await client.get("/admin/login")
    assert "không đúng" in retry_page.text
    assert f'value="{_SUPERADMIN_EMAIL}"' in retry_page.text


async def test_successful_login_regenerates_session_and_reaches_dashboard(
    client: AsyncClient,
) -> None:
    page = await client.get("/admin/login")
    token = _extract_csrf_token(page.text)
    sid_before = client.cookies.get("admirable_session")

    response = await client.post(
        "/admin/login",
        data={"_token": token, "email": _SUPERADMIN_EMAIL, "password": _SUPERADMIN_PASSWORD},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"].endswith("/admin/dashboard")

    sid_after = client.cookies.get("admirable_session")
    assert sid_after != sid_before  # session fixation protection

    dashboard = await client.get("/admin/dashboard")
    assert dashboard.status_code == 200
    assert "Super Admin" in dashboard.text


async def test_logout_clears_session_and_dashboard_redirects_to_login(client: AsyncClient) -> None:
    page = await client.get("/admin/login")
    token = _extract_csrf_token(page.text)
    await client.post(
        "/admin/login",
        data={"_token": token, "email": _SUPERADMIN_EMAIL, "password": _SUPERADMIN_PASSWORD},
        follow_redirects=False,
    )

    dashboard = await client.get("/admin/dashboard")
    logout_token = _extract_csrf_token(dashboard.text)
    logout_response = await client.post(
        "/admin/logout", data={"_token": logout_token}, follow_redirects=False
    )
    assert logout_response.status_code == 303
    assert logout_response.headers["location"].endswith("/admin/login")

    after_logout = await client.get("/admin/dashboard", follow_redirects=False)
    assert after_logout.status_code == 303
    assert after_logout.headers["location"].endswith("/admin/login")


async def test_dashboard_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/admin/dashboard", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].endswith("/admin/login")


async def test_login_page_redirects_away_when_already_authenticated(client: AsyncClient) -> None:
    page = await client.get("/admin/login")
    token = _extract_csrf_token(page.text)
    await client.post(
        "/admin/login",
        data={"_token": token, "email": _SUPERADMIN_EMAIL, "password": _SUPERADMIN_PASSWORD},
        follow_redirects=False,
    )

    response = await client.get("/admin/login", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].endswith("/admin/dashboard")
