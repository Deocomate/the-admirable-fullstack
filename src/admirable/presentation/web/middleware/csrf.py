"""CSRF protection for unsafe methods (POST/PUT/PATCH/DELETE — evaluated
after method-override, so a `_method=DELETE` POST is checked as DELETE).

Token comes from the `_token` form field or the `X-CSRF-Token` header
(compared case-insensitively per-spec; the admin JS actually sends
`X-CSRF-TOKEN`). Missing or mismatched token -> HTTP 419, matching Laravel's
"Page Expired" status code so existing client-side error handling keeps working.
"""

import secrets
from typing import Any

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.types import ASGIApp, Scope, Send

from admirable.presentation.web.middleware._asgi_body import drain_body, header, replay

_SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
_FORM_CONTENT_TYPES = (b"application/x-www-form-urlencoded", b"multipart/form-data")
_CSRF_STATUS = 419


class CsrfMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Any, send: Send) -> None:
        if scope["type"] != "http" or scope["method"] in _SAFE_METHODS:
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        session = getattr(request.state, "session", None)
        expected = session.get("csrf_token") if session is not None else None

        provided = header(scope, b"x-csrf-token").decode("utf-8") or None
        downstream_receive = receive

        if not provided:
            content_type = header(scope, b"content-type")
            if content_type.startswith(_FORM_CONTENT_TYPES):
                body = await drain_body(receive)
                downstream_receive = replay(body)
                form: Any = await Request(scope, replay(body)).form()
                raw = form.get("_token")
                provided = str(raw) if raw else None
                await form.close()

        if not expected or not provided or not secrets.compare_digest(provided, expected):
            response = self._failure_response(request)
            await response(scope, receive, send)
            return

        await self.app(scope, downstream_receive, send)

    def _failure_response(self, request: Request) -> HTMLResponse | JSONResponse:
        wants_json = "application/json" in request.headers.get("accept", "")
        message = "Phiên làm việc đã hết hạn. Vui lòng tải lại trang và thử lại."
        if wants_json:
            return JSONResponse({"message": message}, status_code=_CSRF_STATUS)
        return HTMLResponse(
            f"<html><body><h1>419 — {message}</h1></body></html>", status_code=_CSRF_STATUS
        )
