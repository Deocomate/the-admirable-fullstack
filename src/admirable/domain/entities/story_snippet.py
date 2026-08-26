from dataclasses import dataclass
from datetime import datetime

from admirable.domain.entities._audio_capable import AudioCapable
from admirable.domain.value_objects.audio_status import AudioStatus
from admirable.domain.value_objects.content_block import ContentBlock, build_search_text


@dataclass
class StorySnippet(AudioCapable):
    id: int | None
    figure_id: int
    title: str
    subtitle: str | None
    content_blocks: list[ContentBlock]
    search_text: str
    image_path: str | None = None
    audio_path: str | None = None
    audio_status: AudioStatus = AudioStatus.IDLE
    audio_error: str | None = None
    youtube_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def rebuild_search_text(self) -> None:
        self.search_text = build_search_text(self.content_blocks)
