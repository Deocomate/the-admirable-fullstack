"""Ports `StoreCategoryRequest`/`UpdateCategoryRequest`. The `unique:name`
rule needs a DB query, so it's enforced in the use case (see
`DuplicateValueError`), not here."""

from pydantic import BaseModel, Field

CATEGORY_FIELD_LABELS = {"name": "Tên lĩnh vực"}


class CategoryForm(BaseModel):
    name: str = Field(min_length=1, max_length=255)
