"""Figures + stories CRUD, incl. avatar upload and the plan's explicit
"validation error must preserve every entered content block" criterion."""

import re

from httpx import AsyncClient

from tests.functional.admin.conftest import csrf_token

_PNG_BYTES = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010802000000907753"
    "de0000000c4944415408d763f8ffff3f0005fe02fea1379b3c0000000049454e44ae426082"
)


async def test_figure_crud_with_avatar_and_content_blocks(admin_client: AsyncClient) -> None:
    create_page = await admin_client.get("/admin/figures/create")
    assert create_page.status_code == 200
    token = csrf_token(create_page.text)

    data = {
        "_token": token,
        "name": "Func Test Figure",
        "short_description": "A figure created by a functional test.",
        "content_blocks[0][type]": "heading",
        "content_blocks[0][text_en]": "Func Heading",
        "content_blocks[1][type]": "paragraph",
        "content_blocks[1][text_en]": "English body.",
        "content_blocks[1][text_vi]": "Nội dung tiếng Việt.",
        "key_facts[0][label]": "Born",
        "key_facts[0][value]": "1990",
    }
    store = await admin_client.post(
        "/admin/figures",
        data=data,
        files={"avatar": ("avatar.png", _PNG_BYTES, "image/png")},
        follow_redirects=False,
    )
    assert store.status_code == 303
    assert "/edit" in store.headers["location"]
    figure_id = re.search(r"/admin/figures/(\d+)/edit", store.headers["location"]).group(1)

    try:
        edit_page = await admin_client.get(f"/admin/figures/{figure_id}/edit")
        assert edit_page.status_code == 200
        assert "Func Test Figure" in edit_page.text
        assert "Func Heading" in edit_page.text  # content blocks round-tripped
        # the avatar preview <img> only renders when avatar_path was persisted
        assert 'alt="Func Test Figure"' in edit_page.text

        index = await admin_client.get("/admin/figures")
        assert "Func Test Figure" in index.text

        # ── validation failure must preserve every entered content block ──
        token = csrf_token(edit_page.text)
        bad_update = {
            "_token": token,
            "name": "",  # required -> triggers FormValidationError
            "content_blocks[0][type]": "heading",
            "content_blocks[0][text_en]": "Preserved Heading",
            "content_blocks[1][type]": "paragraph",
            "content_blocks[1][text_en]": "Preserved paragraph EN.",
            "content_blocks[1][text_vi]": "Preserved paragraph VI.",
            "_method": "PUT",
        }
        failed = await admin_client.post(
            f"/admin/figures/{figure_id}", data=bad_update, follow_redirects=True
        )
        assert "Preserved Heading" in failed.text
        assert "Preserved paragraph EN." in failed.text
        assert "Preserved paragraph VI." in failed.text
    finally:
        delete_token = csrf_token((await admin_client.get(f"/admin/figures/{figure_id}/edit")).text)
        destroy = await admin_client.post(
            f"/admin/figures/{figure_id}", data={"_token": delete_token, "_method": "DELETE"}
        )
        assert destroy.status_code == 303
        final_index = await admin_client.get("/admin/figures")
        assert "Func Test Figure" not in final_index.text


async def test_story_crud_round_trip(admin_client: AsyncClient) -> None:
    figures_page = await admin_client.get("/admin/figures")
    figure_id_match = re.search(r"/admin/figures/(\d+)/edit", figures_page.text)
    assert figure_id_match is not None, "dev DB has no figures to attach a story to"
    figure_id = figure_id_match.group(1)

    create_page = await admin_client.get(f"/admin/stories/create?figure_id={figure_id}")
    assert create_page.status_code == 200
    token = csrf_token(create_page.text)

    store = await admin_client.post(
        "/admin/stories",
        data={
            "_token": token,
            "figure_id": figure_id,
            "title": "Func Test Story",
            "subtitle": "Func subtitle",
            "content_blocks[0][type]": "paragraph",
            "content_blocks[0][text_en]": "Story EN.",
            "content_blocks[0][text_vi]": "Story VI.",
        },
        follow_redirects=False,
    )
    assert store.status_code == 303

    index = await admin_client.get("/admin/stories")
    assert "Func Test Story" in index.text
    match = re.search(r"Func Test Story.*?/admin/stories/(\d+)/edit", index.text, re.S)
    assert match is not None
    story_id = match.group(1)

    edit_page = await admin_client.get(f"/admin/stories/{story_id}/edit")
    assert edit_page.status_code == 200
    assert "Story EN." in edit_page.text

    delete_token = csrf_token(edit_page.text)
    destroy = await admin_client.post(
        f"/admin/stories/{story_id}", data={"_token": delete_token, "_method": "DELETE"}
    )
    assert destroy.status_code == 303
    final_index = await admin_client.get("/admin/stories")
    assert "Func Test Story" not in final_index.text
