"""Ports `ContactController::index` / `client.contact`."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates

from admirable.application.use_cases.public.get_contact_page import GetContactPage
from admirable.infrastructure.container import Container
from admirable.presentation.web.dependencies import get_contact_page_uc, get_container
from admirable.presentation.web.routers.client._context import build_client_context
from admirable.presentation.web.seo import SeoMeta

router = APIRouter()


@router.get("/lien-he", name="client.contact")
async def index(
    request: Request,
    uc: Annotated[GetContactPage, Depends(get_contact_page_uc)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    data = await uc.execute()
    templates: Jinja2Templates = request.app.state.templates
    context = await build_client_context(
        request,
        container,
        SeoMeta(
            title="Liên hệ — The Admirable",
            description=(
                "Liên hệ với The Admirable — Chúng tôi luôn sẵn sàng lắng nghe và hợp tác cùng bạn."
            ),
            canonical_url=str(request.url_for("client.contact")),
            keywords="liên hệ, contact, The Admirable, xây dựng website, hợp tác",
            active_page="contact",
        ),
    )
    context["page_contacts"] = data.contacts
    return templates.TemplateResponse(request, "client/contact/index.html", context)
