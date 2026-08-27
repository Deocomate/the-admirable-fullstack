"""Shared client-page context builder: builds SEO metadata and loads
categories/contacts for page layout."""

from typing import Any

from starlette.requests import Request

from admirable.infrastructure.container import Container
from admirable.presentation.web.seo import SeoMeta, build_seo_context


async def build_client_context(
    request: Request, container: Container, meta: SeoMeta
) -> dict[str, Any]:
    ctx = build_seo_context(request, meta)
    ctx["categories"] = [
        {"name": c.name, "slug": c.slug} for c in await container.categories.list_all()
    ]
    ctx["contacts"] = [
        {"type": c.type, "value": c.value, "label": c.label}
        for c in await container.contacts.list_active_ordered()
    ]
    return ctx
