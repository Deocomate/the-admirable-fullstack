from pydantic import BaseModel

from admirable.application.dto.files import UploadedFileDTO
from admirable.domain.value_objects.audio_status import AudioStatus


class KeyFactInput(BaseModel):
    label: str
    value: str


class ContentBlockInput(BaseModel):
    type: str
    text_en: str = ""
    text_vi: str | None = None
    heading_en: str | None = None
    author: str | None = None


class CreateFigureCommand(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    name: str
    short_description: str | None = None
    key_facts: list[KeyFactInput] = []
    content_blocks: list[ContentBlockInput] = []
    youtube_url: str | None = None
    category_ids: list[int] = []
    avatar: UploadedFileDTO | None = None
    audio: UploadedFileDTO | None = None


class UpdateFigureCommand(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    figure_id: int
    name: str
    short_description: str | None = None
    key_facts: list[KeyFactInput] = []
    content_blocks: list[ContentBlockInput] = []
    youtube_url: str | None = None
    category_ids: list[int] = []
    avatar: UploadedFileDTO | None = None
    audio: UploadedFileDTO | None = None


class FigureSummaryDTO(BaseModel):
    id: int
    name: str
    slug: str
    avatar_path: str | None
    short_description: str | None
    category_names: list[str]
    story_snippets_count: int
    is_featured: bool = False
    audio_path: str | None = None
    youtube_url: str | None = None


class FigureDetailDTO(BaseModel):
    id: int
    name: str
    slug: str
    avatar_path: str | None
    short_description: str | None
    key_facts: list[KeyFactInput]
    content_blocks: list[ContentBlockInput]
    audio_path: str | None
    audio_status: AudioStatus
    audio_error: str | None
    youtube_url: str | None
    category_ids: list[int]
    category_names: list[str]
