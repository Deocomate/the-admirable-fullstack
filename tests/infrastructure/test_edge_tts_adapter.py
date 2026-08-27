import pytest

from admirable.infrastructure.tts.edge_tts_adapter import EdgeTtsAdapter, TtsSynthesisError


async def test_empty_text_raises() -> None:
    adapter = EdgeTtsAdapter(voice="en-US-AriaNeural")
    with pytest.raises(TtsSynthesisError):
        await adapter.synthesize("   ")


async def test_retries_transient_failure_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    adapter = EdgeTtsAdapter(voice="en-US-AriaNeural")
    attempts = {"count": 0}

    async def flaky_request(chunk: str) -> bytes:
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise ConnectionError("transient network blip")
        return b"audio-bytes"

    monkeypatch.setattr(adapter, "_request_chunk", flaky_request)
    result = await adapter.synthesize("Hello world.")

    assert result == b"audio-bytes"
    assert attempts["count"] == 2


async def test_gives_up_after_retries_exhausted(monkeypatch: pytest.MonkeyPatch) -> None:
    adapter = EdgeTtsAdapter(voice="en-US-AriaNeural")

    async def always_fails(chunk: str) -> bytes:
        raise ConnectionError("persistent failure")

    monkeypatch.setattr(adapter, "_request_chunk", always_fails)

    with pytest.raises(TtsSynthesisError):
        await adapter.synthesize("Hello world.")


async def test_joins_chunks_in_order(monkeypatch: pytest.MonkeyPatch) -> None:
    adapter = EdgeTtsAdapter(voice="en-US-AriaNeural", max_chars_per_chunk=10)
    seen_chunks: list[str] = []

    async def fake_request(chunk: str) -> bytes:
        seen_chunks.append(chunk)
        return chunk.encode()

    monkeypatch.setattr(adapter, "_request_chunk", fake_request)
    result = await adapter.synthesize("First sentence. Second sentence. Third sentence.")

    assert result == "".join(seen_chunks).encode()
    assert len(seen_chunks) > 1


@pytest.mark.network
async def test_synthesize_real_short_sentence_produces_playable_mp3() -> None:
    """Opt-in network smoke test — skipped by default (see pyproject.toml
    addopts). Run explicitly with: uv run pytest -m network"""
    adapter = EdgeTtsAdapter(voice="en-US-AriaNeural")
    audio = await adapter.synthesize("This is a short test sentence for audio generation.")
    assert len(audio) > 1024
    assert audio[:2] in (b"ID", b"\xff\xfb", b"\xff\xf3", b"\xff\xfa")  # MP3/ID3 signature
