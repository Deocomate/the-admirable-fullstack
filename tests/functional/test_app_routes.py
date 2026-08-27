"""FastAPI route structure and registration integrity tests."""

from typing import Any

from fastapi.routing import APIRoute
from starlette.routing import BaseRoute, Route

from admirable.presentation.web.main import create_app


def _extract_routes(routes: list[BaseRoute]) -> list[dict[str, Any]]:
    extracted: list[dict[str, Any]] = []

    for route in routes:
        if hasattr(route, "original_router") and hasattr(route.original_router, "routes"):
            extracted.extend(_extract_routes(route.original_router.routes))
        elif hasattr(route, "routes"):
            extracted.extend(_extract_routes(route.routes))
        elif isinstance(route, (Route, APIRoute)):
            methods = sorted(list(route.methods)) if route.methods else ["GET"]
            endpoint_fn = getattr(route, "endpoint", None)
            endpoint_name = getattr(endpoint_fn, "__name__", str(endpoint_fn))
            extracted.append(
                {
                    "path": route.path,
                    "methods": methods,
                    "name": getattr(route, "name", None),
                    "endpoint": endpoint_name,
                }
            )

    return extracted


def test_all_expected_app_routes_registered() -> None:
    app = create_app()
    routes = _extract_routes(app.routes)

    route_names = {r["name"] for r in routes if r["name"]}

    # Required Client Routes
    expected_client_routes = {
        "client.home",
        "client.categories.index",
        "client.categories.show",
        "client.figures.show",
        "client.stories.show",
        "client.search",
        "client.about-us",
        "client.contact",
    }
    for name in expected_client_routes:
        assert name in route_names, f"Expected client route {name} not found"

    # Required Admin Auth Routes
    expected_auth_routes = {
        "admin.auth.login",
        "admin.auth.login.submit",
        "admin.auth.forgot-password",
        "admin.auth.forgot-password.submit",
        "admin.auth.reset-password",
        "admin.auth.reset-password.submit",
        "admin.auth.logout",
    }
    for name in expected_auth_routes:
        assert name in route_names, f"Expected admin auth route {name} not found"

    # Required Admin Resource Routes
    expected_resource_routes = {
        "admin.dashboard",
        "admin.categories.index",
        "admin.categories.create",
        "admin.categories.store",
        "admin.categories.edit",
        "admin.categories.update",
        "admin.categories.destroy",
        "admin.figures.index",
        "admin.figures.create",
        "admin.figures.store",
        "admin.figures.edit",
        "admin.figures.update",
        "admin.figures.destroy",
        "admin.featured-figures.index",
        "admin.featured-figures.store",
        "admin.featured-figures.destroy",
        "admin.featured-figures.reorder",
        "admin.stories.index",
        "admin.stories.create",
        "admin.stories.store",
        "admin.stories.edit",
        "admin.stories.update",
        "admin.stories.destroy",
        "admin.contacts.index",
        "admin.contacts.create",
        "admin.contacts.store",
        "admin.contacts.edit",
        "admin.contacts.update",
        "admin.contacts.destroy",
        "admin.settings.about-us",
        "admin.settings.about-us.submit",
        "admin.users.index",
        "admin.users.create",
        "admin.users.store",
        "admin.users.edit",
        "admin.users.update",
        "admin.users.destroy",
    }
    for name in expected_resource_routes:
        assert name in route_names, f"Expected admin resource route {name} not found"

    # Audio Endpoints
    expected_audio_routes = {
        "admin.audio.generate",
        "admin.audio.cancel",
        "admin.audio.status",
    }
    for name in expected_audio_routes:
        assert name in route_names, f"Expected audio route {name} not found"

    assert len(routes) >= 50, f"Expected at least 50 application routes, found {len(routes)}"
