"""Ports `ContactController` + `routes/web.php`'s `admin.contacts.*`
resource group."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from admirable.application.dto.contact_dto import CreateContactCommand, UpdateContactCommand
from admirable.application.use_cases.contacts.create_contact import CreateContact
from admirable.application.use_cases.contacts.delete_contact import DeleteContact
from admirable.application.use_cases.contacts.get_contact import GetContact
from admirable.application.use_cases.contacts.list_contacts import ListContacts, ListContactsQuery
from admirable.application.use_cases.contacts.update_contact import UpdateContact
from admirable.domain.value_objects.pagination import Page
from admirable.presentation.web.dependencies import (
    get_create_contact_uc,
    get_delete_contact_uc,
    get_get_contact_uc,
    get_list_contacts_uc,
    get_session,
    get_update_contact_uc,
    require_auth,
)
from admirable.presentation.web.forms.base import parse_form
from admirable.presentation.web.forms.contact_form import CONTACT_FIELD_LABELS, ContactForm
from admirable.presentation.web.middleware.session import Session
from admirable.presentation.web.routers.resource_helper import register_resource

router = APIRouter(prefix="/admin", dependencies=[Depends(require_auth)])


def _templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates  # type: ignore[no-any-return]


async def _index(
    request: Request, use_case: Annotated[ListContacts, Depends(get_list_contacts_uc)]
) -> object:
    page = int(request.query_params.get("page", 1))
    result = await use_case.execute(ListContactsQuery(page=page, per_page=15))
    contacts = Page(
        items=result.items, total=result.total, page=result.page, per_page=result.per_page
    )
    return _templates(request).TemplateResponse(
        request, "admin/contacts/index.html", {"contacts": contacts}
    )


async def _create(request: Request) -> object:
    return _templates(request).TemplateResponse(request, "admin/contacts/form.html")


async def _store(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[CreateContact, Depends(get_create_contact_uc)],
) -> object:
    form = await parse_form(
        request,
        ContactForm,
        str(request.url_for("admin.contacts.create")),
        CONTACT_FIELD_LABELS,
    )
    await use_case.execute(
        CreateContactCommand(
            type=form.type,
            label=form.label,
            value=form.value,
            icon=form.icon,
            sort_order=form.sort_order,
            is_active=form.is_active,
        )
    )
    session.flash("success", "Thông tin liên hệ đã được tạo thành công.")
    return RedirectResponse(request.url_for("admin.contacts.index"), status_code=303)


async def _edit(
    request: Request, id: int, use_case: Annotated[GetContact, Depends(get_get_contact_uc)]
) -> object:
    contact = await use_case.execute(id)
    return _templates(request).TemplateResponse(
        request, "admin/contacts/form.html", {"contact": contact}
    )


async def _update(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[UpdateContact, Depends(get_update_contact_uc)],
) -> object:
    form = await parse_form(
        request,
        ContactForm,
        str(request.url_for("admin.contacts.edit", id=id)),
        CONTACT_FIELD_LABELS,
    )
    await use_case.execute(
        UpdateContactCommand(
            contact_id=id,
            type=form.type,
            label=form.label,
            value=form.value,
            icon=form.icon,
            sort_order=form.sort_order,
            is_active=form.is_active,
        )
    )
    session.flash("success", "Thông tin liên hệ đã được cập nhật thành công.")
    return RedirectResponse(request.url_for("admin.contacts.index"), status_code=303)


async def _destroy(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[DeleteContact, Depends(get_delete_contact_uc)],
) -> object:
    try:
        await use_case.execute(id)
    except Exception as exc:
        session.flash("error", f"Không thể xóa liên hệ: {exc}")
        return RedirectResponse(request.url_for("admin.contacts.index"), status_code=303)
    session.flash("success", "Thông tin liên hệ đã được xóa thành công.")
    return RedirectResponse(request.url_for("admin.contacts.index"), status_code=303)


register_resource(
    router,
    "/contacts",
    "admin.contacts",
    {
        "index": _index,
        "create": _create,
        "store": _store,
        "edit": _edit,
        "update": _update,
        "destroy": _destroy,
    },
)
