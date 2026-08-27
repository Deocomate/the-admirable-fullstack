"""Ports `HomeController::index` / `routes/web.php`'s `client.home`."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates

from admirable.application.use_cases.public.get_home_page import GetHomePage
from admirable.infrastructure.container import Container
from admirable.presentation.web.dependencies import get_container, get_home_page_uc
from admirable.presentation.web.routers.client._context import build_client_context
from admirable.presentation.web.seo import SeoMeta

router = APIRouter()


@router.get("/", name="client.home")
async def index(
    request: Request,
    uc: Annotated[GetHomePage, Depends(get_home_page_uc)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    data = await uc.execute()
    templates: Jinja2Templates = request.app.state.templates
    context = await build_client_context(
        request,
        container,
        SeoMeta(
            title="The Admirable — Những tấm gương đáng ngưỡng mộ",
            description=(
                "Khám phá những câu chuyện truyền cảm hứng từ các nhân vật nổi tiếng trên "
                "thế giới. Luyện IELTS qua bài đọc song ngữ, audio và video."
            ),
            active_page="home",
            keywords="nhân vật truyền cảm hứng, học tiếng anh, luyện IELTS, câu chuyện song ngữ",
        ),
    )
    context.update(
        {
            "featured_figure": data.featured_figure,
            "latest_figures": data.latest_figures,
            "stats": data.stats,
        }
    )
    return templates.TemplateResponse(request, "client/home/index.html", context)
