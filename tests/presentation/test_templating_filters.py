from admirable.presentation.web.templating import (
    _is_route,
    _number_format,
    _str_limit,
    _strip_tags,
    _youtube_embed_id,
)


def test_number_format_adds_thousands_separator() -> None:
    assert _number_format(1234567) == "1,234,567"


def test_number_format_zero_decimals_by_default() -> None:
    assert _number_format(42.9) == "43"


def test_str_limit_leaves_short_text_untouched() -> None:
    assert _str_limit("hello", limit=100) == "hello"


def test_str_limit_truncates_by_character_count_not_words() -> None:
    text = "a" * 105
    result = _str_limit(text, limit=100)
    assert result == "a" * 100 + "..."


def test_str_limit_handles_none() -> None:
    assert _str_limit(None) == ""


def test_strip_tags_removes_html() -> None:
    assert _strip_tags("<p>Hello <b>world</b></p>") == "Hello world"


def test_strip_tags_handles_none() -> None:
    assert _strip_tags(None) == ""


def test_youtube_embed_id_extracts_from_watch_url() -> None:
    assert _youtube_embed_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_youtube_embed_id_extracts_from_short_url() -> None:
    assert _youtube_embed_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_youtube_embed_id_extracts_from_embed_url() -> None:
    assert _youtube_embed_id("https://www.youtube.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_youtube_embed_id_returns_none_for_invalid_url() -> None:
    assert _youtube_embed_id("https://example.com/not-youtube") is None


def test_youtube_embed_id_returns_none_for_empty() -> None:
    assert _youtube_embed_id(None) is None


class _FakeRoute:
    def __init__(self, name: str) -> None:
        self.name = name


def test_is_route_exact_match() -> None:
    context = {"request": type("R", (), {"scope": {"route": _FakeRoute("admin.dashboard")}})()}
    assert _is_route(context, "admin.dashboard") is True


def test_is_route_wildcard_match() -> None:
    context = {"request": type("R", (), {"scope": {"route": _FakeRoute("admin.figures.index")}})()}
    assert _is_route(context, "admin.figures.*") is True


def test_is_route_wildcard_no_match() -> None:
    context = {"request": type("R", (), {"scope": {"route": _FakeRoute("admin.stories.index")}})()}
    assert _is_route(context, "admin.figures.*") is False


def test_is_route_none_safe_when_route_missing() -> None:
    context = {"request": type("R", (), {"scope": {}})()}
    assert _is_route(context, "admin.dashboard") is False
