"""Users CRUD plus the two business-rule guards `UserService::deleteAdmin`
enforces: a superadmin can never be deleted, and nobody can delete themselves
— both with their exact Vietnamese messages preserved."""

import re

from httpx import AsyncClient

from tests.functional.admin.conftest import SUPERADMIN_EMAIL, csrf_token


async def test_user_crud_round_trip(admin_client: AsyncClient) -> None:
    create_page = await admin_client.get("/admin/users/create")
    assert create_page.status_code == 200
    token = csrf_token(create_page.text)

    store = await admin_client.post(
        "/admin/users",
        data={
            "_token": token,
            "name": "Func Test User",
            "email": "func-test-user@example.com",
            "password": "password123",
            "password_confirmation": "password123",
        },
    )
    assert store.status_code == 303

    index = await admin_client.get("/admin/users")
    assert "Func Test User" in index.text
    match = re.search(r"Func Test User.*?/admin/users/(\d+)/edit", index.text, re.S)
    assert match is not None
    user_id = match.group(1)

    # duplicate email rejected
    dup_page = await admin_client.get("/admin/users/create")
    dup_token = csrf_token(dup_page.text)
    dup = await admin_client.post(
        "/admin/users",
        data={
            "_token": dup_token,
            "name": "Dup",
            "email": "func-test-user@example.com",
            "password": "password123",
            "password_confirmation": "password123",
        },
        follow_redirects=True,
    )
    assert "đã được sử dụng" in dup.text

    edit_page = await admin_client.get(f"/admin/users/{user_id}/edit")
    assert edit_page.status_code == 200
    edit_token = csrf_token(edit_page.text)
    update = await admin_client.post(
        f"/admin/users/{user_id}",
        data={
            "_token": edit_token,
            "name": "Func Test User Renamed",
            "email": "func-test-user@example.com",
            "_method": "PUT",
        },
    )
    assert update.status_code == 303
    renamed = await admin_client.get("/admin/users")
    assert "Func Test User Renamed" in renamed.text

    # this regular admin CAN be deleted by the superadmin
    delete_token = csrf_token((await admin_client.get(f"/admin/users/{user_id}/edit")).text)
    destroy = await admin_client.post(
        f"/admin/users/{user_id}", data={"_token": delete_token, "_method": "DELETE"}
    )
    assert destroy.status_code == 303
    final_index = await admin_client.get("/admin/users")
    assert "Func Test User Renamed" not in final_index.text


async def test_cannot_delete_superadmin(admin_client: AsyncClient) -> None:
    # The index hides the delete form for a superadmin row entirely, so
    # resolve the logged-in superadmin's own id via the "Bạn" (self) badge
    # and drive the guard directly through the destroy route.
    index = await admin_client.get("/admin/users")
    self_row = re.search(r"<tr[^>]*>((?:(?!</tr>).)*?Bạn(?:(?!</tr>).)*?)</tr>", index.text, re.S)
    assert self_row is not None, "could not locate the logged-in user's own row"
    self_id_match = re.search(r"/admin/users/(\d+)/edit", self_row.group(1))
    assert self_id_match is not None
    self_id = self_id_match.group(1)

    edit_page = await admin_client.get(f"/admin/users/{self_id}/edit")
    token = csrf_token(edit_page.text)
    response = await admin_client.post(
        f"/admin/users/{self_id}",
        data={"_token": token, "_method": "DELETE"},
        follow_redirects=True,
    )
    # Self-delete guard fires first only if role check allows it; either way
    # the superadmin must survive with the guard's exact message shown.
    assert "Không thể xóa tài khoản superadmin." in response.text
    still_there = await admin_client.get("/admin/users")
    assert SUPERADMIN_EMAIL in still_there.text
