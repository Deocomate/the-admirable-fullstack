"""SEO tag + JSON-LD coverage for all 8 client routes (Phase 9 plan step 14):
`<title>`, description, canonical, `og:*`, `twitter:*`, >=1 parseable
JSON-LD block; figure/story additionally carry `article:*`."""

import json
import re

import pytest
from httpx import AsyncClient

from admirable.domain.entities.story_snippet import StorySnippet

_JSON_LD_RE = re.compile(r'application/ld\+json">(.*?)</script>', re.S)


def _assert_common_seo(html: str) -> None:
    assert re.search(r"<title>[^<]+</title>", html)
    assert 'name="description" content="' in html
    assert 'rel="canonical" href="' in html
    for tag in ("og:title", "og:description", "og:type", "og:url", "og:site_name"):
        assert f'property="{tag}" content="' in html, f"missing {tag}"
    for tag in ("twitter:card", "twitter:title", "twitter:description"):
        assert f'name="{tag}" content="' in html, f"missing {tag}"

    blocks = _JSON_LD_RE.findall(html)
    assert blocks, "no JSON-LD block found"
    for block in blocks:
        json.loads(block)  # raises if invalid


def _assert_article_tags(html: str) -> None:
    assert 'property="og:type" content="article"' in html
    assert 'property="article:section" content="' in html


def _assert_no_article_tags(html: str) -> None:
    assert "article:published_time" not in html
    assert "article:section" not in html


@pytest.mark.parametrize(
    "path",
    ["/", "/linh-vuc", "/linh-vuc/cong-nghe", "/tim-kiem", "/ve-chung-toi", "/lien-he"],
)
async def test_website_pages_carry_full_seo_and_no_article_tags(
    client: AsyncClient, path: str
) -> None:
    response = await client.get(path)
    assert response.status_code == 200
    _assert_common_seo(response.text)
    _assert_no_article_tags(response.text)


async def test_figure_show_carries_article_seo(client: AsyncClient) -> None:
    response = await client.get("/nhan-vat/mark-zuckerberg")
    assert response.status_code == 200
    html = response.text
    _assert_common_seo(html)
    _assert_article_tags(html)
    assert "Mark Zuckerberg" in html


async def test_story_show_carries_article_seo(client: AsyncClient, story: StorySnippet) -> None:
    response = await client.get(f"/cau-chuyen/{story.id}")
    assert response.status_code == 200
    html = response.text
    _assert_common_seo(html)
    _assert_article_tags(html)
    assert story.title in html
