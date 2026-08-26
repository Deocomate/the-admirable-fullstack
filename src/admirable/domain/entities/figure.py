from dataclasses import dataclass, field
from datetime import datetime

from admirable.domain.entities._audio_capable import AudioCapable
from admirable.domain.value_objects.audio_status import AudioStatus
from admirable.domain.value_objects.content_block import ContentBlock, build_search_text
from admirable.domain.value_objects.key_fact import KeyFact


@dataclass
class Figure(AudioCapable):
    id: int | None
    name: str
    slug: str
    short_description: str | None
    key_facts: list[KeyFact]
    content_blocks: list[ContentBlock]
    search_text: str
    avatar_path: str | None = None
    audio_path: str | None = None
    audio_status: AudioStatus = AudioStatus.IDLE
    audio_error: str | None = None
    youtube_url: str | None = None
    category_ids: list[int] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def rebuild_search_text(self) -> None:
        self.search_text = build_search_text(self.content_blocks)
