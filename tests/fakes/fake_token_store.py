import uuid


class FakeTokenStore:
    def __init__(self) -> None:
        self._tokens: dict[str, str] = {}

    async def issue(self, email: str) -> str:
        token = uuid.uuid4().hex
        self._tokens[token] = email
        return token

    async def consume(self, token: str) -> str | None:
        return self._tokens.pop(token, None)
