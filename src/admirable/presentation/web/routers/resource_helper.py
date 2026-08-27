"""DRY registration for admin CRUD resource groups — Laravel's
`Route::resource($name, Controller::class)->except(['show'])` equivalent: 6
named routes (index, create, store, edit, update, destroy) per resource.

Handlers are registered in the same order Laravel would: `create` (a static
GET path) before the `{id}`-parameterized routes, so a future static segment
added under a resource never risks being swallowed by a dynamic one.
"""

from collections.abc import Awaitable, Callable
from typing import Any, TypedDict

from fastapi import APIRouter

Handler = Callable[..., Awaitable[Any]]


class ResourceHandlers(TypedDict):
    index: Handler
    create: Handler
    store: Handler
    edit: Handler
    update: Handler
    destroy: Handler


def register_resource(
    router: APIRouter, prefix: str, name: str, handlers: ResourceHandlers
) -> None:
    router.add_api_route(prefix, handlers["index"], methods=["GET"], name=f"{name}.index")
    router.add_api_route(
        f"{prefix}/create", handlers["create"], methods=["GET"], name=f"{name}.create"
    )
    router.add_api_route(prefix, handlers["store"], methods=["POST"], name=f"{name}.store")
    router.add_api_route(
        f"{prefix}/{{id}}/edit", handlers["edit"], methods=["GET"], name=f"{name}.edit"
    )
    router.add_api_route(
        f"{prefix}/{{id}}", handlers["update"], methods=["PUT"], name=f"{name}.update"
    )
    router.add_api_route(
        f"{prefix}/{{id}}", handlers["destroy"], methods=["DELETE"], name=f"{name}.destroy"
    )
