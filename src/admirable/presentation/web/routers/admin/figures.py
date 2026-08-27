"""Ports `FigureController` + `routes/web.php`'s `admin.figures.*`
resource group — the largest of the admin resources."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from admirable.application.dto.figure_dto import (
    ContentBlockInput,
    CreateFigureCommand,
    KeyFactInput,
    UpdateFigureCommand,
)
from admirable.application.use_cases.figures.create_figure import CreateFigure
from admirable.application.use_cases.figures.delete_figure import DeleteFigure
from admirable.application.use_cases.figures.get_figure import GetFigure
from admirable.application.use_cases.figures.list_figures import ListFigures, ListFiguresQuery
from admirable.application.use_cases.figures.update_figure import UpdateFigure
from admirable.domain.value_objects.pagination import Page
from admirable.infrastructure.container import Container
from admirable.presentation.web.dependencies import (
    get_container,
    get_create_figure_uc,
    get_delete_figure_uc,
    get_get_figure_uc,
    get_list_figures_uc,
    get_session,
    get_update_figure_uc,
    require_auth,
)
from admirable.presentation.web.forms.base import get_uploaded_file, parse_form
from admirable.presentation.web.forms.figure_form import FIGURE_FIELD_LABELS, FigureForm
from admirable.presentation.web.middleware.session import Session
from admirable.presentation.web.routers.resource_helper import register_resource

router = APIRouter(prefix="/admin", dependencies=[Depends(require_auth)])


def _templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates  # type: ignore[no-any-return]


def _old_or(session: Session, field: str, fallback: list[object]) -> list[object]:
    """`old($field, $figure->$field ?? [])` equivalent — see `stories.py`'s
    identically-shaped `_blocks_context` for the full rationale."""
    old = session.old_raw(field)
    return old if old is not None else fallback


def _selected_category_ids(session: Session, fallback: list[int]) -> list[int]:
    old = session.old_raw("category_ids")
    if old is None:
        return fallback
    return [int(v) for v in old]


async def _index(
    request: Request,
    use_case: Annotated[ListFigures, Depends(get_list_figures_uc)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    page = int(request.query_params.get("page", 1))
    search = request.query_params.get("search") or None
    category_id_raw = request.query_params.get("category_id")
    category_id = int(category_id_raw) if category_id_raw else None

    result = await use_case.execute(
        ListFiguresQuery(search=search, category_id=category_id, page=page, per_page=15)
    )
    figures = Page(
        items=result.items, total=result.total, page=result.page, per_page=result.per_page
    )
    categories = await container.categories.list_all()
    return _templates(request).TemplateResponse(
        request,
        "admin/figures/index.html",
        {
            "figures": figures,
            "categories": categories,
            "search": search or "",
            "category_id": category_id,
        },
    )


async def _create(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    categories = await container.categories.list_all()
    return _templates(request).TemplateResponse(
        request,
        "admin/figures/form.html",
        {
            "categories": categories,
            "key_facts": _old_or(session, "key_facts", []),
            "blocks": _old_or(session, "content_blocks", []),
            "selected_category_ids": _selected_category_ids(session, []),
        },
    )


async def _store(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[CreateFigure, Depends(get_create_figure_uc)],
) -> object:
    redirect_to = str(request.url_for("admin.figures.create"))
    form = await parse_form(request, FigureForm, redirect_to, FIGURE_FIELD_LABELS)
    form_data = await request.form()

    created = await use_case.execute(
        CreateFigureCommand(
            name=form.name,
            short_description=form.short_description,
            key_facts=[KeyFactInput(**kf.model_dump()) for kf in form.key_facts],
            content_blocks=[ContentBlockInput(**cb.model_dump()) for cb in form.content_blocks],
            youtube_url=form.youtube_url,
            category_ids=form.category_ids,
            avatar=await get_uploaded_file(form_data, "avatar"),
            audio=await get_uploaded_file(form_data, "audio"),
        )
    )
    session.flash("success", "Nhân vật đã được tạo thành công.")
    return RedirectResponse(request.url_for("admin.figures.edit", id=created.id), status_code=303)


async def _edit(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[GetFigure, Depends(get_get_figure_uc)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    figure = await use_case.execute(id)
    categories = await container.categories.list_all()
    return _templates(request).TemplateResponse(
        request,
        "admin/figures/form.html",
        {
            "figure": figure,
            "categories": categories,
            "key_facts": _old_or(
                session, "key_facts", [kf.model_dump() for kf in figure.key_facts]
            ),
            "blocks": _old_or(
                session, "content_blocks", [cb.model_dump() for cb in figure.content_blocks]
            ),
            "selected_category_ids": _selected_category_ids(session, figure.category_ids),
        },
    )


async def _update(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[UpdateFigure, Depends(get_update_figure_uc)],
) -> object:
    redirect_to = str(request.url_for("admin.figures.edit", id=id))
    form = await parse_form(request, FigureForm, redirect_to, FIGURE_FIELD_LABELS)
    form_data = await request.form()

    await use_case.execute(
        UpdateFigureCommand(
            figure_id=id,
            name=form.name,
            short_description=form.short_description,
            key_facts=[KeyFactInput(**kf.model_dump()) for kf in form.key_facts],
            content_blocks=[ContentBlockInput(**cb.model_dump()) for cb in form.content_blocks],
            youtube_url=form.youtube_url,
            category_ids=form.category_ids,
            avatar=await get_uploaded_file(form_data, "avatar"),
            audio=await get_uploaded_file(form_data, "audio"),
        )
    )
    session.flash("success", "Nhân vật đã được cập nhật thành công.")
    return RedirectResponse(request.url_for("admin.figures.edit", id=id), status_code=303)


async def _destroy(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[DeleteFigure, Depends(get_delete_figure_uc)],
) -> object:
    try:
        await use_case.execute(id)
    except Exception as exc:
        session.flash("error", f"Không thể xóa nhân vật: {exc}")
        return RedirectResponse(request.url_for("admin.figures.index"), status_code=303)
    session.flash("success", "Nhân vật đã được xóa thành công.")
    return RedirectResponse(request.url_for("admin.figures.index"), status_code=303)


register_resource(
    router,
    "/figures",
    "admin.figures",
    {
        "index": _index,
        "create": _create,
        "store": _store,
        "edit": _edit,
        "update": _update,
        "destroy": _destroy,
    },
)
