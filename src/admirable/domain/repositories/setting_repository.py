from typing import Protocol


class SettingRepository(Protocol):
    async def get(self, key: str) -> str | None: ...

    async def set(self, key: str, value: str | None) -> None: ...
