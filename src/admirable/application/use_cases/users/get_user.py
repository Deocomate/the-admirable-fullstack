from admirable.application.dto.user_dto import UserDTO
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.user_repository import UserRepository


class GetUser:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(self, user_id: int) -> UserDTO:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise EntityNotFoundError("User", user_id)
        return UserDTO(
            id=user.id,  # type: ignore[arg-type]
            name=user.name,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
        )
