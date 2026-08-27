from admirable.application.dto.user_dto import UpdateUserCommand, UserDTO
from admirable.application.ports.password_hasher_port import PasswordHasherPort
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.user_repository import UserRepository


class UpdateUser:
    def __init__(self, users: UserRepository, hasher: PasswordHasherPort) -> None:
        self._users = users
        self._hasher = hasher

    async def execute(self, cmd: UpdateUserCommand) -> UserDTO:
        user = await self._users.get_by_id(cmd.user_id)
        if user is None:
            raise EntityNotFoundError("User", cmd.user_id)
        user.name = cmd.name
        user.email = cmd.email
        if cmd.password:
            user.password_hash = self._hasher.hash(cmd.password)
        updated = await self._users.update(user)
        return UserDTO(id=updated.id, name=updated.name, email=updated.email, role=updated.role)  # type: ignore[arg-type]
