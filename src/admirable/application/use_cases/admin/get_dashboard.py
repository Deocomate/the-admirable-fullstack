from pydantic import BaseModel

from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository
from admirable.domain.repositories.user_repository import UserRepository


class DashboardStatsDTO(BaseModel):
    admins_count: int
    categories_count: int
    figures_count: int
    story_snippets_count: int


class GetDashboard:
    """Ports `AuthController::dashboard`'s stat cards — `admins_count` is
    fetched unconditionally; the router only shows that card to a
    superadmin, matching the Blade's `@if(auth()->user()->isSuperAdmin())`."""

    def __init__(
        self,
        users: UserRepository,
        categories: CategoryRepository,
        figures: FigureRepository,
        story_snippets: StorySnippetRepository,
    ) -> None:
        self._users = users
        self._categories = categories
        self._figures = figures
        self._story_snippets = story_snippets

    async def execute(self) -> DashboardStatsDTO:
        return DashboardStatsDTO(
            admins_count=await self._users.count_all_admins(),
            categories_count=await self._categories.count(),
            figures_count=await self._figures.count(),
            story_snippets_count=await self._story_snippets.count(),
        )
