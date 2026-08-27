from admirable.application.dto.public_dto import StoryDetailPageDTO, StorySummaryLite
from admirable.application.use_cases.stories._mapping import to_story_detail_dto
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository

_OTHER_STORIES_LIMIT = 3


class GetStoryDetail:
    def __init__(self, story_snippets: StorySnippetRepository, figures: FigureRepository) -> None:
        self._story_snippets = story_snippets
        self._figures = figures

    async def execute(self, story_id: int) -> StoryDetailPageDTO:
        snippet = await self._story_snippets.get_by_id(story_id)
        if snippet is None:
            raise EntityNotFoundError("StorySnippet", story_id)
        figure = await self._figures.get_by_id(snippet.figure_id)
        figure_name = figure.name if figure else ""

        others = await self._story_snippets.list_other_by_figure(
            snippet.figure_id, story_id, _OTHER_STORIES_LIMIT
        )
        other_dtos = [
            StorySummaryLite(id=o.id, title=o.title, subtitle=o.subtitle, image_path=o.image_path)  # type: ignore[arg-type]
            for o in others
        ]

        return StoryDetailPageDTO(
            snippet=to_story_detail_dto(snippet, figure_name=figure_name), other_stories=other_dtos
        )
