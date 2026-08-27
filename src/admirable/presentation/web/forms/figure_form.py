"""Figure form validation schema and field labels."""

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
