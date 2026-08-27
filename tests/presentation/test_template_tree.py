"""Codifies two Phase 8 success criteria that are otherwise just manual
`grep`/`wc` commands in the plan, so CI keeps enforcing them."""

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TEMPLATES_DIR = _REPO_ROOT / "src/admirable/presentation/web/templates"
_CONVERSION_MAP = _REPO_ROOT / "docs/template-conversion-map.md"


def test_exactly_one_safe_filter_usage_in_template_tree() -> None:
    matches = [
        path
        for path in _TEMPLATES_DIR.rglob("*.html")
        if "| safe" in path.read_text(encoding="utf-8")
    ]
    assert matches == [_TEMPLATES_DIR / "partials/client/seo-head.html"]


def test_conversion_map_lists_all_84_blade_files() -> None:
    blade_files = sorted(
        p.relative_to(_REPO_ROOT / "resources/views").as_posix()
        for p in (_REPO_ROOT / "resources/views").rglob("*.blade.php")
    )
    assert len(blade_files) == 84

    doc = _CONVERSION_MAP.read_text(encoding="utf-8")
    listed = set(re.findall(r"`([\w./-]+\.blade\.php)`", doc))
    missing = [f for f in blade_files if f not in listed]
    assert not missing, f"conversion map is missing: {missing}"
