from admirable.application.dto.user_dto import CreateUserCommand, UserDTO
from admirable.application.ports.password_hasher_port import PasswordHasherPort
from admirable.domain.entities.user import User
from admirable.domain.exceptions import DuplicateValueError
from admirable.domain.repositories.user_repository import UserRepository
from admirable.domain.value_objects.role import Role


class CreateUser:
    """Always creates a plain `admin` — superadmin cannot be created via this UI."""

    def __init__(self, users: UserRepository, hasher: PasswordHasherPort) -> None:
        self._users = users
        self._hasher = hasher

    async def execute(self, cmd: CreateUserCommand) -> UserDTO:
        if await self._users.get_by_email(cmd.email) is not None:
            raise DuplicateValueError("email", cmd.email)
        user = User(
            id=None,
            name=cmd.name,
            email=cmd.email,
            password_hash=self._hasher.hash(cmd.password),
            role=Role.ADMIN,
        )
        created = await self._users.add(user)
        return UserDTO(
            id=created.id,  # type: ignore[arg-type]
            name=created.name,
            email=created.email,
            role=created.role,
            created_at=created.created_at,
        )
