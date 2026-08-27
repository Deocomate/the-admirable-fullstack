"""Phase 8 success criterion: the ported CSS must be byte-identical to the
Blade source once the wrapping tag is stripped — "not one character of CSS
touched" is a stated absolute requirement, not just structural similarity."""

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_BLADE_STYLES = _REPO_ROOT / "resources/views/components/client/layout/styles.blade.php"
_JINJA_STYLES = (
    _REPO_ROOT / "src/admirable/presentation/web/templates/partials/client/styles.html"
)

_STYLE_RE = re.compile(r"<style>(.*)</style>", re.DOTALL)


def _inner_css(path: Path) -> str:
    match = _STYLE_RE.search(path.read_text(encoding="utf-8"))
    assert match is not None, f"no <style>...</style> block found in {path}"
    return match.group(1)


def test_styles_css_is_byte_identical_to_blade_source() -> None:
    assert _inner_css(_JINJA_STYLES) == _inner_css(_BLADE_STYLES)
