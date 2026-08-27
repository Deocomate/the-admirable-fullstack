"""Ports `FigureController::show` / `client.figures.show`."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates

from admirable.application.use_cases.public.get_figure_detail import GetFigureDetail
from admirable.infrastructure.container import Container
from admirable.presentation.web.dependencies import get_container, get_figure_detail_uc
from admirable.presentation.web.routers.client._context import build_client_context
from admirable.presentation.web.seo import SeoMeta
from admirable.presentation.web.templating import media_url

router = APIRouter(prefix="/nhan-vat")


@router.get("/{slug}", name="client.figures.show")
async def show(
    request: Request,
    slug: str,
    uc: Annotated[GetFigureDetail, Depends(get_figure_detail_uc)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    figure = await uc.execute(slug)
    templates: Jinja2Templates = request.app.state.templates
    settings = request.app.state.settings

    first_category = figure.category_names[0] if figure.category_names else None
    context = await build_client_context(
        request,
        container,
        SeoMeta(
            title=f"{figure.name} — The Admirable",
            description=figure.short_description or "",
            canonical_url=str(request.url_for("client.figures.show", slug=figure.slug)),
            og_type="article",
            og_image=media_url(figure.avatar_path, settings.media.url_prefix),
            published_time=figure.created_at.isoformat() if figure.created_at else None,
            modified_time=figure.updated_at.isoformat() if figure.updated_at else None,
            article_section=first_category,
            article_tags=tuple(figure.category_names),
            keywords=f"{figure.name}, nhân vật truyền cảm hứng, The Admirable",
        ),
    )
    context["figure"] = figure
    return templates.TemplateResponse(request, "client/figure/show.html", context)
