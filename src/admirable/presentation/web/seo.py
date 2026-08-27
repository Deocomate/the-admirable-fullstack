"""SEO metadata computation and JSON-LD schema builder."""

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
    """True for an absolute URL or root-relative path produced by asset/media helpers."""
    if value.startswith("/"):
        return True
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def build_seo_context(request: Request, meta: SeoMeta) -> dict[str, Any]:
    """Computes SEO canonical URLs, OG images, and prepends default Schema.org JSON-LD."""
    settings: Settings = request.app.state.settings
    site_name = settings.app.name

    seo_canonical = meta.canonical_url or str(request.url.replace(query=""))

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
