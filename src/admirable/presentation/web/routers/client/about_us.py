"""Ports `AboutUsController::index` / `client.about-us`."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates

from admirable.application.use_cases.public.get_about_us_page import GetAboutUsPage
from admirable.infrastructure.container import Container
from admirable.presentation.web.dependencies import get_about_us_page_uc, get_container
from admirable.presentation.web.routers.client._context import build_client_context
from admirable.presentation.web.seo import SeoMeta

router = APIRouter()


@router.get("/ve-chung-toi", name="client.about-us")
async def index(
    request: Request,
    uc: Annotated[GetAboutUsPage, Depends(get_about_us_page_uc)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    data = await uc.execute()
    templates: Jinja2Templates = request.app.state.templates
    context = await build_client_context(
        request,
        container,
        SeoMeta(
            title="Về chúng tôi — The Admirable",
            description=(
                "The Admirable là nền tảng học tiếng Anh truyền cảm hứng qua những câu "
                "chuyện về các nhân vật vĩ đại."
            ),
            canonical_url=str(request.url_for("client.about-us")),
            keywords="về chúng tôi, The Admirable, học tiếng anh truyền cảm hứng",
            active_page="about-us",
        ),
    )
    context["about_us"] = data.data
    return templates.TemplateResponse(request, "client/about-us/index.html", context)
