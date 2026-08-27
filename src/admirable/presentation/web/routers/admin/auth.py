"""Ports `AuthController` + `routes/web.php`'s admin.auth.* group.

Two routers, matching Laravel's `guest` vs `auth` middleware groups exactly:
`guest_router` (login/forgot/reset) rejects already-logged-in users,
`auth_router` (dashboard/logout) requires a session.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from admirable.application.dto.auth_dto import (
    AuthenticatedUserDTO,
    LoginCommand,
    RequestPasswordResetCommand,
    ResetPasswordCommand,
)
from admirable.application.use_cases.admin.get_dashboard import GetDashboard
from admirable.application.use_cases.auth.login import InvalidCredentialsError, Login
from admirable.application.use_cases.auth.request_password_reset import RequestPasswordReset
from admirable.application.use_cases.auth.reset_password import (
    InvalidResetTokenError,
    ResetPassword,
)
from admirable.presentation.web.dependencies import (
    get_dashboard_uc,
    get_login_use_case,
    get_request_password_reset_use_case,
    get_reset_password_use_case,
    get_session,
    require_auth,
    require_guest,
)
from admirable.presentation.web.forms.base import parse_form
from admirable.presentation.web.middleware.session import Session

_REMEMBER_TTL_SECONDS = 30 * 24 * 3600

guest_router = APIRouter(prefix="/admin", dependencies=[Depends(require_guest)])
auth_router = APIRouter(prefix="/admin", dependencies=[Depends(require_auth)])


def _templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates  # type: ignore[no-any-return]


class LoginForm(BaseModel):
    email: str
    password: str
    remember: bool = False


@guest_router.get("/login", name="admin.auth.login")
async def show_login(request: Request) -> object:
    return _templates(request).TemplateResponse(request, "admin/auth/login.html")


@guest_router.post("/login", name="admin.auth.login.submit")
async def login(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[Login, Depends(get_login_use_case)],
) -> object:
    redirect_to = str(request.url_for("admin.auth.login"))
    form = await parse_form(request, LoginForm, redirect_to=redirect_to)

    try:
        user = await use_case.execute(LoginCommand(email=form.email, password=form.password))
    except InvalidCredentialsError:
        session.set_old_and_errors(
            {"email": form.email, "remember": form.remember},
            {"email": ["Email hoặc mật khẩu không đúng."]},
        )
        return RedirectResponse(request.url_for("admin.auth.login"), status_code=303)

    session.regenerate()
    session["user_id"] = user.id
    if form.remember:
        session.remember_for(_REMEMBER_TTL_SECONDS)
    session.flash("success", "Đăng nhập thành công. Chào mừng bạn!")
    return RedirectResponse(request.url_for("admin.dashboard"), status_code=303)


@guest_router.get("/forgot-password", name="admin.auth.forgot-password")
async def show_forgot_password(request: Request) -> object:
    return _templates(request).TemplateResponse(request, "admin/auth/forgot-password.html")


class ForgotPasswordForm(BaseModel):
    email: str


@guest_router.post("/forgot-password", name="admin.auth.forgot-password.submit")
async def forgot_password(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[RequestPasswordReset, Depends(get_request_password_reset_use_case)],
) -> object:
    form = await parse_form(
        request, ForgotPasswordForm, redirect_to=str(request.url_for("admin.auth.forgot-password"))
    )
    await use_case.execute(RequestPasswordResetCommand(email=form.email))
    session.flash("success", "Chúng tôi đã gửi link đặt lại mật khẩu vào email của bạn.")
    return RedirectResponse(request.url_for("admin.auth.forgot-password"), status_code=303)


@guest_router.get("/reset-password/{token}", name="admin.auth.reset-password")
async def show_reset_password(request: Request, token: str) -> object:
    email = request.query_params.get("email", "")
    return _templates(request).TemplateResponse(
        request, "admin/auth/reset.html", {"token": token, "email": email}
    )


class ResetPasswordForm(BaseModel):
    token: str
    email: str
    password: str
    password_confirmation: str


@guest_router.post("/reset-password", name="admin.auth.reset-password.submit")
async def reset_password(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[ResetPassword, Depends(get_reset_password_use_case)],
) -> object:
    form = await parse_form(
        request, ResetPasswordForm, redirect_to=str(request.url_for("admin.auth.login"))
    )

    if form.password != form.password_confirmation:
        session.set_old_and_errors(
            {"email": form.email},
            {"password": ["Xác nhận mật khẩu không khớp."]},
        )
        return RedirectResponse(
            request.url_for("admin.auth.reset-password", token=form.token), status_code=303
        )

    try:
        await use_case.execute(
            ResetPasswordCommand(token=form.token, email=form.email, password=form.password)
        )
    except InvalidResetTokenError:
        session.set_old_and_errors(
            {"email": form.email},
            {"email": ["Đường dẫn đặt lại mật khẩu không hợp lệ hoặc đã hết hạn."]},
        )
        return RedirectResponse(
            request.url_for("admin.auth.reset-password", token=form.token), status_code=303
        )

    session.flash("success", "Mật khẩu đã được đặt lại thành công. Vui lòng đăng nhập.")
    return RedirectResponse(request.url_for("admin.auth.login"), status_code=303)


@auth_router.get("/", name="admin.home")
async def admin_home(request: Request) -> object:
    return RedirectResponse(request.url_for("admin.dashboard"), status_code=303)


@auth_router.get("/dashboard", name="admin.dashboard")
async def dashboard(
    request: Request,
    user: Annotated[AuthenticatedUserDTO, Depends(require_auth)],
    use_case: Annotated[GetDashboard, Depends(get_dashboard_uc)],
) -> object:
    stats = await use_case.execute()
    return _templates(request).TemplateResponse(request, "admin/dashboard.html", {"stats": stats})


@auth_router.post("/logout", name="admin.auth.logout")
async def logout(request: Request, session: Annotated[Session, Depends(get_session)]) -> object:
    session.invalidate()
    return RedirectResponse(request.url_for("admin.auth.login"), status_code=303)
