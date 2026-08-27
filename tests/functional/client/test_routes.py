"""Status/template smoke tests for all 8 client routes against real migrated
dev data (see tests/functional/conftest.py) — Phase 9 plan step 11."""

from httpx import AsyncClient

from admirable.domain.entities.story_snippet import StorySnippet


async def test_home_returns_200(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert "The Admirable" in response.text


async def test_categories_index_returns_200(client: AsyncClient) -> None:
    response = await client.get("/linh-vuc")
    assert response.status_code == 200
    assert "Lĩnh vực" in response.text


async def test_categories_show_returns_200_for_real_slug(client: AsyncClient) -> None:
    response = await client.get("/linh-vuc/cong-nghe")
    assert response.status_code == 200
    assert "Công nghệ" in response.text


async def test_categories_show_returns_404_for_missing_slug(client: AsyncClient) -> None:
    response = await client.get("/linh-vuc/khong-ton-tai-abc123")
    assert response.status_code == 404


async def test_figure_show_returns_200_for_real_slug(client: AsyncClient) -> None:
    response = await client.get("/nhan-vat/mark-zuckerberg")
    assert response.status_code == 200
    assert "Mark Zuckerberg" in response.text
    assert "data-audio-player" in response.text  # real figure has audio_path


async def test_figure_show_returns_404_for_missing_slug(client: AsyncClient) -> None:
    response = await client.get("/nhan-vat/khong-ton-tai-abc123")
    assert response.status_code == 404


async def test_story_show_returns_200_for_real_id(client: AsyncClient, story: StorySnippet) -> None:
    response = await client.get(f"/cau-chuyen/{story.id}")
    assert response.status_code == 200
    assert story.title in response.text
    assert story.subtitle is not None
    assert story.subtitle in response.text


async def test_story_show_returns_404_for_missing_id(client: AsyncClient) -> None:
    response = await client.get("/cau-chuyen/999999999")
    assert response.status_code == 404


async def test_search_returns_200(client: AsyncClient) -> None:
    response = await client.get("/tim-kiem")
    assert response.status_code == 200
    assert "Tìm kiếm" in response.text


async def test_about_us_returns_200(client: AsyncClient) -> None:
    response = await client.get("/ve-chung-toi")
    assert response.status_code == 200


async def test_contact_returns_200(client: AsyncClient) -> None:
    response = await client.get("/lien-he")
    assert response.status_code == 200
    assert "Liên hệ" in response.text
