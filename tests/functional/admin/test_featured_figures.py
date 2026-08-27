"""Featured figures: add, drag-reorder (the JSON `reorder` endpoint), and
remove — end to end against the real dev DB."""

import re

from httpx import AsyncClient

from tests.functional.admin.conftest import csrf_token


async def test_add_reorder_remove_featured_figure(admin_client: AsyncClient) -> None:
    figures_page = await admin_client.get("/admin/figures")
    ids = re.findall(r"/admin/figures/(\d+)/edit", figures_page.text)
    assert len(ids) >= 1, "dev DB has no figures to feature"
    figure_id = ids[0]

    index = await admin_client.get("/admin/featured-figures")
    assert index.status_code == 200
    already_featured = f'data-figure-id="{figure_id}"' in index.text
    token = csrf_token(index.text)

    if not already_featured:
        store = await admin_client.post(
            "/admin/featured-figures", data={"_token": token, "figure_id": figure_id}
        )
        assert store.status_code == 303

    try:
        index2 = await admin_client.get("/admin/featured-figures")
        assert f'data-figure-id="{figure_id}"' in index2.text

        # reorder: single-element order is a trivial but valid reorder call
        reorder_token = csrf_token(index2.text)
        reorder = await admin_client.post(
            "/admin/featured-figures/reorder",
            json={"figure_ids": [int(figure_id)]},
            headers={"X-CSRF-TOKEN": reorder_token, "Accept": "application/json"},
        )
        assert reorder.status_code == 200
        assert "message" in reorder.json()
    finally:
        index3 = await admin_client.get("/admin/featured-figures")
        match = re.search(
            rf'data-figure-id="{figure_id}".*?/admin/featured-figures/(\d+)', index3.text, re.S
        )
        if match:
            remove_token = csrf_token(index3.text)
            destroy = await admin_client.post(
                f"/admin/featured-figures/{match.group(1)}",
                data={"_token": remove_token, "_method": "DELETE"},
            )
            assert destroy.status_code == 303
            index4 = await admin_client.get("/admin/featured-figures")
            assert f'data-figure-id="{figure_id}"' not in index4.text
