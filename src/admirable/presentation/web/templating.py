"""Jinja2 environment: globals and filters that stand in for what Blade gave
Laravel for free (`route()`, `@csrf`, `old()`, `$errors`, `session()->flash`)."""

from pathlib import Path
from typing import Any

from jinja2 import pass_context
from markupsafe import Markup, escape
from starlette.templating import Jinja2Templates

from admirable.application.dto.auth_dto import AuthenticatedUserDTO
from admirable.config import Settings
from admirable.presentation.web.security.csrf_token import get_or_create_csrf_token

_TEMPLATES_DIR = Path(__file__).parent / "templates"


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


def _nl2br(value: str) -> Markup:
    return Markup("<br>\n".join(str(escape(value)).split("\n")))


def _truncate_words(value: str, count: int = 30) -> str:
    words = value.split()
    if len(words) <= count:
        return value
    return " ".join(words[:count]) + "…"


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
    env.globals["asset"] = lambda path: f"/static/{path.lstrip('/')}"
    env.globals["media_url"] = lambda path: f"{settings.media.url_prefix}{path}" if path else None
    env.globals["config"] = {"app_name": settings.app.name, "base_url": settings.app.base_url}

    env.filters["nl2br"] = _nl2br
    env.filters["truncate_words"] = _truncate_words
    env.filters["date_vi"] = _date_vi

    return templates
