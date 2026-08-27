from admirable.domain.entities.user import User


class FakeUserRepository:
    def __init__(self) -> None:
        self._items: dict[int, User] = {}
        self._next_id = 1

    async def get_by_id(self, user_id: int) -> User | None:
        return self._items.get(user_id)

    async def get_by_email(self, email: str) -> User | None:
        return next((u for u in self._items.values() if u.email == email), None)

    async def list_all_admins(self, page: int, per_page: int) -> list[User]:
        items = list(self._items.values())
        start = (page - 1) * per_page
        return items[start : start + per_page]

    async def count_all_admins(self) -> int:
        return len(self._items)

    async def add(self, user: User) -> User:
        user.id = self._next_id
        self._next_id += 1
        self._items[user.id] = user
        return user

    async def update(self, user: User) -> User:
        assert user.id is not None
        self._items[user.id] = user
        return user

    async def delete(self, user_id: int) -> None:
        self._items.pop(user_id, None)
