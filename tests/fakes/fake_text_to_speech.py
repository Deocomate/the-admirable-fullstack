class FakeTextToSpeech:
    def __init__(
        self, result: bytes = b"fake-audio-bytes", raises: Exception | None = None
    ) -> None:
        self.result = result
        self.raises = raises
        self.calls: list[str] = []

    async def synthesize(self, text: str) -> bytes:
        self.calls.append(text)
        if self.raises is not None:
            raise self.raises
        return self.result
