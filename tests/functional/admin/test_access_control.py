"""Auth guard coverage: unauthenticated -> redirect to login; a non-superadmin
authenticated user -> 403 on the superadmin-only `/admin/users*` group."""

import re

from httpx import AsyncClient

from tests.functional.admin.conftest import SUPERADMIN_PASSWORD, csrf_token, login

_PROTECTED_GET_ROUTES = [
    "/admin/dashboard",
    "/admin/categories",
    "/admin/figures",
    "/admin/stories",
    "/admin/contacts",
    "/admin/featured-figures",
    "/admin/settings/about-us",
    "/admin/users",
]


async def test_unauthenticated_get_redirects_to_login(client: AsyncClient) -> None:
    for path in _PROTECTED_GET_ROUTES:
        response = await client.get(path, follow_redirects=False)
        assert response.status_code == 303, path
        assert response.headers["location"].endswith("/admin/login"), path


async def test_non_superadmin_forbidden_from_users(admin_client: AsyncClient) -> None:
    # Create a plain admin via the real endpoint (dogfooding CreateUser).
    page = await admin_client.get("/admin/users/create")
    token = csrf_token(page.text)
    email = "qa-access-control@example.com"
    r = await admin_client.post(
        "/admin/users",
        data={
            "_token": token,
            "name": "QA Access Control",
            "email": email,
            "password": "password123",
            "password_confirmation": "password123",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303

    try:
        # Log the SAME client out and back in as the new plain admin.
        logout_page = await admin_client.get("/admin/dashboard")
        logout_token = csrf_token(logout_page.text)
        await admin_client.post("/admin/logout", data={"_token": logout_token})

        await login(admin_client, email, "password123")
        forbidden = await admin_client.get("/admin/users", follow_redirects=False)
        assert forbidden.status_code == 403

        create_forbidden = await admin_client.get("/admin/users/create", follow_redirects=False)
        assert create_forbidden.status_code == 403
    finally:
        # Log the plain admin out before logging back in as superadmin —
        # `login()` hits `/admin/login`, which 303s away for anyone already
        # authenticated (`require_guest`), leaving an empty redirect body.
        dashboard = await admin_client.get("/admin/dashboard")
        if dashboard.status_code == 200:
            await admin_client.post("/admin/logout", data={"_token": csrf_token(dashboard.text)})
        await login(admin_client, "admin@gmail.com", SUPERADMIN_PASSWORD)
        idx = await admin_client.get("/admin/users")
        m = re.search(rf"{email}.*?/admin/users/(\d+)/edit", idx.text, re.S)
        if m:
            edit = await admin_client.get(f"/admin/users/{m.group(1)}/edit")
            token = csrf_token(edit.text)
            await admin_client.post(
                f"/admin/users/{m.group(1)}", data={"_token": token, "_method": "DELETE"}
            )
