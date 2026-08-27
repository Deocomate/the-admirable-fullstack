"""Standard CRUD resource router registration helper for admin management views.

Registers 6 canonical named routes: index, create, store, edit, update, and destroy.
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
        f"{prefix}/{{id}}", handlers["update"], methods=["PUT", "PATCH"], name=f"{name}.update"
    )
    router.add_api_route(
        f"{prefix}/{{id}}", handlers["destroy"], methods=["DELETE"], name=f"{name}.destroy"
    )
