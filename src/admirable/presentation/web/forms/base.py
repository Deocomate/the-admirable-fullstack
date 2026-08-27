"""Bridges Starlette form parsing to Pydantic command DTOs.

`unflatten_form_data` decodes Laravel's bracket-notation array fields
(`content_blocks[0][text_en]`, `key_facts[0][label]`, `category_ids[]`) —
the admin figures/stories JS still generates exactly this shape — into
nested dict/list structures a Pydantic model can validate directly.
"""

import re
from collections.abc import Sequence

from fastapi import UploadFile
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from starlette.datastructures import FormData
from starlette.requests import Request

from admirable.application.dto.files import UploadedFileDTO
from admirable.presentation.web.exceptions import FormValidationError

_KEY_RE = re.compile(r"^([^\[\]]+)((?:\[[^\]]*\])*)$")
_SEGMENT_RE = re.compile(r"\[([^\]]*)\]")


def _parse_key(raw_key: str) -> list[str]:
    match = _KEY_RE.match(raw_key)
    if not match:
        return [raw_key]
    base, rest = match.groups()
    return [base, *_SEGMENT_RE.findall(rest)]


def _assign(node: dict[str, object], segments: list[str], value: object) -> None:
    key = segments[0]
    if len(segments) == 1:
        node[key] = value
        return

    next_seg = segments[1]
    if next_seg == "":
        bucket = node.setdefault(key, [])
        assert isinstance(bucket, list)
        if len(segments) == 2:
            bucket.append(value)
        else:
            new_dict: dict[str, object] = {}
            _assign(new_dict, segments[2:], value)
            bucket.append(new_dict)
        return

    child = node.setdefault(key, {})
    assert isinstance(child, dict)
    _assign(child, segments[1:], value)


def _finalize(node: object) -> object:
    if isinstance(node, dict):
        finalized = {k: _finalize(v) for k, v in node.items()}
        if finalized and all(k.isdigit() for k in finalized):
            return [finalized[k] for k in sorted(finalized, key=int)]
        return finalized
    if isinstance(node, list):
        return [_finalize(v) for v in node]
    return node


def unflatten_form_data(items: Sequence[tuple[str, object]]) -> dict[str, object]:
    root: dict[str, object] = {}
    for raw_key, value in items:
        _assign(root, _parse_key(raw_key), value)
    result = _finalize(root)
    assert isinstance(result, dict)
    return result


def to_uploaded_file_dto(upload: UploadFile) -> UploadedFileDTO:
    async def _stream() -> object:
        while chunk := await upload.read(1024 * 1024):
            yield chunk

    return UploadedFileDTO(
        filename=upload.filename or "upload",
        content_type=upload.content_type or "application/octet-stream",
        stream=_stream(),  # type: ignore[arg-type]
    )


def _flashable_old_input(raw: dict[str, object]) -> dict[str, object]:
    """Drop file fields — an UploadFile can't be flashed into session/JSON."""
    return {k: v for k, v in raw.items() if not isinstance(v, UploadFile)}


async def parse_form[T: BaseModel](request: Request, model: type[T], redirect_to: str) -> T:
    form: FormData = await request.form()
    items = list(form.multi_items())
    raw = unflatten_form_data(items)

    try:
        return model.model_validate(raw)
    except PydanticValidationError as exc:
        errors: dict[str, list[str]] = {}
        for err in exc.errors():
            field = ".".join(str(p) for p in err["loc"])
            errors.setdefault(field, []).append(err["msg"])
        raise FormValidationError(errors, _flashable_old_input(raw), redirect_to) from exc
