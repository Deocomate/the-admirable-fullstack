"""Jinja2 template tree integrity tests."""

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TEMPLATES_DIR = _REPO_ROOT / "src/admirable/presentation/web/templates"


def test_exactly_one_safe_filter_usage_in_template_tree() -> None:
    """Ensure XSS protection by restricting raw HTML safe filter usage only to SEO JSON-LD."""
    matches = [
        path
        for path in _TEMPLATES_DIR.rglob("*.html")
        if "| safe" in path.read_text(encoding="utf-8")
    ]
    assert matches == [_TEMPLATES_DIR / "partials/client/seo-head.html"]
