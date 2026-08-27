"""Renders each macro with fake data and asserts no error plus the
Tailwind classes/markup that make it recognizably the ported component."""

from collections.abc import Callable

from starlette.requests import Request
from starlette.templating import Jinja2Templates


def _render(templates: Jinja2Templates, request: Request, source: str, **kwargs: object) -> str:
    return templates.env.from_string(source).render(request=request, **kwargs)


def test_figure_card_renders(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    figure = {
        "slug": "marie-curie",
        "name": "Marie Curie",
        "short_description": "Physicist and chemist.",
        "avatar_path": None,
        # `FigureSummaryDTO.category_names` is a flat list[str], not ORM
        # relation objects — matches the real Phase 9 DTO shape.
        "category_names": ["Khoa học"],
    }
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/cards.html" as cards with context %}'
        "{{ cards.figure_card(figure=figure, featured=True) }}",
        figure=figure,
    )
    assert "Marie Curie" in html
    assert "Khoa học" in html
    assert "card-hover" in html
    assert "Nổi bật" in html


def test_story_card_renders_without_subtitle(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    # `story` is always a lite DTO (id/title/subtitle/image_path) — no plain
    # `content` field exists post-DB-cleanup (Phase 3 dropped `content` for
    # `search_text`), so a missing subtitle renders no second line, not a
    # stripped-content fallback.
    story = {"id": 7, "title": "A Story", "subtitle": None}
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/cards.html" as cards with context %}'
        "{{ cards.story_card(story=story) }}",
        story=story,
    )
    assert "A Story" in html
    assert "Đọc mẩu chuyện" in html


def test_content_blocks_renders_heading_paragraph_quote(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    blocks = [
        {"type": "heading", "text_en": "Early life"},
        {"type": "paragraph", "text_en": "Born in Warsaw.", "text_vi": "Sinh ra ở Warsaw."},
        {"type": "quote", "text_en": "Nothing in life is to be feared.", "author": "Marie Curie"},
    ]
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/content.html" as content with context %}'
        "{{ content.content_blocks(blocks) }}",
        blocks=blocks,
    )
    assert "Early life" in html
    assert "Born in Warsaw." in html
    assert "Sinh ra ở Warsaw." in html
    assert "Nothing in life is to be feared." in html
    assert "Marie Curie" in html


def test_content_blocks_skips_empty_text(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    # Matches the Blade source exactly: the outer <article> wrapper is keyed
    # off whether the blocks list itself is non-empty, not whether any block
    # survives the per-block empty-text skip — so it still renders here,
    # just with no block content inside.
    blocks = [{"type": "paragraph", "text_en": "   "}]
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/content.html" as content with context %}'
        "{{ content.content_blocks(blocks) }}",
        blocks=blocks,
    )
    assert "<article" in html
    assert '<p class="text-[17px]' not in html


def test_audio_player_renders_when_path_present(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/media.html" as media with context %}'
        '{{ media.audio_player("audio/x.mp3") }}',
    )
    assert "data-audio-player" in html
    assert "/media/audio/x.mp3" in html


def test_audio_player_renders_nothing_without_path(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/media.html" as media with context %}'
        "{{ media.audio_player(None) }}",
    )
    assert html.strip() == ""


def test_category_pills_marks_active_slug(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    categories = [{"name": "Khoa học", "slug": "khoa-hoc"}, {"name": "Lịch sử", "slug": "lich-su"}]
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/nav.html" as nav with context %}'
        '{{ nav.category_pills(categories, "khoa-hoc") }}',
        categories=categories,
    )
    assert "Khoa học" in html
    assert "bg-apple-black text-white shadow-sm" in html


def test_pagination_hidden_for_single_page(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    from admirable.domain.value_objects.pagination import Page

    page = Page(items=[1, 2, 3], total=3, page=1, per_page=10)
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/nav.html" as nav with context %}'
        '{{ nav.pagination(page, "/x") }}',
        page=page,
    )
    assert html.strip() == ""


def test_pagination_renders_page_numbers_and_links(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    from admirable.domain.value_objects.pagination import Page

    page = Page(items=list(range(10)), total=50, page=2, per_page=10)
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/nav.html" as nav with context %}'
        '{{ nav.pagination(page, "/x") }}',
        page=page,
    )
    assert "/x?page=1" in html
    assert "/x?page=3" in html
    assert ">2<" in html


def test_share_buttons_escapes_url_via_tojson(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/nav.html" as nav with context %}'
        '{{ nav.share_buttons("http://x/y?a=1&b=2", "Title") }}',
    )
    assert "copyArticleLink(this," in html
    # tojson escapes "&" to & (safe inside the single-quoted JS-in-HTML
    # attribute) rather than leaving a raw "&" that plain interpolation would.
    assert "http://x/y?a=1\\u0026b=2" in html
    assert "http://x/y?a=1&b=2" not in html


def test_forms_text_input_shows_error(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/forms.html" as forms with context %}'
        '{{ forms.text_input("name", "Tên", "", {"name": ["Bắt buộc."]}, required=True) }}',
    )
    assert "border-red-400" in html
    assert "Bắt buộc." in html
    assert 'required' in html


def test_forms_checkbox_renders_hidden_fallback(
    templates: Jinja2Templates, make_request: Callable[..., Request]
) -> None:
    html = _render(
        templates,
        make_request("/"),
        '{% import "macros/forms.html" as forms with context %}'
        '{{ forms.checkbox("is_active", "Hiển thị", True) }}',
    )
    assert 'type="hidden" name="is_active" value="0"' in html
    assert "checked" in html
