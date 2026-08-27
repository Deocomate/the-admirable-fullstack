from admirable.application.dto.figure_dto import FigureDetailDTO, UpdateFigureCommand
from admirable.application.ports.file_storage_port import FileStoragePort
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.services.slug_generator import ensure_unique
from admirable.domain.value_objects.content_block import build_search_text
from admirable.domain.value_objects.key_fact import KeyFact
from admirable.domain.value_objects.slug import Slug

from ._mapping import to_domain_blocks, to_figure_detail_dto


class UpdateFigure:
    def __init__(self, figures: FigureRepository, storage: FileStoragePort) -> None:
        self._figures = figures
        self._storage = storage

    async def execute(self, cmd: UpdateFigureCommand) -> FigureDetailDTO:
        figure = await self._figures.get_by_id(cmd.figure_id)
        if figure is None:
            raise EntityNotFoundError("Figure", cmd.figure_id)

        new_slug_candidate = Slug.from_text(cmd.name)
        if new_slug_candidate.value != figure.slug:
            # Only regenerate the slug when the name actually changed — keeps
            # existing URLs/SEO stable across unrelated edits.
            unique_slug = await ensure_unique(new_slug_candidate, self._figures.slug_exists)
            figure.slug = unique_slug.value

        figure.name = cmd.name
        figure.short_description = cmd.short_description
        figure.key_facts = [KeyFact(label=f.label, value=f.value) for f in cmd.key_facts]
        figure.content_blocks = to_domain_blocks(cmd.content_blocks)
        figure.search_text = build_search_text(figure.content_blocks)
        figure.youtube_url = cmd.youtube_url

        if cmd.avatar is not None:
            await self._storage.delete(figure.avatar_path)
            avatar_path = await self._storage.save(cmd.avatar, "uploads/avatars", figure.slug)
            figure.avatar_path = avatar_path
        if cmd.audio is not None:
            await self._storage.delete(figure.audio_path)
            path = await self._storage.save(cmd.audio, "uploads/audio", figure.slug)
            figure.attach_audio_upload(path)

        await self._figures.update(figure)
        await self._figures.sync_categories(cmd.figure_id, cmd.category_ids)
        refreshed = await self._figures.get_by_id(cmd.figure_id)
        assert refreshed is not None
        return to_figure_detail_dto(refreshed, category_names=[])
