"""Renders each layout end-to-end and checks structural markers (navbar,
footer, sidebar, csrf-token meta) plus the full seo-head tag list."""

from collections.abc import Callable

from starlette.requests import Request
from starlette.templating import Jinja2Templates

from admirable.presentation.web.seo import SeoMeta, build_seo_context

_REQUIRED_SEO_TAGS = (
    "<title>",
    '<meta name="description"',
    '<meta name="robots"',
    '<link rel="canonical"',
    'property="og:locale"',
    'property="og:type"',
    'property="og:site_name"',
    'property="og:title"',
    'property="og:description"',
    'property="og:url"',
    'property="og:image"',
    'name="twitter:card"',
    'name="twitter:title"',
    'name="twitter:description"',
    'name="twitter:image"',
    "application/ld+json",
    '<link rel="icon"',
    '<link rel="shortcut icon"',
)


def _client_context(make_request: Callable[..., Request], path: str = "/") -> dict[str, object]:
    request = make_request(path)
    ctx = build_seo_context(request, SeoMeta(active_page="home"))
    ctx["request"] = request
    ctx["categories"] = [{"name": "Khoa học", "slug": "khoa-hoc"}]
    ctx["contacts"] = [{"type": "email", "value": "hi@example.com", "label": "Email"}]
    return ctx


def test_client_layout_renders_full_seo_head(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    html = templates.get_template("layouts/client.html").render(_client_context(make_request))
    for tag in _REQUIRED_SEO_TAGS:
        assert tag in html, f"missing {tag!r} in rendered client layout head"


def test_client_layout_renders_navbar_footer_back_to_top(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    html = templates.get_template("layouts/client.html").render(_client_context(make_request))
    assert 'id="main-navbar"' in html
    assert "<footer" in html
    assert 'id="back-to-top"' in html
    assert "Khoa học" in html  # footer category list


def test_client_layout_navbar_marks_active_page(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    html = templates.get_template("layouts/client.html").render(_client_context(make_request))
    assert "text-apple-black" in html


def test_admin_layout_has_csrf_meta_and_sidebar(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    request = make_request("/")
    html = templates.get_template("layouts/admin.html").render(request=request)
    assert '<meta name="csrf-token"' in html
    assert "bg-[#0f0f13]" in html  # sidebar
    assert "Tổng quan" in html


def test_admin_layout_shows_breadcrumb_when_provided(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    request = make_request("/")
    breadcrumb = "Admin › Lĩnh vực"  # noqa: RUF001 — real separator used in admin breadcrumbs
    html = templates.get_template("layouts/admin.html").render(
        request=request, breadcrumb=breadcrumb
    )
    assert breadcrumb in html


def test_admin_auth_layout_has_csrf_meta(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    request = make_request("/")
    html = templates.get_template("layouts/admin_auth.html").render(request=request)
    assert '<meta name="csrf-token"' in html
    assert "Admin Admirable.site" in html


def test_error_403_renders(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    request = make_request("/")
    html = templates.get_template("errors/403.html").render(request=request)
    assert "403" in html
    assert "Không có quyền truy cập" in html
