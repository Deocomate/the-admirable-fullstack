from datetime import datetime

from pydantic import BaseModel

from admirable.application.dto.figure_dto import ContentBlockInput
from admirable.application.dto.files import UploadedFileDTO
from admirable.domain.value_objects.audio_status import AudioStatus


class CreateStoryCommand(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    figure_id: int
    title: str
    subtitle: str | None = None
    content_blocks: list[ContentBlockInput] = []
    youtube_url: str | None = None
    image: UploadedFileDTO | None = None
    audio: UploadedFileDTO | None = None


class UpdateStoryCommand(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    story_id: int
    figure_id: int
    title: str
    subtitle: str | None = None
    content_blocks: list[ContentBlockInput] = []
    youtube_url: str | None = None
    image: UploadedFileDTO | None = None
    audio: UploadedFileDTO | None = None


class StorySummaryDTO(BaseModel):
    id: int
    figure_id: int
    figure_name: str
    title: str
    subtitle: str | None


class StoryDetailDTO(BaseModel):
    id: int
    figure_id: int
    figure_name: str
    figure_slug: str
    figure_avatar_path: str | None = None
    title: str
    subtitle: str | None
    content_blocks: list[ContentBlockInput]
    image_path: str | None
    audio_path: str | None
    audio_status: AudioStatus
    audio_error: str | None
    youtube_url: str | None
    category_name: str | None = None
    category_slug: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
