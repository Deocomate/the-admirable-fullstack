"""Architecture layer boundary verification using AST analysis.

Enforces Clean Architecture dependency rules:
- Domain layer must not depend on application, infrastructure, presentation,
  or external frameworks (FastAPI, SQLAlchemy, Pydantic, Redis, TaskIQ, Jinja2).
- Application layer must not depend on infrastructure, presentation,
  or external frameworks (FastAPI, SQLAlchemy, Redis, TaskIQ, Jinja2).
- Infrastructure layer must not depend on presentation layer.
"""

import ast
from pathlib import Path

FORBIDDEN_DEPENDENCIES: dict[str, list[str]] = {
    "admirable.domain": [
        "fastapi",
        "sqlalchemy",
        "pydantic",
        "redis",
        "taskiq",
        "taskiq_redis",
        "jinja2",
        "starlette",
        "admirable.application",
        "admirable.infrastructure",
        "admirable.presentation",
    ],
    "admirable.application": [
        "fastapi",
        "sqlalchemy",
        "redis",
        "taskiq",
        "taskiq_redis",
        "jinja2",
        "starlette",
        "admirable.infrastructure",
        "admirable.presentation",
    ],
    "admirable.infrastructure": [
        "admirable.presentation",
        "fastapi",
        "starlette",
        "jinja2",
    ],
}


def _get_imports(file_path: Path) -> list[str]:
    """Parse a python file using ast and extract all top-level imported module names."""
    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    except Exception as exc:
        raise RuntimeError(f"Failed to parse AST for {file_path}: {exc}") from exc

    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def _check_violations(layer_pkg: str, forbidden_list: list[str]) -> list[str]:
    violations: list[str] = []
    rel_path = layer_pkg.replace(".", "/")
    layer_dir = Path("src") / rel_path

    if not layer_dir.exists():
        return violations

    for py_file in layer_dir.rglob("*.py"):
        if py_file.name == "__pycache__":
            continue
        file_imports = _get_imports(py_file)
        for imp in file_imports:
            for forbidden in forbidden_list:
                if imp == forbidden or imp.startswith(f"{forbidden}."):
                    violations.append(
                        f"Layer violation in {py_file}: imports '{imp}' (prohibited: '{forbidden}')"
                    )
    return violations


def test_domain_layer_has_no_forbidden_imports() -> None:
    violations = _check_violations("admirable.domain", FORBIDDEN_DEPENDENCIES["admirable.domain"])
    assert not violations, "\n".join(violations)


def test_application_layer_has_no_forbidden_imports() -> None:
    violations = _check_violations(
        "admirable.application", FORBIDDEN_DEPENDENCIES["admirable.application"]
    )
    assert not violations, "\n".join(violations)


def test_infrastructure_layer_has_no_forbidden_imports() -> None:
    violations = _check_violations(
        "admirable.infrastructure", FORBIDDEN_DEPENDENCIES["admirable.infrastructure"]
    )
    assert not violations, "\n".join(violations)
