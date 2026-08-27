"""Ports `CategoryController::index`/`show` — same use case and template for
both, distinguished only by whether a `slug` path param is present, matching
`client/category/index.blade.php`'s own `$category ?? null` branch."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates

from admirable.application.use_cases.public.get_category_page import GetCategoryPage
from admirable.domain.value_objects.pagination import Page
from admirable.infrastructure.container import Container
from admirable.presentation.web.dependencies import get_category_page_uc, get_container
from admirable.presentation.web.routers.client._context import build_client_context
from admirable.presentation.web.seo import SeoMeta

router = APIRouter(prefix="/linh-vuc")


async def _render(
    request: Request,
    uc: GetCategoryPage,
    container: Container,
    slug: str | None,
    page: int,
) -> object:
    data = await uc.execute(slug, page)
    templates: Jinja2Templates = request.app.state.templates

    if data.category is not None:
        title = f"{data.category.name} — The Admirable"
        description = (
            f"Khám phá các nhân vật truyền cảm hứng thuộc lĩnh vực "
            f"{data.category.name} tại The Admirable."
        )
        keywords = f"{data.category.name}, nhân vật truyền cảm hứng, The Admirable"
        canonical = str(request.url_for("client.categories.show", slug=data.category.slug))
    else:
        title = "Lĩnh vực — The Admirable"
        description = (
            "Khám phá các lĩnh vực và những nhân vật truyền cảm hứng nổi bật tại The Admirable."
        )
        keywords = "lĩnh vực, nhân vật truyền cảm hứng, The Admirable"
        canonical = str(request.url_for("client.categories.index"))

    context = await build_client_context(
        request,
        container,
        SeoMeta(
            title=title,
            description=description,
            canonical_url=canonical,
            keywords=keywords,
            active_page="category",
        ),
    )
    context.update(
        {
            "category": data.category,
            "featured_figure": data.featured_figure,
            "figures": data.figures,
            "page_obj": Page(
                items=data.figures, total=data.total, page=data.page, per_page=data.per_page
            ),
        }
    )
    return templates.TemplateResponse(request, "client/category/index.html", context)


@router.get("", name="client.categories.index")
async def index(
    request: Request,
    uc: Annotated[GetCategoryPage, Depends(get_category_page_uc)],
    container: Annotated[Container, Depends(get_container)],
    page: int = 1,
) -> object:
    return await _render(request, uc, container, None, page)


@router.get("/{slug}", name="client.categories.show")
async def show(
    request: Request,
    slug: str,
    uc: Annotated[GetCategoryPage, Depends(get_category_page_uc)],
    container: Annotated[Container, Depends(get_container)],
    page: int = 1,
) -> object:
    return await _render(request, uc, container, slug, page)
