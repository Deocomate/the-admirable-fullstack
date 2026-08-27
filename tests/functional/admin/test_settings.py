"""About Us settings: saving reflects both on the editor and on the real
public `/ve-chung-toi` page — the plan's explicit acceptance criterion.

The form always round-trips every field (a real browser submits the whole
pre-filled form, not just the edited inputs — `UpdateAboutUs` saves the POST
body verbatim with no merge-against-existing-data step). This test captures
the live dev DB's current values via BeautifulSoup before mutating anything
and restores them afterward, so it leaves no residue on real seeded content."""

from bs4 import BeautifulSoup
from httpx import AsyncClient

from tests.functional.admin.conftest import csrf_token


def _capture_form_fields(html: str) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form")
    fields: dict[str, str] = {}
    for tag in form.find_all(["input", "textarea"]):
        name = tag.get("name")
        if not name or name == "_token":
            continue
        fields[name] = tag.get_text() if tag.name == "textarea" else (tag.get("value") or "")
    return fields


async def test_about_us_save_reflects_on_public_page(admin_client: AsyncClient) -> None:
    page = await admin_client.get("/admin/settings/about-us")
    assert page.status_code == 200
    original_fields = _capture_form_fields(page.text)
    token = csrf_token(page.text)

    marker = "Func Test Tagline Marker"
    edited_fields = dict(original_fields)
    edited_fields["hero[tagline]"] = marker
    edited_fields["_token"] = token

    try:
        submit = await admin_client.post("/admin/settings/about-us", data=edited_fields)
        assert submit.status_code == 303

        editor = await admin_client.get("/admin/settings/about-us")
        assert marker in editor.text

        public_page = await admin_client.get("/ve-chung-toi")
        assert public_page.status_code == 200
        assert marker in public_page.text
    finally:
        restore_page = await admin_client.get("/admin/settings/about-us")
        restore_token = csrf_token(restore_page.text)
        restore_fields = dict(original_fields)
        restore_fields["_token"] = restore_token
        restore = await admin_client.post("/admin/settings/about-us", data=restore_fields)
        assert restore.status_code == 303
        final = await admin_client.get("/admin/settings/about-us")
        assert marker not in final.text
