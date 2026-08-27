class FakeMailer:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    async def send_password_reset(self, email: str, token: str) -> None:
        self.sent.append((email, token))
