"""Ports `StoreStorySnippetRequest`/`UpdateStorySnippetRequest` (identical
rules on both). `image`/`audio` files and the `figure_id.exists` DB check
aren't here — files come from `FormData` directly (see `forms/base.py`'s
`get_uploaded_file`), and the figure existence check happens in the use case
(`CreateStory`/`UpdateStory` already raise `EntityNotFoundError`)."""

from typing import Literal

from pydantic import BaseModel, Field

STORY_FIELD_LABELS = {
    "figure_id": "Nhân vật",
    "title": "Tiêu đề mẩu chuyện",
    "subtitle": "Phụ đề",
    "content_blocks": "Nội dung song ngữ",
    "youtube_url": "Link YouTube",
}


class StoryContentBlockForm(BaseModel):
    type: Literal["paragraph", "heading", "quote"]
    text_en: str = Field(min_length=1)
    text_vi: str | None = None
    heading_en: str | None = Field(default=None, max_length=500)
    author: str | None = Field(default=None, max_length=255)


class StoryForm(BaseModel):
    figure_id: int
    title: str = Field(min_length=1, max_length=255)
    subtitle: str | None = Field(default=None, max_length=500)
    content_blocks: list[StoryContentBlockForm] = Field(min_length=1)
    youtube_url: str | None = Field(default=None, max_length=500)
