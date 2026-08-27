"""build_seo_context reproduces app.blade.php's three computed values exactly
(seo_canonical / seo_image / seo_locale) plus the WebSite JSON-LD merge order.
The 4 og:image scenarios are the plan's explicit required test matrix."""

from collections.abc import Callable
from typing import Any

from starlette.requests import Request

from admirable.presentation.web.seo import SeoMeta, build_seo_context


def _ctx(make_request: Callable[..., Request], meta: SeoMeta, path: str = "/") -> dict[str, Any]:
    request = make_request(path)
    request.scope["app"].state.settings.app.locale = "en"
    return build_seo_context(request, meta)


def test_default_canonical_uses_current_url(make_request: Callable[..., Request]) -> None:
    ctx = _ctx(make_request, SeoMeta(), path="/some/page")
    assert ctx["seo_canonical"] == "http://test/some/page"


def test_custom_canonical_url_overrides_current_url(make_request: Callable[..., Request]) -> None:
    ctx = _ctx(make_request, SeoMeta(canonical_url="https://example.com/custom"), path="/x")
    assert ctx["seo_canonical"] == "https://example.com/custom"


def test_relative_og_image_wrapped_through_asset(make_request: Callable[..., Request]) -> None:
    ctx = _ctx(make_request, SeoMeta(og_image="assets/images/custom.png"))
    assert ctx["seo_image"] == "/static/assets/images/custom.png"


def test_default_og_image_falls_back_to_logo(make_request: Callable[..., Request]) -> None:
    ctx = _ctx(make_request, SeoMeta())
    assert ctx["seo_image"] == "/static/assets/images/logo.png"


def test_absolute_og_image_url_is_not_wrapped(make_request: Callable[..., Request]) -> None:
    ctx = _ctx(make_request, SeoMeta(og_image="https://cdn.example.com/pic.jpg"))
    assert ctx["seo_image"] == "https://cdn.example.com/pic.jpg"


def test_locale_underscore_replaced_with_hyphen(make_request: Callable[..., Request]) -> None:
    request = make_request("/")
    request.scope["app"].state.settings.app.locale = "vi_VN"
    ctx = build_seo_context(request, SeoMeta())
    assert ctx["seo_locale"] == "vi-VN"


def test_default_json_ld_prepended_before_page_json_ld(
    make_request: Callable[..., Request],
) -> None:
    page_schema = {"@context": "https://schema.org", "@type": "Article", "headline": "x"}
    ctx = _ctx(make_request, SeoMeta(json_ld=(page_schema,)))
    scripts = ctx["json_ld_scripts"]
    assert len(scripts) == 2
    assert scripts[0]["@type"] == "WebSite"
    assert scripts[0]["potentialAction"]["@type"] == "SearchAction"
    assert scripts[1] is page_schema


def test_default_json_ld_search_action_targets_search_route(
    make_request: Callable[..., Request],
) -> None:
    ctx = _ctx(make_request, SeoMeta())
    target = ctx["json_ld_scripts"][0]["potentialAction"]["target"]
    assert target.endswith("?q={search_term_string}")
    assert "/_test/client.search" in target
