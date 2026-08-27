from admirable.infrastructure.tts.text_chunker import chunk_text


def test_empty_text_returns_no_chunks() -> None:
    assert chunk_text("") == []
    assert chunk_text("   ") == []


def test_short_text_returns_single_chunk() -> None:
    assert chunk_text("Hello world.", max_chars=100) == ["Hello world."]


def test_never_splits_mid_word() -> None:
    text = "word " * 500  # 2500 chars
    chunks = chunk_text(text, max_chars=100)
    for chunk in chunks:
        assert not chunk.startswith(" ")
        assert not chunk.endswith(" ")
        for word in chunk.split(" "):
            assert word == "word" or word == ""


def test_all_chunks_within_limit() -> None:
    text = "This is a sentence. " * 1200  # ~24000 chars
    chunks = chunk_text(text, max_chars=3000)
    assert len(text) > 20000
    for chunk in chunks:
        assert len(chunk) <= 3000


def test_reassembled_chunks_preserve_all_words() -> None:
    text = "First sentence here. Second sentence here. Third one too."
    chunks = chunk_text(text, max_chars=30)
    reassembled_words = " ".join(chunks).split()
    original_words = text.split()
    assert reassembled_words == original_words


def test_single_sentence_longer_than_limit_hard_wraps() -> None:
    text = "word " * 50  # single "sentence" with no punctuation, 250 chars
    chunks = chunk_text(text.strip(), max_chars=50)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 50
