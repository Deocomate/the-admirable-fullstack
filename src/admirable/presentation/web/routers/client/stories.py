"""Ports `StoryController::show` / `client.stories.show`."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates

from admirable.application.use_cases.public.get_story_detail import GetStoryDetail
from admirable.infrastructure.container import Container
from admirable.presentation.web.dependencies import get_container, get_story_detail_uc
from admirable.presentation.web.routers.client._context import build_client_context
from admirable.presentation.web.seo import SeoMeta
from admirable.presentation.web.templating import media_url

router = APIRouter(prefix="/cau-chuyen")


@router.get("/{story_id}", name="client.stories.show")
async def show(
    request: Request,
    story_id: int,
    uc: Annotated[GetStoryDetail, Depends(get_story_detail_uc)],
    container: Annotated[Container, Depends(get_container)],
) -> object:
    data = await uc.execute(story_id)
    snippet = data.snippet
    templates: Jinja2Templates = request.app.state.templates
    settings = request.app.state.settings

    og_image = media_url(snippet.image_path, settings.media.url_prefix) or media_url(
        snippet.figure_avatar_path, settings.media.url_prefix
    )
    article_tags = tuple(t for t in (snippet.category_name, snippet.figure_name) if t)
    body_preview = " ".join(b.text_en for b in snippet.content_blocks if b.text_en)
    description = (snippet.subtitle or body_preview or snippet.figure_name)[:160]
    context = await build_client_context(
        request,
        container,
        SeoMeta(
            title=f"{snippet.title} — The Admirable",
            description=description,
            canonical_url=str(request.url_for("client.stories.show", story_id=snippet.id)),
            og_type="article",
            og_image=og_image,
            published_time=snippet.created_at.isoformat() if snippet.created_at else None,
            modified_time=snippet.updated_at.isoformat() if snippet.updated_at else None,
            article_section=snippet.category_name,
            article_tags=article_tags,
            keywords=f"{snippet.title}, {snippet.figure_name}, The Admirable",
        ),
    )
    context.update({"snippet": snippet, "other_stories": data.other_stories})
    return templates.TemplateResponse(request, "client/story/show.html", context)
