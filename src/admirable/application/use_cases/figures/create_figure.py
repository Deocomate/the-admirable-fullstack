from admirable.application.dto.figure_dto import CreateFigureCommand, FigureDetailDTO
from admirable.application.ports.file_storage_port import FileStoragePort
from admirable.domain.entities.figure import Figure
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.services.slug_generator import ensure_unique
from admirable.domain.value_objects.content_block import build_search_text
from admirable.domain.value_objects.key_fact import KeyFact
from admirable.domain.value_objects.slug import Slug

from ._mapping import to_domain_blocks, to_figure_detail_dto


class CreateFigure:
    def __init__(self, figures: FigureRepository, storage: FileStoragePort) -> None:
        self._figures = figures
        self._storage = storage

    async def execute(self, cmd: CreateFigureCommand) -> FigureDetailDTO:
        base_slug = Slug.from_text(cmd.name)
        slug = await ensure_unique(base_slug, self._figures.slug_exists)

        blocks = to_domain_blocks(cmd.content_blocks)
        key_facts = [KeyFact(label=f.label, value=f.value) for f in cmd.key_facts]

        figure = Figure(
            id=None,
            name=cmd.name,
            slug=slug.value,
            short_description=cmd.short_description,
            key_facts=key_facts,
            content_blocks=blocks,
            search_text=build_search_text(blocks),
            youtube_url=cmd.youtube_url,
        )

        if cmd.avatar is not None:
            figure.avatar_path = await self._storage.save(cmd.avatar, "uploads/avatars", slug.value)
        if cmd.audio is not None:
            path = await self._storage.save(cmd.audio, "uploads/audio", slug.value)
            figure.attach_audio_upload(path)

        created = await self._figures.add(figure)
        if cmd.category_ids:
            await self._figures.sync_categories(created.id, cmd.category_ids)  # type: ignore[arg-type]
            refreshed = await self._figures.get_by_id(created.id)  # type: ignore[arg-type]
            assert refreshed is not None
            created = refreshed

        return to_figure_detail_dto(created, category_names=[])
