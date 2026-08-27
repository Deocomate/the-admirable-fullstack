"""Ports `SettingController` + `routes/web.php`'s `admin.settings.about-us*`
routes. Every field is `nullable` in Laravel's validation and
`AboutUsContent.merge()` tolerantly coerces whatever comes in, so — unlike
the other admin forms — there's no failure path here that needs `old()`/
error-preserving redirects; a save always succeeds."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from admirable.application.dto.settings_dto import UpdateAboutUsCommand
from admirable.application.use_cases.settings.get_about_us import GetAboutUs
from admirable.application.use_cases.settings.update_about_us import UpdateAboutUs
from admirable.presentation.web.dependencies import (
    get_get_about_us_admin_uc,
    get_session,
    get_update_about_us_uc,
    require_auth,
)
from admirable.presentation.web.forms.base import unflatten_form_data
from admirable.presentation.web.middleware.session import Session

router = APIRouter(prefix="/admin/settings", dependencies=[Depends(require_auth)])


def _templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates  # type: ignore[no-any-return]


@router.get("/about-us", name="admin.settings.about-us")
async def edit_about_us(
    request: Request, use_case: Annotated[GetAboutUs, Depends(get_get_about_us_admin_uc)]
) -> object:
    result = await use_case.execute()
    return _templates(request).TemplateResponse(
        request, "admin/settings/about-us.html", {"about_data": result.data}
    )


@router.post("/about-us", name="admin.settings.about-us.submit")
async def update_about_us(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[UpdateAboutUs, Depends(get_update_about_us_uc)],
) -> object:
    form = await request.form()
    raw = unflatten_form_data(list(form.multi_items()))
    raw.pop("_token", None)
    await use_case.execute(UpdateAboutUsCommand(data=raw))
    session.flash("success", 'Nội dung "Về chúng tôi" đã được cập nhật thành công.')
    return RedirectResponse(request.url_for("admin.settings.about-us"), status_code=303)
