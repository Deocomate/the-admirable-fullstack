class FakeSettingRepository:
    def __init__(self) -> None:
        self._items: dict[str, str | None] = {}

    async def get(self, key: str) -> str | None:
        return self._items.get(key)

    async def set(self, key: str, value: str | None) -> None:
        self._items[key] = value
