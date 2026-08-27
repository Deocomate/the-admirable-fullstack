"""Implements TextToSpeechPort with edge-tts — no API key needed, unlike Azure."""

import asyncio

import edge_tts

from admirable.infrastructure.tts.text_chunker import chunk_text

_OVERALL_TIMEOUT_SECONDS = 150
_RETRIES_PER_CHUNK = 2
_RETRY_BACKOFF_SECONDS = 0.5


class TtsSynthesisError(Exception):
    pass


class EdgeTtsAdapter:
    def __init__(
        self,
        voice: str,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        max_chars_per_chunk: int = 3000,
    ) -> None:
        self._voice = voice
        self._rate = rate
        self._volume = volume
        self._pitch = pitch
        self._max_chars_per_chunk = max_chars_per_chunk

    async def synthesize(self, text: str) -> bytes:
        chunks = chunk_text(text, self._max_chars_per_chunk)
        if not chunks:
            raise TtsSynthesisError("No text available for audio generation.")

        async with asyncio.timeout(_OVERALL_TIMEOUT_SECONDS):
            parts = [await self._synthesize_chunk(chunk) for chunk in chunks]

        audio = b"".join(parts)
        if not audio:
            raise TtsSynthesisError("edge-tts returned no audio data.")
        return audio

    async def _synthesize_chunk(self, chunk: str) -> bytes:
        last_error: Exception | None = None
        for attempt in range(_RETRIES_PER_CHUNK + 1):
            try:
                return await self._request_chunk(chunk)
            except Exception as exc:
                last_error = exc
                if attempt < _RETRIES_PER_CHUNK:
                    await asyncio.sleep(_RETRY_BACKOFF_SECONDS)
        raise TtsSynthesisError(f"edge-tts request failed: {last_error}") from last_error

    async def _request_chunk(self, chunk: str) -> bytes:
        communicate = edge_tts.Communicate(
            chunk, voice=self._voice, rate=self._rate, volume=self._volume, pitch=self._pitch
        )
        buffer = bytearray()
        async for event in communicate.stream():
            if event["type"] == "audio":
                buffer.extend(event["data"])
        return bytes(buffer)
