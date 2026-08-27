from admirable.domain.entities.story_snippet import StorySnippet
from admirable.infrastructure.db.models.story_snippet import StorySnippetModel


def to_entity(model: StorySnippetModel) -> StorySnippet:
    return StorySnippet(
        id=model.id,
        figure_id=model.figure_id,
        title=model.title,
        subtitle=model.subtitle,
        content_blocks=model.content_blocks or [],
        search_text=model.search_text or "",
        image_path=model.image_path,
        audio_path=model.audio_path,
        audio_status=model.audio_status,
        audio_error=model.audio_error,
        youtube_url=model.youtube_url,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def apply_to_model(entity: StorySnippet, model: StorySnippetModel) -> None:
    model.figure_id = entity.figure_id
    model.title = entity.title
    model.subtitle = entity.subtitle
    model.content_blocks = entity.content_blocks
    model.search_text = entity.search_text
    model.image_path = entity.image_path
    model.audio_path = entity.audio_path
    model.audio_status = entity.audio_status
    model.audio_error = entity.audio_error
    model.youtube_url = entity.youtube_url
