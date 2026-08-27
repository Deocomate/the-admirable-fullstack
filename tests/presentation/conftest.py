"""Shared fixtures for pure template-rendering tests (Phase 8).

These deliberately avoid DB/Redis (unlike tests/functional/): rendering a
layout or macro needs a `Request` (for `request.url_for`) and a `Session`
(for `csrf_token()`), both of which are cheap to construct in-memory —
there's no reason to spin up a real app stack just to check HTML output.
"""

from collections.abc import Callable

import pytest
from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from admirable.config import AppSettings, DbSettings, MediaSettings, RedisSettings, Settings
from admirable.presentation.web.middleware.session import Session
from admirable.presentation.web.templating import build_templates

# Every named route referenced anywhere in the Phase 8 template tree
# (layouts/partials/macros). Client/admin page routes don't exist for real
# until Phase 9/10 — registering them here as dummy endpoints is exactly
# what those phases will do for real, so `route()`/`url_for()` behaves
# identically to production.
_ROUTE_NAMES = [
    "client.home",
    "client.categories.index",
    "client.categories.show",
    "client.search",
    "client.about-us",
    "client.contact",
    "client.figures.show",
    "client.stories.show",
    "admin.dashboard",
    "admin.auth.logout",
    "admin.users.index",
    "admin.categories.index",
    "admin.figures.index",
    "admin.featured-figures.index",
    "admin.stories.index",
    "admin.contacts.index",
    "admin.settings.about-us",
]

_PARAM_ROUTE_NAMES = {
    "client.categories.show": "/categories/{slug}",
    "client.figures.show": "/figures/{slug}",
    "client.stories.show": "/stories/{story_id}",
}


def _dummy_endpoint() -> dict[str, bool]:
    return {"ok": True}


def _build_app(settings: Settings) -> FastAPI:
    app = FastAPI()
    app.state.settings = settings
    app.state.templates = build_templates(settings)

    for name in _ROUTE_NAMES:
        path = _PARAM_ROUTE_NAMES.get(name, f"/_test/{name}")
        app.add_api_route(path, _dummy_endpoint, name=name)

    return app


@pytest.fixture
def template_settings() -> Settings:
    return Settings(
        app=AppSettings(secret_key="a" * 32, env="testing", debug=True, base_url="http://test"),
        db=DbSettings(),
        redis=RedisSettings(),
        media=MediaSettings(),
    )


@pytest.fixture
def templates(template_settings: Settings) -> Jinja2Templates:
    return build_templates(template_settings)


@pytest.fixture
def make_request(template_settings: Settings) -> Callable[..., Request]:
    """Builds a `Request` with a real router (for `url_for`) and an
    in-memory `Session` (for `csrf_token`/`old`/`errors`/`flash`)."""
    app = _build_app(template_settings)

    def _make(
        path: str = "/", method: str = "GET", session_data: dict[str, object] | None = None
    ) -> Request:
        scope = {
            "type": "http",
            "method": method,
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": [],
            "app": app,
            "router": app.router,
            "scheme": "http",
            "server": ("test", 80),
            "client": ("test", 123),
        }
        request = Request(scope)
        request.state.session = Session("test-sid", session_data or {})
        return request

    return _make
