"""Ports `FeaturedFigureController` + `routes/web.php`'s
`admin.featured-figures.*` group (index/store/destroy + the JSON `reorder`
endpoint SortableJS calls after a drag-and-drop)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from admirable.application.use_cases.featured.add_featured import AddFeatured
from admirable.application.use_cases.featured.list_featured import ListFeatured
from admirable.application.use_cases.featured.remove_featured import RemoveFeatured
from admirable.application.use_cases.featured.reorder_featured import ReorderFeatured
from admirable.infrastructure.container import Container
from admirable.presentation.web.dependencies import (
    get_add_featured_uc,
    get_container,
    get_list_featured_uc,
    get_remove_featured_uc,
    get_reorder_featured_uc,
    get_session,
    require_auth,
)
from admirable.presentation.web.middleware.session import Session

router = APIRouter(prefix="/admin/featured-figures", dependencies=[Depends(require_auth)])


def _templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates  # type: ignore[no-any-return]


@router.get("", name="admin.featured-figures.index")
async def index(
    request: Request,
    use_case: Annotated[ListFeatured, Depends(get_list_featured_uc)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    featured_figures = await use_case.execute()
    search = request.query_params.get("search") or None
    available_figures = await container.featured.list_available_figures(search, limit=200)
    return _templates(request).TemplateResponse(
        request,
        "admin/featured-figures/index.html",
        {
            "featured_figures": featured_figures,
            "available_figures": available_figures,
            "search": search or "",
        },
    )


@router.post("", name="admin.featured-figures.store")
async def store(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[AddFeatured, Depends(get_add_featured_uc)],
) -> object:
    form = await request.form()
    raw_figure_id = form.get("figure_id")
    if not raw_figure_id:
        session.flash("error", "Vui lòng chọn một nhân vật.")
        return RedirectResponse(request.url_for("admin.featured-figures.index"), status_code=303)
    await use_case.execute(int(raw_figure_id))  # type: ignore[arg-type]
    session.flash("success", "Đã thêm nhân vật vào danh sách tiêu biểu.")
    return RedirectResponse(request.url_for("admin.featured-figures.index"), status_code=303)


@router.delete("/{id}", name="admin.featured-figures.destroy")
async def destroy(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[RemoveFeatured, Depends(get_remove_featured_uc)],
) -> object:
    await use_case.execute(id)
    session.flash("success", "Đã gỡ nhân vật khỏi danh sách tiêu biểu.")
    return RedirectResponse(request.url_for("admin.featured-figures.index"), status_code=303)


class ReorderRequest(BaseModel):
    figure_ids: list[int]


@router.post("/reorder", name="admin.featured-figures.reorder")
async def reorder(
    body: ReorderRequest,
    use_case: Annotated[ReorderFeatured, Depends(get_reorder_featured_uc)],
) -> object:
    await use_case.execute(body.figure_ids)
    return JSONResponse({"message": "Cập nhật vị trí thành công."})
