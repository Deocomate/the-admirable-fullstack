"""Ports `UserController` + `routes/web.php`'s `admin.users.*` group —
superadmin-only (`Route::middleware('role:superadmin')`)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from admirable.application.dto.auth_dto import AuthenticatedUserDTO
from admirable.application.dto.user_dto import CreateUserCommand, UpdateUserCommand
from admirable.application.use_cases.users.create_user import CreateUser
from admirable.application.use_cases.users.delete_user import DeleteUser
from admirable.application.use_cases.users.get_user import GetUser
from admirable.application.use_cases.users.list_users import ListUsers
from admirable.application.use_cases.users.update_user import UpdateUser
from admirable.domain.entities.user import User as UserEntity
from admirable.domain.exceptions import DuplicateValueError
from admirable.domain.value_objects.pagination import Page
from admirable.domain.value_objects.role import Role
from admirable.presentation.web.dependencies import (
    get_create_user_uc,
    get_delete_user_uc,
    get_get_user_uc,
    get_list_users_uc,
    get_session,
    get_update_user_uc,
    require_auth,
    require_role,
)
from admirable.presentation.web.exceptions import FormValidationError
from admirable.presentation.web.forms.base import parse_form
from admirable.presentation.web.forms.user_form import (
    USER_FIELD_LABELS,
    CreateUserForm,
    UpdateUserForm,
)
from admirable.presentation.web.middleware.session import Session
from admirable.presentation.web.routers.resource_helper import register_resource

router = APIRouter(prefix="/admin", dependencies=[require_role(Role.SUPERADMIN)])


def _templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates  # type: ignore[no-any-return]


async def _index(
    request: Request, use_case: Annotated[ListUsers, Depends(get_list_users_uc)]
) -> object:
    page = int(request.query_params.get("page", 1))
    result = await use_case.execute(page=page, per_page=15)
    users = Page(items=result.items, total=result.total, page=result.page, per_page=result.per_page)
    return _templates(request).TemplateResponse(request, "admin/users/index.html", {"users": users})


async def _create(request: Request) -> object:
    return _templates(request).TemplateResponse(request, "admin/users/create.html")


async def _store(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[CreateUser, Depends(get_create_user_uc)],
) -> object:
    redirect_to = str(request.url_for("admin.users.create"))
    form = await parse_form(request, CreateUserForm, redirect_to, USER_FIELD_LABELS)
    if form.password != form.password_confirmation:
        raise FormValidationError(
            {"password_confirmation": ["Xác nhận mật khẩu không khớp."]},
            {"name": form.name, "email": form.email},
            redirect_to,
        )
    try:
        await use_case.execute(
            CreateUserCommand(name=form.name, email=form.email, password=form.password)
        )
    except DuplicateValueError:
        raise FormValidationError(
            {"email": ["Email này đã được sử dụng."]},
            {"name": form.name, "email": form.email},
            redirect_to,
        ) from None
    session.flash("success", "Tài khoản admin đã được tạo thành công.")
    return RedirectResponse(request.url_for("admin.users.index"), status_code=303)


async def _edit(
    request: Request, id: int, use_case: Annotated[GetUser, Depends(get_get_user_uc)]
) -> object:
    user = await use_case.execute(id)
    return _templates(request).TemplateResponse(request, "admin/users/edit.html", {"user": user})


async def _update(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[UpdateUser, Depends(get_update_user_uc)],
) -> object:
    redirect_to = str(request.url_for("admin.users.edit", id=id))
    form = await parse_form(request, UpdateUserForm, redirect_to, USER_FIELD_LABELS)
    old_input: dict[str, object] = {"name": form.name, "email": form.email}

    if form.password:
        if len(form.password) < 8:
            raise FormValidationError(
                {"password": ["Mật khẩu phải có ít nhất 8 ký tự."]}, old_input, redirect_to
            )
        if form.password != form.password_confirmation:
            raise FormValidationError(
                {"password_confirmation": ["Xác nhận mật khẩu không khớp."]}, old_input, redirect_to
            )

    try:
        await use_case.execute(
            UpdateUserCommand(
                user_id=id, name=form.name, email=form.email, password=form.password or None
            )
        )
    except DuplicateValueError:
        raise FormValidationError(
            {"email": ["Email này đã được sử dụng."]}, old_input, redirect_to
        ) from None
    session.flash("success", "Thông tin tài khoản đã được cập nhật.")
    return RedirectResponse(request.url_for("admin.users.index"), status_code=303)


async def _destroy(
    request: Request,
    id: int,
    actor: Annotated[AuthenticatedUserDTO, Depends(require_auth)],
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[DeleteUser, Depends(get_delete_user_uc)],
) -> object:
    actor_entity = UserEntity(
        id=actor.id, name=actor.name, email=actor.email, password_hash="", role=actor.role
    )
    try:
        await use_case.execute(id, actor=actor_entity)
    except Exception as exc:
        session.flash("error", str(exc))
        return RedirectResponse(request.url_for("admin.users.index"), status_code=303)
    session.flash("success", "Tài khoản đã bị xóa thành công.")
    return RedirectResponse(request.url_for("admin.users.index"), status_code=303)


register_resource(
    router,
    "/users",
    "admin.users",
    {
        "index": _index,
        "create": _create,
        "store": _store,
        "edit": _edit,
        "update": _update,
        "destroy": _destroy,
    },
)
