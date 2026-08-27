from admirable.application.dto.auth_dto import ResetPasswordCommand
from admirable.application.ports.password_hasher_port import PasswordHasherPort
from admirable.application.ports.token_store_port import TokenStorePort
from admirable.domain.exceptions import DomainError
from admirable.domain.repositories.user_repository import UserRepository


class InvalidResetTokenError(DomainError):
    def __init__(self) -> None:
        super().__init__("Invalid or expired password reset token")


class ResetPassword:
    def __init__(
        self, users: UserRepository, tokens: TokenStorePort, hasher: PasswordHasherPort
    ) -> None:
        self._users = users
        self._tokens = tokens
        self._hasher = hasher

    async def execute(self, cmd: ResetPasswordCommand) -> None:
        email = await self._tokens.consume(cmd.token)
        if email is None or email != cmd.email:
            raise InvalidResetTokenError()

        user = await self._users.get_by_email(email)
        if user is None:
            raise InvalidResetTokenError()

        user.password_hash = self._hasher.hash(cmd.password)
        await self._users.update(user)
