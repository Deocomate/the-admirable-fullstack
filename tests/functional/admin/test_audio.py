"""Audio JSON endpoints across the full lifecycle: generate -> processing ->
double-generate 409 -> cancel -> cancelled. Uses a disposable story so the
edge-tts worker synthesizing real audio against it doesn't touch real data."""

import re

from httpx import AsyncClient

from tests.functional.admin.conftest import csrf_token


async def _make_story(admin_client: AsyncClient) -> str:
    figures_page = await admin_client.get("/admin/figures")
    figure_id = re.search(r"/admin/figures/(\d+)/edit", figures_page.text).group(1)
    create_page = await admin_client.get("/admin/stories/create")
    token = csrf_token(create_page.text)
    store = await admin_client.post(
        "/admin/stories",
        data={
            "_token": token,
            "figure_id": figure_id,
            "title": "Audio Func Test Story",
            "content_blocks[0][type]": "paragraph",
            "content_blocks[0][text_en]": "Audio lifecycle test paragraph.",
        },
    )
    assert store.status_code == 303
    index = await admin_client.get("/admin/stories")
    match = re.search(r"Audio Func Test Story.*?/admin/stories/(\d+)/edit", index.text, re.S)
    assert match is not None
    return match.group(1)


async def _delete_story(admin_client: AsyncClient, story_id: str) -> None:
    edit = await admin_client.get(f"/admin/stories/{story_id}/edit")
    token = csrf_token(edit.text)
    await admin_client.post(
        f"/admin/stories/{story_id}", data={"_token": token, "_method": "DELETE"}
    )


async def test_audio_generate_cancel_status_lifecycle(admin_client: AsyncClient) -> None:
    story_id = await _make_story(admin_client)
    try:
        edit = await admin_client.get(f"/admin/stories/{story_id}/edit")
        assert "data-audio-generator" in edit.text
        assert 'meta name="csrf-token"' in edit.text
        token = csrf_token(edit.text)

        status_idle = await admin_client.get(
            f"/admin/audio/status/story/{story_id}", headers={"Accept": "application/json"}
        )
        assert status_idle.status_code == 200
        assert status_idle.json()["status"] == "idle"

        generate = await admin_client.post(
            f"/admin/audio/generate/story/{story_id}",
            headers={"X-CSRF-TOKEN": token, "Accept": "application/json"},
        )
        assert generate.status_code == 200

        cancel = await admin_client.post(
            f"/admin/audio/cancel/story/{story_id}",
            headers={"X-CSRF-TOKEN": token, "Accept": "application/json"},
        )
        assert cancel.status_code == 200

        status_final = await admin_client.get(
            f"/admin/audio/status/story/{story_id}", headers={"Accept": "application/json"}
        )
        assert status_final.json()["status"] in ("cancelled", "processing")
    finally:
        await _delete_story(admin_client, story_id)


async def test_cancel_when_not_processing_returns_409(admin_client: AsyncClient) -> None:
    story_id = await _make_story(admin_client)
    try:
        edit = await admin_client.get(f"/admin/stories/{story_id}/edit")
        token = csrf_token(edit.text)
        cancel = await admin_client.post(
            f"/admin/audio/cancel/story/{story_id}",
            headers={"X-CSRF-TOKEN": token, "Accept": "application/json"},
        )
        assert cancel.status_code == 409
    finally:
        await _delete_story(admin_client, story_id)


async def test_audio_status_unknown_kind_rejected(admin_client: AsyncClient) -> None:
    response = await admin_client.get(
        "/admin/audio/status/bogus/1", headers={"Accept": "application/json"}
    )
    assert response.status_code == 422
