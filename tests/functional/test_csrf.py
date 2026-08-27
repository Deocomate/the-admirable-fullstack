import re

from httpx import AsyncClient


def _extract_csrf_token(html: str) -> str:
    match = re.search(r'name="_token" value="([^"]+)"', html)
    assert match is not None
    return match.group(1)


async def test_post_without_token_returns_419(client: AsyncClient) -> None:
    response = await client.post("/admin/login", data={"email": "x@example.com", "password": "y"})
    assert response.status_code == 419


async def test_post_with_wrong_token_returns_419(client: AsyncClient) -> None:
    await client.get("/admin/login")  # establish a session
    response = await client.post(
        "/admin/login",
        data={"_token": "totally-wrong-token", "email": "x@example.com", "password": "y"},
    )
    assert response.status_code == 419


async def test_post_with_valid_token_passes_csrf_check(client: AsyncClient) -> None:
    page = await client.get("/admin/login")
    token = _extract_csrf_token(page.text)
    response = await client.post(
        "/admin/login",
        data={"_token": token, "email": "wrong@example.com", "password": "wrong"},
        follow_redirects=False,
    )
    # Not 419: the request passed CSRF and reached the login use case,
    # which redirected back because the credentials themselves are wrong.
    assert response.status_code == 303


async def test_header_token_accepted_case_insensitively(client: AsyncClient) -> None:
    page = await client.get("/admin/login")
    token = _extract_csrf_token(page.text)
    response = await client.post(
        "/admin/login",
        data={"email": "wrong@example.com", "password": "wrong"},
        headers={"X-CSRF-TOKEN": token},
        follow_redirects=False,
    )
    assert response.status_code == 303


async def test_json_accept_header_gets_json_419_body(client: AsyncClient) -> None:
    response = await client.post(
        "/admin/login",
        data={"email": "x", "password": "y"},
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 419
    assert response.headers["content-type"].startswith("application/json")
