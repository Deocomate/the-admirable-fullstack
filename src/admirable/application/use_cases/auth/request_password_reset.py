from admirable.application.dto.auth_dto import RequestPasswordResetCommand
from admirable.application.ports.mailer_port import MailerPort
from admirable.application.ports.token_store_port import TokenStorePort
from admirable.domain.repositories.user_repository import UserRepository


class RequestPasswordReset:
    """Always succeeds from the caller's perspective — never reveals whether
    the email is registered."""

    def __init__(self, users: UserRepository, tokens: TokenStorePort, mailer: MailerPort) -> None:
        self._users = users
        self._tokens = tokens
        self._mailer = mailer

    async def execute(self, cmd: RequestPasswordResetCommand) -> None:
        user = await self._users.get_by_email(cmd.email)
        if user is None:
            return
        token = await self._tokens.issue(cmd.email)
        await self._mailer.send_password_reset(cmd.email, token)
