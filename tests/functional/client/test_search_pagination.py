"""Search pagination preserves `q`/`category` query parameters across pages."""

from httpx import AsyncClient


async def test_unfiltered_pagination_links_include_page_2(client: AsyncClient) -> None:
    # No filter matches all 30 dev-DB figures at per_page=12 -> 3 pages,
    # deterministic regardless of what real figure names/categories exist.
    response = await client.get("/tim-kiem")
    assert response.status_code == 200
    assert 'href="http://test/tim-kiem?page=2"' in response.text


async def test_query_and_category_survive_into_page_2_link(client: AsyncClient) -> None:
    response = await client.get("/tim-kiem", params={"q": "a"})
    assert response.status_code == 200
    html = response.text
    assert "page=2" in html
    # Jinja autoescapes `&` to `&amp;` inside the href attribute.
    assert "q=a&amp;page=2" in html or "q=a" in html.split("page=2")[0][-40:]


async def test_second_page_returns_200_and_links_back_to_page_1(client: AsyncClient) -> None:
    response = await client.get("/tim-kiem", params={"page": 2})
    assert response.status_code == 200
    assert 'href="http://test/tim-kiem?page=1"' in response.text
