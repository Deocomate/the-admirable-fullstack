"""Server-side Redis session — deliberately not Starlette's SessionMiddleware,
which packs all state into the cookie and can't be invalidated server-side
(we dropped Laravel's `sessions` table, but logout must still be real).

The cookie holds only a signed session id. Session data lives at Redis key
`sess:{sid}` with a sliding TTL. Flash messages and validation old-input/
errors use a double buffer: a use case writes to `_next_*` this request: the
next request's Session.__init__ promotes `_next_*` to the readable `_flash`/
`_old`/`_errors`, and those display-only keys are dropped again before the
next save — so they're visible for exactly one subsequent request.
"""

import json
import secrets
from collections.abc import Iterator, MutableMapping
from typing import Any

import itsdangerous
from redis.asyncio import Redis
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

_KEY_PREFIX = "sess:"
_DISPLAY_ONLY_KEYS = ("_flash", "_old", "_errors")


class Session(MutableMapping[str, Any]):
    def __init__(self, sid: str, data: dict[str, Any]) -> None:
        self.sid = sid
        self.is_new = False
        self.regenerated = False
        self.invalidated = False
        self.ttl_override_seconds: int | None = None
        self._data = dict(data)
        self._data["_flash"] = self._data.pop("_next_flash", {})
        self._data["_old"] = self._data.pop("_next_old", {})
        self._data["_errors"] = self._data.pop("_next_errors", {})

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def flash(self, key: str, value: Any) -> None:
        self._data.setdefault("_next_flash", {})[key] = value

    def get_flash(self, key: str, default: Any = None) -> Any:
        flash: dict[str, Any] = self._data.get("_flash", {})
        return flash.get(key, default)

    def set_old_and_errors(self, old_input: dict[str, Any], errors: dict[str, list[str]]) -> None:
        self._data["_next_old"] = old_input
        self._data["_next_errors"] = errors

    def old(self, field: str, default: str = "") -> str:
        old_input: dict[str, Any] = self._data.get("_old", {})
        value = old_input.get(field, default)
        return str(value) if value is not None else default

    def old_raw(self, field: str, default: Any = None) -> Any:
        """Like `old()` but returns the value unconverted — for a nested
        field (`content_blocks`, `key_facts`) `unflatten_form_data` produced
        as a real list/dict, not a scalar. The whole session round-trips
        through `json.dumps`/`json.loads` (see `to_storage`), so this is
        still plain JSON-shaped data, just not coerced to `str`."""
        old_input: dict[str, Any] = self._data.get("_old", {})
        return old_input.get(field, default)

    @property
    def errors(self) -> dict[str, list[str]]:
        return dict(self._data.get("_errors", {}))

    def regenerate(self) -> None:
        self.regenerated = True

    def remember_for(self, seconds: int) -> None:
        """'Remember me': extend this session's TTL beyond the usual default
        (Laravel's `remember_token` column was dropped — this replaces it)."""
        self.ttl_override_seconds = seconds

    def invalidate(self) -> None:
        self.invalidated = True
        self._data.clear()

    def to_storage(self) -> dict[str, Any]:
        return {k: v for k, v in self._data.items() if k not in _DISPLAY_ONLY_KEYS}


class RedisSessionMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: Any,
        redis: Redis,
        secret_key: str,
        cookie_name: str = "admirable_session",
        ttl_seconds: int = 7200,
        secure: bool = True,
    ) -> None:
        super().__init__(app)
        self._redis = redis
        self._signer = itsdangerous.TimestampSigner(secret_key)
        self._cookie_name = cookie_name
        self._ttl = ttl_seconds
        self._secure = secure

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        sid = self._read_sid(request)
        data: dict[str, Any] = {}
        is_new = True
        if sid:
            raw = await self._redis.get(f"{_KEY_PREFIX}{sid}")
            if raw is not None:
                data = json.loads(raw)
                is_new = False
        if sid is None or is_new:
            sid = secrets.token_urlsafe(32)

        session = Session(sid, data)
        session.is_new = is_new
        request.state.session = session

        response = await call_next(request)

        if session.invalidated:
            await self._redis.delete(f"{_KEY_PREFIX}{session.sid}")
            response.delete_cookie(self._cookie_name)
            return response

        final_sid = session.sid
        if session.regenerated:
            await self._redis.delete(f"{_KEY_PREFIX}{session.sid}")
            final_sid = secrets.token_urlsafe(32)

        ttl = session.ttl_override_seconds or self._ttl
        await self._redis.set(f"{_KEY_PREFIX}{final_sid}", json.dumps(session.to_storage()), ex=ttl)
        response.set_cookie(
            self._cookie_name,
            self._sign(final_sid),
            httponly=True,
            samesite="lax",
            secure=self._secure,
            max_age=ttl,
        )
        return response

    def _read_sid(self, request: Request) -> str | None:
        raw_cookie = request.cookies.get(self._cookie_name)
        if not raw_cookie:
            return None
        try:
            # No max_age here: expiry is Redis's job (the TTL may be the
            # "remember me" 30-day override, not the default), the signer
            # only proves the cookie wasn't tampered with.
            unsigned = self._signer.unsign(raw_cookie)
        except itsdangerous.BadSignature:
            return None
        return unsigned.decode("utf-8")

    def _sign(self, sid: str) -> str:
        return self._signer.sign(sid.encode("utf-8")).decode("utf-8")
