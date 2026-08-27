"""Jinja2 environment: globals and filters that stand in for what Blade gave
Laravel for free (`route()`, `@csrf`, `old()`, `$errors`, `session()->flash`)."""

import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from jinja2 import pass_context
from markupsafe import Markup, escape
from starlette.templating import Jinja2Templates

from admirable.application.dto.auth_dto import AuthenticatedUserDTO
from admirable.config import Settings
from admirable.presentation.web.security.csrf_token import get_or_create_csrf_token

_TEMPLATES_DIR = Path(__file__).parent / "templates"


def asset_url(path: str) -> str:
    """`asset()` equivalent — shared with `seo.py` so both compute the same URL."""
    return f"/static/{path.lstrip('/')}"


def media_url(path: str | None, url_prefix: str) -> str | None:
    """`asset('storage/' . $path)` equivalent — shared with routers that need
    to build a fully-resolved media URL for `SeoMeta.og_image` (see seo.py's
    `_is_already_resolved`, which requires this instead of a bare path)."""
    return f"{url_prefix}{path}" if path else None


def _with_query(base: str, **params: Any) -> str:
    """`route($name, ['q' => $query])` equivalent: Starlette's `url_for` only
    fills path params, so query-string params (search filters, pagination)
    are appended here instead. Falsy values are dropped, matching Laravel's
    array-building pattern of only adding a key when it has a value."""
    filtered = {k: v for k, v in params.items() if v}
    if not filtered:
        return base
    return f"{base}?{urlencode(filtered)}"


@pass_context
def _route(context: dict[str, Any], name: str, **params: Any) -> str:
    request = context["request"]
    return str(request.url_for(name, **params))


@pass_context
def _csrf_token(context: dict[str, Any]) -> str:
    request = context["request"]
    return get_or_create_csrf_token(request.state.session)


@pass_context
def _csrf_field(context: dict[str, Any]) -> Markup:
    token = _csrf_token(context)
    return Markup(f'<input type="hidden" name="_token" value="{escape(token)}">')


@pass_context
def _old(context: dict[str, Any], field: str, default: str = "") -> str:
    request = context["request"]
    return request.state.session.old(field, default)  # type: ignore[no-any-return]


@pass_context
def _errors(context: dict[str, Any]) -> dict[str, list[str]]:
    request = context["request"]
    return request.state.session.errors  # type: ignore[no-any-return]


@pass_context
def _flash(context: dict[str, Any], key: str, default: Any = None) -> Any:
    request = context["request"]
    return request.state.session.get_flash(key, default)


@pass_context
def _current_user(context: dict[str, Any]) -> AuthenticatedUserDTO | None:
    request = context["request"]
    return getattr(request.state, "current_user", None)


@pass_context
def _is_route(context: dict[str, Any], pattern: str) -> bool:
    """`request()->routeIs('admin.figures.*')` equivalent; `None`-safe for
    contexts with no matched route (error pages)."""
    request = context["request"]
    route = request.scope.get("route")
    name = getattr(route, "name", None)
    if name is None:
        return False
    if pattern.endswith(".*"):
        return bool(name.startswith(pattern[:-1]))
    return bool(name == pattern)


def _nl2br(value: str) -> Markup:
    return Markup("<br>\n".join(str(escape(value)).split("\n")))


def _truncate_words(value: str, count: int = 30) -> str:
    words = value.split()
    if len(words) <= count:
        return value
    return " ".join(words[:count]) + "…"


def _str_limit(value: str | None, limit: int = 100, end: str = "...") -> str:
    """`Str::limit()` equivalent: truncates by character count, not words."""
    if not value:
        return ""
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + end


_TAG_RE = re.compile(r"<[^>]*>")


def _strip_tags(value: str | None) -> str:
    if not value:
        return ""
    return _TAG_RE.sub("", value)


def _number_format(value: float | int, decimals: int = 0) -> str:
    return f"{value:,.{decimals}f}"


_YOUTUBE_RE = re.compile(
    r"(?:youtu\.be/|youtube\.com/(?:embed/|v/|watch\?v=))([a-zA-Z0-9_-]{11})"
)


def _youtube_embed_id(url: str | None) -> str | None:
    if not url:
        return None
    match = _YOUTUBE_RE.search(url)
    return match.group(1) if match else None


_VI_MONTHS = (
    "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6",
    "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12",
)


def _date_vi(value: Any) -> str:
    if value is None:
        return ""
    return f"{value.day:02d}/{value.month:02d}/{value.year}"


def build_templates(settings: Settings) -> Jinja2Templates:
    templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))
    env = templates.env
    env.trim_blocks = True
    env.lstrip_blocks = True

    env.globals["route"] = _route
    env.globals["csrf_token"] = _csrf_token
    env.globals["csrf_field"] = _csrf_field
    env.globals["old"] = _old
    env.globals["errors"] = _errors
    env.globals["flash"] = _flash
    env.globals["current_user"] = _current_user
    env.globals["is_route"] = _is_route
    env.globals["now"] = datetime.now
    env.globals["asset"] = asset_url
    env.globals["with_query"] = _with_query
    env.globals["media_url"] = lambda path: media_url(path, settings.media.url_prefix)
    env.globals["config"] = {"app_name": settings.app.name, "base_url": settings.app.base_url}

    env.filters["nl2br"] = _nl2br
    env.filters["truncate_words"] = _truncate_words
    env.filters["date_vi"] = _date_vi
    env.filters["str_limit"] = _str_limit
    env.filters["strip_tags"] = _strip_tags
    env.filters["number_format"] = _number_format
    env.filters["youtube_embed_id"] = _youtube_embed_id

    return templates
