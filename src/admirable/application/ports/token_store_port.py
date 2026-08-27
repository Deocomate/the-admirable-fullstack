from typing import Protocol


class TokenStorePort(Protocol):
    async def issue(self, email: str) -> str: ...

    async def consume(self, token: str) -> str | None: ...
