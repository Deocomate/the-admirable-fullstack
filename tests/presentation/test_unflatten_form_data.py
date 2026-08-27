"""Tests for unflatten_form_data converting multi-dimensional form fields into nested structures."""

from admirable.presentation.web.forms.base import unflatten_form_data


def test_simple_fields_pass_through() -> None:
    result = unflatten_form_data([("name", "Marie Curie"), ("youtube_url", "")])
    assert result == {"name": "Marie Curie", "youtube_url": ""}


def test_indexed_array_of_objects() -> None:
    items = [
        ("content_blocks[0][type]", "heading"),
        ("content_blocks[0][text_en]", "Early life"),
        ("content_blocks[1][type]", "paragraph"),
        ("content_blocks[1][text_en]", "Born in Warsaw."),
        ("content_blocks[1][text_vi]", "Sinh ra ở Warsaw."),
    ]
    result = unflatten_form_data(items)
    assert result["content_blocks"] == [
        {"type": "heading", "text_en": "Early life"},
        {"type": "paragraph", "text_en": "Born in Warsaw.", "text_vi": "Sinh ra ở Warsaw."},
    ]


def test_key_facts_array() -> None:
    items = [
        ("key_facts[0][label]", "Born"),
        ("key_facts[0][value]", "1867"),
        ("key_facts[1][label]", "Died"),
        ("key_facts[1][value]", "1934"),
    ]
    result = unflatten_form_data(items)
    assert result["key_facts"] == [
        {"label": "Born", "value": "1867"},
        {"label": "Died", "value": "1934"},
    ]


def test_repeated_empty_bracket_field_becomes_list() -> None:
    items = [
        ("category_ids[]", "3"),
        ("category_ids[]", "7"),
        ("category_ids[]", "12"),
    ]
    result = unflatten_form_data(items)
    assert result["category_ids"] == ["3", "7", "12"]


def test_full_real_figure_form_payload() -> None:
    """The exact shape a real figure-edit submission sends."""
    items: list[tuple[str, object]] = [
        ("name", "Marie Curie"),
        ("short_description", "Physicist and chemist."),
        ("youtube_url", ""),
        ("key_facts[0][label]", "Born"),
        ("key_facts[0][value]", "7 November 1867"),
        ("content_blocks[0][type]", "heading"),
        ("content_blocks[0][text_en]", "The Misfit Who Saw the Future"),
        ("content_blocks[1][type]", "quote"),
        ("content_blocks[1][text_en]", "Nothing in life is to be feared."),
        ("content_blocks[1][author]", "Marie Curie"),
        ("category_ids[]", "2"),
        ("category_ids[]", "5"),
    ]
    result = unflatten_form_data(items)

    assert result["name"] == "Marie Curie"
    assert result["key_facts"] == [{"label": "Born", "value": "7 November 1867"}]
    assert result["content_blocks"] == [
        {"type": "heading", "text_en": "The Misfit Who Saw the Future"},
        {"type": "quote", "text_en": "Nothing in life is to be feared.", "author": "Marie Curie"},
    ]
    assert result["category_ids"] == ["2", "5"]


def test_out_of_order_indices_are_sorted() -> None:
    items = [
        ("content_blocks[2][text_en]", "third"),
        ("content_blocks[0][text_en]", "first"),
        ("content_blocks[1][text_en]", "second"),
    ]
    result = unflatten_form_data(items)
    blocks = result["content_blocks"]
    assert isinstance(blocks, list)
    assert [b["text_en"] for b in blocks] == ["first", "second", "third"]
