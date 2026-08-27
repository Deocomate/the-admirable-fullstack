"""Ports `StorySnippetController` + `routes/web.php`'s `admin.stories.*`
resource group."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from admirable.application.dto.figure_dto import ContentBlockInput
from admirable.application.dto.story_dto import CreateStoryCommand, UpdateStoryCommand
from admirable.application.use_cases.stories.create_story import CreateStory
from admirable.application.use_cases.stories.delete_story import DeleteStory
from admirable.application.use_cases.stories.get_story import GetStory
from admirable.application.use_cases.stories.list_stories import ListStories, ListStoriesQuery
from admirable.application.use_cases.stories.update_story import UpdateStory
from admirable.domain.value_objects.pagination import Page
from admirable.infrastructure.container import Container
from admirable.presentation.web.dependencies import (
    get_container,
    get_create_story_uc,
    get_delete_story_uc,
    get_get_story_uc,
    get_list_stories_uc,
    get_session,
    get_update_story_uc,
    require_auth,
)
from admirable.presentation.web.forms.base import get_uploaded_file, parse_form
from admirable.presentation.web.forms.story_form import STORY_FIELD_LABELS, StoryForm
from admirable.presentation.web.middleware.session import Session
from admirable.presentation.web.routers.resource_helper import register_resource

router = APIRouter(prefix="/admin", dependencies=[Depends(require_auth)])


def _templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates  # type: ignore[no-any-return]


def _blocks_context(session: Session, story: object | None) -> list[dict[str, object]]:
    """`old('content_blocks', $story->content_blocks ?? [])` equivalent: a
    validation failure repopulates from the raw unflattened payload; a clean
    edit load repopulates from the persisted story."""
    old = session.old_raw("content_blocks")
    if old is not None:
        return old  # type: ignore[no-any-return]
    if story is None:
        return []
    return [b.model_dump() for b in story.content_blocks]  # type: ignore[attr-defined]


async def _index(
    request: Request,
    use_case: Annotated[ListStories, Depends(get_list_stories_uc)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    page = int(request.query_params.get("page", 1))
    search = request.query_params.get("search") or None
    figure_id_raw = request.query_params.get("figure_id")
    figure_id = int(figure_id_raw) if figure_id_raw else None

    result = await use_case.execute(
        ListStoriesQuery(figure_id=figure_id, search=search, page=page, per_page=15)
    )
    stories = Page(
        items=result.items, total=result.total, page=result.page, per_page=result.per_page
    )
    figures = await container.figures.list_all()
    return _templates(request).TemplateResponse(
        request,
        "admin/stories/index.html",
        {
            "stories": stories,
            "figures": figures,
            "search": search or "",
            "figure_id": figure_id,
        },
    )


async def _create(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    figures = await container.figures.list_all()
    selected_figure_id = request.query_params.get("figure_id")
    return _templates(request).TemplateResponse(
        request,
        "admin/stories/form.html",
        {
            "figures": figures,
            "selected_figure_id": selected_figure_id,
            "blocks": _blocks_context(session, None),
        },
    )


async def _store(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[CreateStory, Depends(get_create_story_uc)],
) -> object:
    redirect_to = str(request.url_for("admin.stories.create"))
    form = await parse_form(request, StoryForm, redirect_to, STORY_FIELD_LABELS)
    form_data = await request.form()

    await use_case.execute(
        CreateStoryCommand(
            figure_id=form.figure_id,
            title=form.title,
            subtitle=form.subtitle,
            content_blocks=[ContentBlockInput(**b.model_dump()) for b in form.content_blocks],
            youtube_url=form.youtube_url,
            image=await get_uploaded_file(form_data, "image"),
            audio=await get_uploaded_file(form_data, "audio"),
        )
    )
    session.flash("success", "Mẩu chuyện đã được tạo thành công.")
    return RedirectResponse(request.url_for("admin.stories.index"), status_code=303)


async def _edit(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[GetStory, Depends(get_get_story_uc)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    story = await use_case.execute(id)
    figures = await container.figures.list_all()
    return _templates(request).TemplateResponse(
        request,
        "admin/stories/form.html",
        {
            "story": story,
            "figures": figures,
            "blocks": _blocks_context(session, story),
        },
    )


async def _update(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[UpdateStory, Depends(get_update_story_uc)],
) -> object:
    redirect_to = str(request.url_for("admin.stories.edit", id=id))
    form = await parse_form(request, StoryForm, redirect_to, STORY_FIELD_LABELS)
    form_data = await request.form()

    await use_case.execute(
        UpdateStoryCommand(
            story_id=id,
            figure_id=form.figure_id,
            title=form.title,
            subtitle=form.subtitle,
            content_blocks=[ContentBlockInput(**b.model_dump()) for b in form.content_blocks],
            youtube_url=form.youtube_url,
            image=await get_uploaded_file(form_data, "image"),
            audio=await get_uploaded_file(form_data, "audio"),
        )
    )
    session.flash("success", "Mẩu chuyện đã được cập nhật thành công.")
    return RedirectResponse(request.url_for("admin.stories.index"), status_code=303)


async def _destroy(
    request: Request,
    id: int,
    session: Annotated[Session, Depends(get_session)],
    use_case: Annotated[DeleteStory, Depends(get_delete_story_uc)],
) -> object:
    try:
        await use_case.execute(id)
    except Exception as exc:
        session.flash("error", f"Không thể xóa mẩu chuyện: {exc}")
        return RedirectResponse(request.url_for("admin.stories.index"), status_code=303)
    session.flash("success", "Mẩu chuyện đã được xóa thành công.")
    return RedirectResponse(request.url_for("admin.stories.index"), status_code=303)


register_resource(
    router,
    "/stories",
    "admin.stories",
    {
        "index": _index,
        "create": _create,
        "store": _store,
        "edit": _edit,
        "update": _update,
        "destroy": _destroy,
    },
)
