"""Presentation tests for stylesheet and theme design tokens."""

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_JINJA_STYLES = _REPO_ROOT / "src/admirable/presentation/web/templates/partials/client/styles.html"
_STYLE_RE = re.compile(r"<style>(.*)</style>", re.DOTALL)


def _inner_css(path: Path) -> str:
    match = _STYLE_RE.search(path.read_text(encoding="utf-8"))
    assert match is not None, f"no <style>...</style> block found in {path}"
    return match.group(1)


def test_styles_template_is_valid_and_contains_design_system_tokens() -> None:
    assert _JINJA_STYLES.exists(), f"{_JINJA_STYLES} must exist"
    css = _inner_css(_JINJA_STYLES)
    assert len(css.strip()) > 0

    # Ensure key theme rules and tokens are present
    assert "scroll-behavior" in css
    assert "@keyframes" in css
    assert "card-hover" in css
    assert "prefers-reduced-motion" in css
