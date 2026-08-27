from pydantic import BaseModel

from admirable.application.dto.user_dto import UserDTO
from admirable.domain.repositories.user_repository import UserRepository


class ListUsersResult(BaseModel):
    items: list[UserDTO]
    total: int
    page: int
    per_page: int


class ListUsers:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(self, page: int = 1, per_page: int = 15) -> ListUsersResult:
        users = await self._users.list_all_admins(page, per_page)
        total = await self._users.count_all_admins()
        items = [
            UserDTO(
                id=u.id,  # type: ignore[arg-type]
                name=u.name,
                email=u.email,
                role=u.role,
                created_at=u.created_at,
            )
            for u in users
        ]
        return ListUsersResult(items=items, total=total, page=page, per_page=per_page)
