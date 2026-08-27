"""Development mailer adapter: writes email contents directly to the application logger."""

import logging

logger = logging.getLogger("admirable.mail")


class LogMailer:
    async def send_password_reset(self, email: str, token: str) -> None:
        logger.info("Password reset requested for %s — token=%s", email, token)
