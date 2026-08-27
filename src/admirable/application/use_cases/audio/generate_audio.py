"""Taskiq background worker use case for asynchronous audio generation.

Includes multiple cancellation checkpoints to safely abort TTS processing
and clean up generated files if cancelled by the user.
"""

from collections.abc import AsyncIterator
from typing import Protocol, cast

from admirable.application.dto.audio_dto import AudioActionCommand
from admirable.application.dto.files import UploadedFileDTO
from admirable.application.ports.clock_port import ClockPort
from admirable.application.ports.file_storage_port import FileStoragePort
from admirable.application.ports.text_to_speech_port import TextToSpeechPort
from admirable.domain.entities._audio_capable import AudioCapable
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository
from admirable.domain.value_objects.audio_status import AudioStatus
from admirable.domain.value_objects.content_block import ContentBlock, extract_english_text
from admirable.domain.value_objects.slug import Slug

from ._lookup import load_entity, save_entity

_ERROR_MESSAGE_LIMIT = 500


class _AudioSourceEntity(Protocol):
    """Figure and StorySnippet both have `content_blocks`, but AudioCapable
    itself doesn't declare it (it's shared by non-content entities too)."""

    content_blocks: list[ContentBlock]


class GenerateAudio:
    def __init__(
        self,
        figures: FigureRepository,
        story_snippets: StorySnippetRepository,
        tts: TextToSpeechPort,
        storage: FileStoragePort,
        clock: ClockPort,
    ) -> None:
        self._figures = figures
        self._story_snippets = story_snippets
        self._tts = tts
        self._storage = storage
        self._clock = clock

    async def execute(self, cmd: AudioActionCommand) -> None:
        entity = await load_entity(cmd.kind, cmd.entity_id, self._figures, self._story_snippets)
        if entity.audio_status != AudioStatus.PROCESSING:
            return

        try:
            content_blocks = cast(_AudioSourceEntity, entity).content_blocks
            text = extract_english_text(content_blocks)
            audio_bytes = await self._tts.synthesize(text)

            entity = await load_entity(cmd.kind, cmd.entity_id, self._figures, self._story_snippets)
            if entity.audio_status != AudioStatus.PROCESSING:
                return

            old_path = entity.audio_path
            new_path = await self._store_audio(cmd, entity, audio_bytes)

            entity = await load_entity(cmd.kind, cmd.entity_id, self._figures, self._story_snippets)
            if entity.audio_status != AudioStatus.PROCESSING:
                await self._storage.delete(new_path)
                return

            entity.mark_audio_completed(new_path)
            await save_entity(cmd.kind, entity, self._figures, self._story_snippets)
            if old_path != new_path:
                await self._storage.delete(old_path)
        except Exception as exc:
            entity = await load_entity(cmd.kind, cmd.entity_id, self._figures, self._story_snippets)
            entity.mark_audio_failed(str(exc)[:_ERROR_MESSAGE_LIMIT])
            await save_entity(cmd.kind, entity, self._figures, self._story_snippets)

    async def _store_audio(
        self, cmd: AudioActionCommand, entity: AudioCapable, audio_bytes: bytes
    ) -> str:
        name = getattr(entity, "name", None) or getattr(entity, "title", None) or "audio"
        slug = Slug.from_text(name).value
        directory = "uploads/audio" if cmd.kind == "figure" else "uploads/stories/audio"
        timestamp = int(self._clock.now().timestamp())
        filename = f"{slug}_{timestamp}.mp3"

        async def _stream() -> AsyncIterator[bytes]:
            yield audio_bytes

        upload = UploadedFileDTO(filename=filename, content_type="audio/mpeg", stream=_stream())
        return await self._storage.save(upload, directory, slug)
