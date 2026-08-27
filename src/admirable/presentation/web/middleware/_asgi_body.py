"""Shared ASGI body drain/replay helpers used by method_override.py and csrf.py
(both need to read a form body without stealing it from the real handler)."""

from collections.abc import Awaitable, Callable

from starlette.types import Message, Receive, Scope


def header(scope: Scope, name: bytes) -> bytes:
    for key, value in scope.get("headers", []):
        if key.lower() == name:
            return bytes(value)
    return b""


async def drain_body(receive: Receive) -> bytes:
    chunks: list[bytes] = []
    more_body = True
    while more_body:
        message: Message = await receive()
        chunks.append(message.get("body", b""))
        more_body = message.get("more_body", False)
    return b"".join(chunks)


def replay(body: bytes) -> Callable[[], Awaitable[Message]]:
    sent = False

    async def receive() -> Message:
        nonlocal sent
        if not sent:
            sent = True
            return {"type": "http.request", "body": body, "more_body": False}
        return {"type": "http.disconnect"}

    return receive
