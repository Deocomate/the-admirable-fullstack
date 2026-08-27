"""Shared client-page context builder: SEO dict + the footer's categories/
contacts. Every client page needs this since layouts/client.html's footer is
included unconditionally — computed explicitly here (per router call, not a
hidden template global) since footer.blade.php's own inline DB query is
exactly the hidden-dependency pattern Phase 8 deliberately did not replicate.
"""

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
