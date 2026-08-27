"""Registers application exception handlers mapping domain and web exceptions to HTTP responses."""

import logging

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.templating import Jinja2Templates

from admirable.domain.exceptions import (
    BusinessRuleViolationError,
    EntityNotFoundError,
    InvalidAudioTransitionError,
)
from admirable.presentation.web.exceptions import (
    AlreadyAuthenticatedError,
    ForbiddenError,
    FormValidationError,
    NotAuthenticatedError,
)

logger = logging.getLogger("admirable.web")


def _wants_json(request: Request) -> bool:
    return "application/json" in request.headers.get("accept", "")


def register_exception_handlers(app: FastAPI, templates: Jinja2Templates) -> None:
    @app.exception_handler(InvalidAudioTransitionError)
    async def _audio_conflict(request: Request, exc: InvalidAudioTransitionError) -> Response:
        return JSONResponse({"message": str(exc)}, status_code=409)

    @app.exception_handler(EntityNotFoundError)
    async def _not_found(request: Request, exc: EntityNotFoundError) -> Response:
        if _wants_json(request):
            return JSONResponse({"message": str(exc)}, status_code=404)
        return templates.TemplateResponse(request, "errors/404.html", status_code=404)

    @app.exception_handler(BusinessRuleViolationError)
    async def _business_rule(request: Request, exc: BusinessRuleViolationError) -> Response:
        if _wants_json(request):
            return JSONResponse({"message": str(exc)}, status_code=422)
        session = getattr(request.state, "session", None)
        if session is not None:
            session.flash("error", str(exc))
        return RedirectResponse(request.headers.get("referer", "/"), status_code=303)

    @app.exception_handler(NotAuthenticatedError)
    async def _not_authenticated(request: Request, exc: NotAuthenticatedError) -> Response:
        return RedirectResponse(request.url_for("admin.auth.login"), status_code=303)

    @app.exception_handler(AlreadyAuthenticatedError)
    async def _already_authenticated(request: Request, exc: AlreadyAuthenticatedError) -> Response:
        return RedirectResponse(request.url_for("admin.dashboard"), status_code=303)

    @app.exception_handler(ForbiddenError)
    async def _forbidden(request: Request, exc: ForbiddenError) -> Response:
        if _wants_json(request):
            return JSONResponse({"message": exc.message}, status_code=403)
        return templates.TemplateResponse(
            request, "errors/403.html", {"message": exc.message}, status_code=403
        )

    @app.exception_handler(FormValidationError)
    async def _form_validation(request: Request, exc: FormValidationError) -> Response:
        session = getattr(request.state, "session", None)
        if session is not None:
            session.set_old_and_errors(exc.old_input, exc.errors)
        return RedirectResponse(exc.redirect_to, status_code=303)

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception) -> Response:
        logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
        if _wants_json(request):
            return JSONResponse({"message": "Internal server error."}, status_code=500)
        try:
            return templates.TemplateResponse(request, "errors/500.html", status_code=500)
        except Exception:
            return HTMLResponse("<h1>500 — Internal Server Error</h1>", status_code=500)
