"""CRUD functional coverage for the two simplest admin resources —
categories (incl. duplicate-name rejection) and contacts."""

import re

from httpx import AsyncClient

from tests.functional.admin.conftest import csrf_token


async def test_category_crud_round_trip(admin_client: AsyncClient) -> None:
    create_page = await admin_client.get("/admin/categories/create")
    assert create_page.status_code == 200
    token = csrf_token(create_page.text)

    store = await admin_client.post(
        "/admin/categories", data={"_token": token, "name": "Func Test Category"}
    )
    assert store.status_code == 303

    index = await admin_client.get("/admin/categories")
    assert "Func Test Category" in index.text
    match = re.search(r"Func Test Category.*?/admin/categories/(\d+)/edit", index.text, re.S)
    assert match is not None
    category_id = match.group(1)

    # duplicate name is rejected with a field error, not a 500/silent success
    dup_page = await admin_client.get("/admin/categories/create")
    dup_token = csrf_token(dup_page.text)
    dup = await admin_client.post(
        "/admin/categories",
        data={"_token": dup_token, "name": "Func Test Category"},
        follow_redirects=True,
    )
    assert "đã tồn tại" in dup.text

    edit_page = await admin_client.get(f"/admin/categories/{category_id}/edit")
    assert edit_page.status_code == 200
    edit_token = csrf_token(edit_page.text)
    update = await admin_client.post(
        f"/admin/categories/{category_id}",
        data={"_token": edit_token, "name": "Func Test Category Renamed", "_method": "PUT"},
    )
    assert update.status_code == 303
    renamed = await admin_client.get("/admin/categories")
    assert "Func Test Category Renamed" in renamed.text

    delete_token = csrf_token(
        (await admin_client.get(f"/admin/categories/{category_id}/edit")).text
    )
    destroy = await admin_client.post(
        f"/admin/categories/{category_id}",
        data={"_token": delete_token, "_method": "DELETE"},
    )
    assert destroy.status_code == 303
    final_index = await admin_client.get("/admin/categories")
    assert "Func Test Category Renamed" not in final_index.text


async def test_contact_crud_round_trip(admin_client: AsyncClient) -> None:
    create_page = await admin_client.get("/admin/contacts/create")
    token = csrf_token(create_page.text)
    store = await admin_client.post(
        "/admin/contacts",
        data={
            "_token": token,
            "type": "email",
            "label": "Func Test Contact",
            "value": "functest@example.com",
            "sort_order": "5",
            "is_active": "1",
        },
    )
    assert store.status_code == 303

    index = await admin_client.get("/admin/contacts")
    assert "Func Test Contact" in index.text
    match = re.search(r"Func Test Contact.*?/admin/contacts/(\d+)/edit", index.text, re.S)
    assert match is not None
    contact_id = match.group(1)

    edit_page = await admin_client.get(f"/admin/contacts/{contact_id}/edit")
    assert edit_page.status_code == 200
    edit_token = csrf_token(edit_page.text)
    update = await admin_client.post(
        f"/admin/contacts/{contact_id}",
        data={
            "_token": edit_token,
            "type": "phone",
            "label": "Func Test Contact Updated",
            "value": "0123456789",
            "sort_order": "1",
            "is_active": "0",  # the real form's hidden input sends this when unchecked
            "_method": "PUT",
        },
    )
    assert update.status_code == 303
    updated_index = await admin_client.get("/admin/contacts")
    assert "Func Test Contact Updated" in updated_index.text
    assert "Ẩn" in updated_index.text  # is_active toggled off is reflected

    delete_token = csrf_token((await admin_client.get(f"/admin/contacts/{contact_id}/edit")).text)
    destroy = await admin_client.post(
        f"/admin/contacts/{contact_id}",
        data={"_token": delete_token, "_method": "DELETE"},
    )
    assert destroy.status_code == 303
    final_index = await admin_client.get("/admin/contacts")
    assert "Func Test Contact Updated" not in final_index.text
