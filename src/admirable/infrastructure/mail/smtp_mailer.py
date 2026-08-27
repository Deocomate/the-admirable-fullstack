"""Real SMTP mailer, enabled by setting `MAIL__DRIVER=smtp`."""

from email.message import EmailMessage

import aiosmtplib


class SmtpMailer:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        from_address: str,
        from_name: str,
        base_url: str,
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._from_address = from_address
        self._from_name = from_name
        self._base_url = base_url

    async def send_password_reset(self, email: str, token: str) -> None:
        reset_url = f"{self._base_url}/admin/reset-password/{token}?email={email}"
        message = EmailMessage()
        message["From"] = f"{self._from_name} <{self._from_address}>"
        message["To"] = email
        message["Subject"] = "Password Reset Request"
        message.set_content(f"Reset your password: {reset_url}")

        await aiosmtplib.send(
            message,
            hostname=self._host,
            port=self._port,
            username=self._username or None,
            password=self._password or None,
            start_tls=True,
        )
