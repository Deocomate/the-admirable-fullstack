from sqlalchemy import inspect as sa_inspect

from admirable.domain.entities.figure import Figure
from admirable.infrastructure.db.models.figure import FigureModel


def to_entity(model: FigureModel) -> Figure:
    category_loaded = "categories" not in sa_inspect(model).unloaded
    return Figure(
        id=model.id,
        name=model.name,
        slug=model.slug,
        short_description=model.short_description,
        key_facts=model.key_facts or [],
        content_blocks=model.content_blocks or [],
        search_text=model.search_text or "",
        avatar_path=model.avatar_path,
        audio_path=model.audio_path,
        audio_status=model.audio_status,
        audio_error=model.audio_error,
        youtube_url=model.youtube_url,
        category_ids=[c.id for c in model.categories] if category_loaded else [],
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def apply_to_model(entity: Figure, model: FigureModel) -> None:
    model.name = entity.name
    model.slug = entity.slug
    model.short_description = entity.short_description
    model.key_facts = entity.key_facts
    model.content_blocks = entity.content_blocks
    model.search_text = entity.search_text
    model.avatar_path = entity.avatar_path
    model.audio_path = entity.audio_path
    model.audio_status = entity.audio_status
    model.audio_error = entity.audio_error
    model.youtube_url = entity.youtube_url
