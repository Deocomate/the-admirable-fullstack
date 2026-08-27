"""Default mailer (matches Laravel's `MAIL_MAILER=log`): writes to the logger
instead of sending, so password-reset links are visible in dev without SMTP."""

import logging

logger = logging.getLogger("admirable.mail")


class LogMailer:
    async def send_password_reset(self, email: str, token: str) -> None:
        logger.info("Password reset requested for %s — token=%s", email, token)
