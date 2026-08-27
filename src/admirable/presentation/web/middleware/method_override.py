"""Laravel's `@method('PUT')` spoofing: a hidden `_method` form field on a
POST request is used to route to PUT/PATCH/DELETE handlers.

Pure ASGI (not BaseHTTPMiddleware) because the body must be read to find
`_method`, then replayed byte-for-byte to the real handler — BaseHTTPMiddleware
builds a fresh Request downstream that can't see a body already consumed by
a middleware-local Request object.
"""

from typing import Any

from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Send

from admirable.presentation.web.middleware._asgi_body import drain_body, header, replay

_OVERRIDABLE_METHODS = {"PUT", "PATCH", "DELETE"}
_FORM_CONTENT_TYPES = (b"application/x-www-form-urlencoded", b"multipart/form-data")


class MethodOverrideMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Any, send: Send) -> None:
        if scope["type"] != "http" or scope["method"] != "POST":
            await self.app(scope, receive, send)
            return

        content_type = header(scope, b"content-type")
        if not content_type.startswith(_FORM_CONTENT_TYPES):
            await self.app(scope, receive, send)
            return

        body = await drain_body(receive)
        override = await _extract_method_override(scope, body)

        if override in _OVERRIDABLE_METHODS:
            scope = {**scope, "method": override}

        await self.app(scope, replay(body), send)


async def _extract_method_override(scope: Scope, body: bytes) -> str | None:
    temp_request = Request(scope, replay(body))
    form: Any = await temp_request.form()
    try:
        raw = form.get("_method")
        return str(raw).upper() if raw else None
    finally:
        await form.close()
