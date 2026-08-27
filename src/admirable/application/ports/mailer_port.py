from typing import Protocol


class MailerPort(Protocol):
    async def send_password_reset(self, email: str, token: str) -> None: ...
