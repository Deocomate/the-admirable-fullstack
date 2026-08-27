"""Ports `SearchController::index` / `client.search`."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates

from admirable.application.use_cases.public.search_figures import (
    SearchFigures,
    SearchFiguresQuery,
)
from admirable.domain.value_objects.pagination import Page
from admirable.infrastructure.container import Container
from admirable.presentation.web.dependencies import get_container, get_search_figures_uc
from admirable.presentation.web.routers.client._context import build_client_context
from admirable.presentation.web.seo import SeoMeta

router = APIRouter(prefix="/tim-kiem")


@router.get("", name="client.search")
async def index(
    request: Request,
    uc: Annotated[SearchFigures, Depends(get_search_figures_uc)],
    container: Annotated[Container, Depends(get_container)],
    q: str = "",
    category: str | None = None,
    page: int = 1,
) -> object:
    data = await uc.execute(
        SearchFiguresQuery(query=q, category_slug=category, page=page, per_page=12)
    )
    templates: Jinja2Templates = request.app.state.templates

    description = (
        f'Kết quả tìm kiếm cho "{q}" trên The Admirable.'
        if q
        else "Tìm kiếm nhân vật và câu chuyện song ngữ trên The Admirable."
    )
    context = await build_client_context(
        request,
        container,
        SeoMeta(
            title="Tìm kiếm — The Admirable",
            description=description,
            canonical_url=str(request.url_for("client.search")),
            robots="noindex,follow",
            keywords="tìm kiếm nhân vật, câu chuyện song ngữ, The Admirable",
            active_page="search",
        ),
    )
    context.update(
        {
            "query": data.query,
            "category_slug": data.category_slug,
            "figures": data.figures,
            "trending_figures": data.trending_figures,
            "page_obj": Page(
                items=data.figures, total=data.total, page=data.page, per_page=data.per_page
            ),
        }
    )
    return templates.TemplateResponse(request, "client/search/index.html", context)
