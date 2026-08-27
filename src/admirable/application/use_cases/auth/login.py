from admirable.application.dto.auth_dto import AuthenticatedUserDTO, LoginCommand
from admirable.application.ports.password_hasher_port import PasswordHasherPort
from admirable.domain.exceptions import DomainError
from admirable.domain.repositories.user_repository import UserRepository


class InvalidCredentialsError(DomainError):
    def __init__(self) -> None:
        super().__init__("Invalid email or password")


class Login:
    """Authenticates credentials only — creating the session is presentation's job."""

    def __init__(self, users: UserRepository, hasher: PasswordHasherPort) -> None:
        self._users = users
        self._hasher = hasher

    async def execute(self, cmd: LoginCommand) -> AuthenticatedUserDTO:
        user = await self._users.get_by_email(cmd.email)
        if user is None or not self._hasher.verify(cmd.password, user.password_hash):
            raise InvalidCredentialsError()

        if self._hasher.needs_rehash(user.password_hash):
            user.password_hash = self._hasher.hash(cmd.password)
            await self._users.update(user)

        return AuthenticatedUserDTO(id=user.id, name=user.name, email=user.email, role=user.role)  # type: ignore[arg-type]
