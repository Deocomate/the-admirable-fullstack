from admirable.application.ports.task_queue_port import AudioKind
from admirable.domain.entities._audio_capable import AudioCapable
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository


async def load_entity(
    kind: AudioKind,
    entity_id: int,
    figures: FigureRepository,
    story_snippets: StorySnippetRepository,
) -> AudioCapable:
    entity: AudioCapable | None
    if kind == "figure":
        entity = await figures.get_by_id(entity_id)
    else:
        entity = await story_snippets.get_by_id(entity_id)
    if entity is None:
        raise EntityNotFoundError(kind, entity_id)
    return entity


async def save_entity(
    kind: AudioKind,
    entity: AudioCapable,
    figures: FigureRepository,
    story_snippets: StorySnippetRepository,
) -> None:
    if kind == "figure":
        await figures.update(entity)  # type: ignore[arg-type]
    else:
        await story_snippets.update(entity)  # type: ignore[arg-type]
