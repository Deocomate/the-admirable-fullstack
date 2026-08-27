from admirable.application.dto.story_dto import StoryDetailDTO
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository

from ._mapping import to_story_detail_dto


class GetStory:
    def __init__(self, story_snippets: StorySnippetRepository, figures: FigureRepository) -> None:
        self._story_snippets = story_snippets
        self._figures = figures

    async def execute(self, story_id: int) -> StoryDetailDTO:
        snippet = await self._story_snippets.get_by_id(story_id)
        if snippet is None:
            raise EntityNotFoundError("StorySnippet", story_id)
        figure = await self._figures.get_by_id(snippet.figure_id)
        figure_name = figure.name if figure else ""
        return to_story_detail_dto(snippet, figure_name=figure_name)
