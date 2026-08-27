from admirable.application.dto.story_dto import StoryDetailDTO
from admirable.domain.entities.story_snippet import StorySnippet


def to_story_detail_dto(snippet: StorySnippet, figure_name: str) -> StoryDetailDTO:
    from admirable.application.use_cases.figures._mapping import to_dto_blocks

    assert snippet.id is not None
    return StoryDetailDTO(
        id=snippet.id,
        figure_id=snippet.figure_id,
        figure_name=figure_name,
        title=snippet.title,
        subtitle=snippet.subtitle,
        content_blocks=to_dto_blocks(snippet.content_blocks),
        image_path=snippet.image_path,
        audio_path=snippet.audio_path,
        audio_status=snippet.audio_status,
        audio_error=snippet.audio_error,
        youtube_url=snippet.youtube_url,
    )
