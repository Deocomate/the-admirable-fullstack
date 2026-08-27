"""SEO metadata computation, moved out of the Blade `@php` block
(`components/client/layout/app.blade.php:17-41`) into pure Python so the
template only renders — it never computes."""

from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

from starlette.requests import Request

from admirable.config import Settings
from admirable.presentation.web.templating import asset_url


@dataclass(frozen=True)
class SeoMeta:
    title: str = "The Admirable — Những tấm gương đáng ngưỡng mộ"
    description: str = (
        "Khám phá những câu chuyện truyền cảm hứng từ các nhân vật nổi tiếng trên "
        "thế giới. Luyện IELTS qua bài đọc song ngữ, audio và video."
    )
    active_page: str = ""
    canonical_url: str | None = None
    og_type: str = "website"
    og_image: str | None = None
    robots: str = "index,follow"
    keywords: str | None = None
    published_time: str | None = None
    modified_time: str | None = None
    article_section: str | None = None
    article_tags: tuple[str, ...] = ()
    json_ld: tuple[dict[str, Any], ...] = field(default_factory=tuple)


def _is_already_resolved(value: str) -> bool:
    """True for an absolute external URL, or a root-relative path already
    produced by `asset_url()`/`media_url()` (e.g. a figure's avatar via
    `media_url(figure.avatar_path)`) — either way, wrapping it again through
    `asset_url()` would be wrong. Only a bare relative path with no leading
    slash (Blade's `ltrim($seoImage, '/')` fallback case) still gets wrapped.
    """
    if value.startswith("/"):
        return True
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def build_seo_context(request: Request, meta: SeoMeta) -> dict[str, Any]:
    """Reproduces `app.blade.php`'s three computed values exactly:
    `seo_canonical`, `seo_image` (wrapped through `asset()` only when not
    already an absolute URL — the `FILTER_VALIDATE_URL` branch), and
    `seo_locale`. Then prepends the default `WebSite`/`SearchAction` schema
    to the page's own `json_ld`, matching `array_merge([$default], $jsonLd)`.
    """
    settings: Settings = request.app.state.settings
    site_name = settings.app.name

    seo_canonical = meta.canonical_url or str(request.url.replace(query=""))

    # Laravel's asset() returns a fully-qualified absolute URL, so the
    # default logo path short-circuits the FILTER_VALIDATE_URL branch below.
    # Our asset_url() is root-relative instead, so the default must be used
    # as-is here rather than run through the "wrap if not absolute" check —
    # otherwise it gets asset_url()-wrapped twice.
    if meta.og_image is None:
        seo_image = asset_url("assets/images/logo.png")
    elif _is_already_resolved(meta.og_image):
        seo_image = meta.og_image
    else:
        seo_image = asset_url(meta.og_image)

    seo_locale = settings.app.locale.replace("_", "-")

    default_json_ld: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site_name,
        "url": settings.app.base_url + "/",
        "inLanguage": "vi",
        "potentialAction": {
            "@type": "SearchAction",
            "target": str(request.url_for("client.search")) + "?q={search_term_string}",
            "query-input": "required name=search_term_string",
        },
    }
    json_ld_scripts = [default_json_ld, *meta.json_ld]

    return {
        "seo": meta,
        "site_name": site_name,
        "seo_canonical": seo_canonical,
        "seo_image": seo_image,
        "seo_locale": seo_locale,
        "json_ld_scripts": json_ld_scripts,
    }
