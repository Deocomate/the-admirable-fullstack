"""Method-override is exercised indirectly here since Phase 7 has no PUT/DELETE
routes yet (those arrive in Phase 10) — these tests hit the ASGI middleware
directly with a tiny throwaway app, proving the body-replay mechanism itself
works for both urlencoded and multipart-with-file-upload bodies (the
plan's explicit risk: middleware body-draining must not break router form
reads, including file uploads)."""

from httpx import ASGITransport, AsyncClient
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from admirable.presentation.web.middleware.method_override import MethodOverrideMiddleware


async def _echo(request: Request) -> JSONResponse:
    from starlette.datastructures import UploadFile

    form = await request.form()
    file = form.get("avatar")
    file_info = None
    if isinstance(file, UploadFile):
        file_info = {"filename": file.filename, "size": len(await file.read())}
    return JSONResponse(
        {
            "method": request.method,
            "fields": {k: v for k, v in form.items() if isinstance(v, str)},
            "file": file_info,
        }
    )


def _build_app() -> Starlette:
    app = Starlette(routes=[Route("/echo", _echo, methods=["POST", "PUT", "DELETE"])])
    app.add_middleware(MethodOverrideMiddleware)
    return app


async def test_urlencoded_method_override_to_put() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=_build_app()), base_url="http://test"
    ) as client:
        response = await client.post("/echo", data={"_method": "PUT", "name": "Marie Curie"})
        assert response.status_code == 200
        body = response.json()
        assert body["method"] == "PUT"
        assert body["fields"]["name"] == "Marie Curie"


async def test_urlencoded_method_override_to_delete() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=_build_app()), base_url="http://test"
    ) as client:
        response = await client.post("/echo", data={"_method": "DELETE"})
        assert response.json()["method"] == "DELETE"


async def test_multipart_with_file_upload_survives_method_override() -> None:
    """The plan's explicit risk case: PUT via multipart/form-data with a
    file must read both the field AND the file correctly downstream."""
    async with AsyncClient(
        transport=ASGITransport(app=_build_app()), base_url="http://test"
    ) as client:
        response = await client.post(
            "/echo",
            data={"_method": "PUT", "name": "Marie Curie"},
            files={"avatar": ("photo.jpg", b"fake-image-bytes", "image/jpeg")},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["method"] == "PUT"
        assert body["fields"]["name"] == "Marie Curie"
        assert body["file"] == {"filename": "photo.jpg", "size": len(b"fake-image-bytes")}


async def test_no_method_override_field_keeps_post() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=_build_app()), base_url="http://test"
    ) as client:
        response = await client.post("/echo", data={"name": "Marie Curie"})
        assert response.json()["method"] == "POST"


async def test_unsupported_override_value_keeps_post() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=_build_app()), base_url="http://test"
    ) as client:
        response = await client.post("/echo", data={"_method": "PATCHXYZ", "name": "x"})
        assert response.json()["method"] == "POST"
