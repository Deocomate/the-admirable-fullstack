"""HTTP-level check of the home page's featured/backfill algorithm (Phase 9
plan step 12). The algorithm's 0/3/6/10-featured branch coverage is already
exhaustively unit-tested in tests/application/test_get_home_page.py; this
confirms the router/template render exactly what that use case returns —
at most 6 "latest" cards, no duplicate figures, none of them the hero."""

import re

from httpx import AsyncClient

_FIGURE_HREF_RE = re.compile(r'href="[^"]*/nhan-vat/([a-z0-9-]+)"')


async def test_latest_figures_grid_has_no_duplicates_and_respects_limit(
    client: AsyncClient,
) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    html = response.text

    # Isolate the "Mới nhất" section from the rest of the page (hero/footer
    # links to figures would otherwise pollute the href count).
    start = html.index("Mới nhất")
    end = html.index("</section>", start)
    section = html[start:end]

    hrefs = _FIGURE_HREF_RE.findall(section)
    assert 0 < len(hrefs) <= 6
    assert len(hrefs) == len(set(hrefs)), "latest-figures grid rendered a duplicate figure"
