"""Splits long text into TTS-safe chunks, breaking at sentence boundaries
(never mid-word) so edge-tts requests stay under its practical length limit."""

import re

_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+|\n+")


def chunk_text(text: str, max_chars: int = 3000) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    sentences = [s for s in _SENTENCE_BOUNDARY.split(text) if s]
    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        if len(sentence) > max_chars:
            # A single sentence longer than the limit: hard-wrap on words.
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(_wrap_long_sentence(sentence, max_chars))
            continue

        candidate = f"{current} {sentence}".strip() if current else sentence
        if len(candidate) > max_chars:
            chunks.append(current)
            current = sentence
        else:
            current = candidate

    if current:
        chunks.append(current)
    return chunks


def _wrap_long_sentence(sentence: str, max_chars: int) -> list[str]:
    words = sentence.split(" ")
    chunks: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip() if current else word
        if len(candidate) > max_chars:
            if current:
                chunks.append(current)
            current = word
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks
