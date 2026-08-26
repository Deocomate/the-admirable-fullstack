from admirable.domain.value_objects.content_block import (
    HeadingBlock,
    ParagraphBlock,
    QuoteBlock,
    build_search_text,
    extract_english_text,
    parse_content_blocks,
    serialize_content_blocks,
)


def test_parse_drops_blocks_with_blank_text() -> None:
    raw: list[dict[str, object]] = [
        {"type": "heading", "text_en": "  "},
        {"type": "paragraph", "text_en": "Hello"},
        {"type": "unknown", "text_en": "ignored"},
    ]
    blocks = parse_content_blocks(raw)
    assert len(blocks) == 1
    assert isinstance(blocks[0], ParagraphBlock)
    assert blocks[0].text_en == "Hello"


def test_parse_all_three_types() -> None:
    raw: list[dict[str, object]] = [
        {"type": "heading", "text_en": "Early life"},
        {"type": "paragraph", "text_en": "EN text", "text_vi": "VI text", "heading_en": "Sub"},
        {"type": "quote", "text_en": "Nothing in life is to be feared", "author": "Marie Curie"},
    ]
    blocks = parse_content_blocks(raw)
    assert isinstance(blocks[0], HeadingBlock)
    assert isinstance(blocks[1], ParagraphBlock)
    assert isinstance(blocks[2], QuoteBlock)


def test_serialize_round_trip() -> None:
    raw: list[dict[str, object]] = [{"type": "heading", "text_en": "Title"}]
    blocks = parse_content_blocks(raw)
    serialized = serialize_content_blocks(blocks)
    assert serialized == [{"type": "heading", "text_en": "Title"}]


def test_extract_english_text_excludes_vietnamese() -> None:
    blocks = parse_content_blocks(
        [{"type": "paragraph", "text_en": "English only", "text_vi": "Tieng Viet"}]
    )
    text = extract_english_text(blocks)
    assert "English only" in text
    assert "Tieng Viet" not in text


def test_build_search_text_includes_both_languages() -> None:
    blocks = parse_content_blocks(
        [{"type": "paragraph", "text_en": "English", "text_vi": "Vietnamese"}]
    )
    text = build_search_text(blocks)
    assert "English" in text
    assert "Vietnamese" in text


def test_quote_block_formatting() -> None:
    blocks = parse_content_blocks([{"type": "quote", "text_en": "Quote", "author": "Someone"}])
    text = build_search_text(blocks)
    assert text == '"Quote" — Someone'


def test_quote_block_without_author() -> None:
    blocks = parse_content_blocks([{"type": "quote", "text_en": "Quote"}])
    assert build_search_text(blocks) == '"Quote"'
    assert extract_english_text(blocks) == '"Quote"'


def test_serialize_paragraph_and_quote() -> None:
    blocks = parse_content_blocks(
        [
            {"type": "paragraph", "text_en": "EN", "text_vi": "VI", "heading_en": "H"},
            {"type": "quote", "text_en": "Q", "author": "A"},
        ]
    )
    serialized = serialize_content_blocks(blocks)
    assert serialized == [
        {"type": "paragraph", "text_en": "EN", "text_vi": "VI", "heading_en": "H"},
        {"type": "quote", "text_en": "Q", "author": "A"},
    ]


def test_parse_missing_type_dropped() -> None:
    blocks = parse_content_blocks([{"text_en": "orphan"}])
    assert blocks == []
