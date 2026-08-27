"""Ports `CategoryController` + `routes/web.php`'s `admin.categories.*`
resource group (`Route::resource('categories', ...)->except(['show'])`)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from admirable.application.dto.category_dto import CreateCategoryCommand, UpdateCategoryCommand
from admirable.application.use_cases.categories.create_category import CreateCategory
from admirable.application.use_cases.categories.delete_category import DeleteCategory
from admirable.application.use_cases.categories.get_category import GetCategory
from admirable.application.use_cases.categories.list_categories import (
    ListCategories,
    ListCategoriesQuery,
)
from admirable.application.use_cases.categories.update_category import UpdateCategory
from admirable.domain.exceptions import DuplicateValueError
from admirable.domain.value_objects.pagination import Page
from admirable.presentation.web.dependencies import (
    get_create_category_uc,
    get_delete_category_uc,
    get_get_category_uc,
    get_list_categories_admin_uc,
    get_session,
    get_update_category_uc,
    require_auth,
)
from admirable.presentation.web.exceptions import FormValidationError
from admirable.presentation.web.forms.base import parse_form
from admirable.presentation.web.forms.category_form import CATEGORY_FIELD_LABELS, CategoryForm
from admirable.presentation.web.middleware.session import Session
from admirable.presentation.web.routers.resource_helper import register_resource

router = APIRouter(prefix="/admin", dependencies=[Depends(require_auth)])


def _templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates  # type: ignore[no-any-return]


async def _index(
    request: Request, use_case: Annotated[ListCategories, Depends(get_list_categories_admin_uc)]
) -> object:
    page = int(request.query_params.get("page", 1))
    result = await use_case.execute(ListCategoriesQuery(page=page, per_page=15))
    categories = Page(
        items=result.items, total=result.total, page=result.page, per_page=result.per_page
    )
    return _templates(request).TemplateResponse(
        request, "admin/categories/index.html", {"categories": categories}
    )


async def _create(request: Request) -> object:
    return _templates(request).TemplateResponse(request, "admin/categories/form.html")


async def _store(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[CreateCategory, Depends(get_create_category_uc)],
) -> object:
    redirect_to = str(request.url_for("admin.categories.create"))
    form = await parse_form(request, CategoryForm, redirect_to, CATEGORY_FIELD_LABELS)
    try:
        await use_case.execute(CreateCategoryCommand(name=form.name))
    except DuplicateValueError:
        raise FormValidationError(
            {"name": ["Lĩnh vực này đã tồn tại."]}, {"name": form.name}, redirect_to
        ) from None
    session.flash("success", "Lĩnh vực đã được tạo thành công.")
    return RedirectResponse(request.url_for("admin.categories.index"), status_code=303)


async def _edit(
    request: Request, id: int, use_case: Annotated[GetCategory, Depends(get_get_category_uc)]
) -> object:
    category = await use_case.execute(id)
    return _templates(request).TemplateResponse(
        request, "admin/categories/form.html", {"category": category}
    )


async def _update(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[UpdateCategory, Depends(get_update_category_uc)],
) -> object:
    redirect_to = str(request.url_for("admin.categories.edit", id=id))
    form = await parse_form(request, CategoryForm, redirect_to, CATEGORY_FIELD_LABELS)
    try:
        await use_case.execute(UpdateCategoryCommand(category_id=id, name=form.name))
    except DuplicateValueError:
        raise FormValidationError(
            {"name": ["Lĩnh vực này đã tồn tại."]}, {"name": form.name}, redirect_to
        ) from None
    session.flash("success", "Lĩnh vực đã được cập nhật thành công.")
    return RedirectResponse(request.url_for("admin.categories.index"), status_code=303)


async def _destroy(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[DeleteCategory, Depends(get_delete_category_uc)],
) -> object:
    try:
        await use_case.execute(id)
    except Exception as exc:
        session.flash("error", f"Không thể xóa lĩnh vực: {exc}")
        return RedirectResponse(request.url_for("admin.categories.index"), status_code=303)
    session.flash("success", "Lĩnh vực đã được xóa thành công.")
    return RedirectResponse(request.url_for("admin.categories.index"), status_code=303)


register_resource(
    router,
    "/categories",
    "admin.categories",
    {
        "index": _index,
        "create": _create,
        "store": _store,
        "edit": _edit,
        "update": _update,
        "destroy": _destroy,
    },
)
