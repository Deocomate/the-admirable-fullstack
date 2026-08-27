"""Ports `StoreFigureRequest`/`UpdateFigureRequest` (identical rules on
both). `avatar`/`audio` files come from `FormData` directly (see
`forms/base.py`'s `get_uploaded_file`); `category_ids.*.exists` isn't
re-checked here — `sync_categories` only attaches ids that exist.

Unlike stories, a figure's `content_blocks.*.text_en` is `nullable` at the
Laravel validation layer — a block with blank `text_en` is dropped later by
`parse_content_blocks`/`to_domain_blocks`, not rejected outright."""

from pydantic import BaseModel, Field

FIGURE_FIELD_LABELS = {
    "name": "Tên nhân vật",
    "short_description": "Mô tả ngắn",
    "content_blocks": "Nội dung bài viết",
    "youtube_url": "Link YouTube",
}


class FigureKeyFactForm(BaseModel):
    label: str = ""
    value: str = ""


class FigureContentBlockForm(BaseModel):
    type: str
    text_en: str = ""
    text_vi: str | None = None
    heading_en: str | None = Field(default=None, max_length=500)
    author: str | None = Field(default=None, max_length=255)


class FigureForm(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    short_description: str | None = Field(default=None, max_length=1000)
    key_facts: list[FigureKeyFactForm] = []
    content_blocks: list[FigureContentBlockForm] = Field(min_length=1)
    youtube_url: str | None = Field(default=None, max_length=500)
    category_ids: list[int] = []
