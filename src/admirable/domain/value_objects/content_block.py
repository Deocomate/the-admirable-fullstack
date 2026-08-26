"""content_blocks value objects.

Mirrors the JSON schema currently produced by the admin form JS
(`content_blocks[idx][text_en]`, ...) and consumed by `FigureService` /
`StorySnippetService` on the Laravel side. Kept byte-for-byte compatible so
existing rows need no data conversion.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class HeadingBlock:
    text_en: str
    type: Literal["heading"] = "heading"


@dataclass(frozen=True)
class ParagraphBlock:
    text_en: str
    text_vi: str | None = None
    heading_en: str | None = None
    type: Literal["paragraph"] = "paragraph"


@dataclass(frozen=True)
class QuoteBlock:
    text_en: str
    author: str | None = None
    type: Literal["quote"] = "quote"


ContentBlock = HeadingBlock | ParagraphBlock | QuoteBlock


def parse_content_blocks(raw: list[dict[str, object]]) -> list[ContentBlock]:
    """Parse raw JSON blocks, silently dropping malformed ones.

    Matches `FigureService::normalizeContentBlocks`: a block survives only if
    its `text_en` is non-blank after stripping whitespace.
    """
    blocks: list[ContentBlock] = []
    for raw_block in raw:
        block_type = raw_block.get("type")
        text_en = str(raw_block.get("text_en") or "").strip()
        if not text_en:
            continue
        if block_type == "heading":
            blocks.append(HeadingBlock(text_en=text_en))
        elif block_type == "paragraph":
            text_vi_raw = raw_block.get("text_vi")
            heading_en_raw = raw_block.get("heading_en")
            blocks.append(
                ParagraphBlock(
                    text_en=text_en,
                    text_vi=str(text_vi_raw) if text_vi_raw else None,
                    heading_en=str(heading_en_raw) if heading_en_raw else None,
                )
            )
        elif block_type == "quote":
            author_raw = raw_block.get("author")
            author = str(author_raw) if author_raw else None
            blocks.append(QuoteBlock(text_en=text_en, author=author))
    return blocks


def serialize_content_blocks(blocks: list[ContentBlock]) -> list[dict[str, object]]:
    """Serialize back to the JSON shape stored in `figures.content_blocks`."""
    result: list[dict[str, object]] = []
    for block in blocks:
        if isinstance(block, HeadingBlock):
            result.append({"type": "heading", "text_en": block.text_en})
        elif isinstance(block, ParagraphBlock):
            result.append(
                {
                    "type": "paragraph",
                    "text_en": block.text_en,
                    "text_vi": block.text_vi,
                    "heading_en": block.heading_en,
                }
            )
        elif isinstance(block, QuoteBlock):
            result.append({"type": "quote", "text_en": block.text_en, "author": block.author})
    return result


def extract_english_text(blocks: list[ContentBlock]) -> str:
    """English-only text for TTS synthesis (mirrors `AzureTextToSpeechService` input)."""
    parts: list[str] = []
    for block in blocks:
        if isinstance(block, HeadingBlock):
            parts.append(block.text_en)
        elif isinstance(block, ParagraphBlock):
            if block.heading_en:
                parts.append(block.heading_en)
            parts.append(block.text_en)
        elif isinstance(block, QuoteBlock):
            quoted = f'"{block.text_en}"'
            parts.append(f"{quoted} — {block.author}" if block.author else quoted)
    return "\n\n".join(parts)


def build_search_text(blocks: list[ContentBlock]) -> str:
    """EN + VI plain text used for the `search_text` column (was `buildPlainContent`)."""
    parts: list[str] = []
    for block in blocks:
        if isinstance(block, HeadingBlock):
            parts.append(block.text_en)
        elif isinstance(block, ParagraphBlock):
            if block.heading_en:
                parts.append(block.heading_en)
            parts.append(block.text_en)
            if block.text_vi:
                parts.append(block.text_vi)
        elif isinstance(block, QuoteBlock):
            quoted = f'"{block.text_en}"'
            parts.append(f"{quoted} — {block.author}" if block.author else quoted)
    return "\n\n".join(parts)
