from pydantic import BaseModel

from admirable.application.ports.task_queue_port import AudioKind
from admirable.domain.value_objects.audio_status import AudioStatus


class AudioActionCommand(BaseModel):
    kind: AudioKind
    entity_id: int


class AudioStatusDTO(BaseModel):
    status: AudioStatus
    error: str | None
    audio_url: str | None
