from admirable.application.dto.user_dto import UserDTO
from admirable.domain.repositories.user_repository import UserRepository


class ListUsers:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(self, page: int = 1, per_page: int = 15) -> list[UserDTO]:
        users = await self._users.list_all_admins(page, per_page)
        return [UserDTO(id=u.id, name=u.name, email=u.email, role=u.role) for u in users]  # type: ignore[arg-type]
