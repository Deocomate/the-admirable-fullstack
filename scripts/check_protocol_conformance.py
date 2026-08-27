"""Static-only check: assigns each repository implementation to its Protocol
type so mypy verifies structural conformance. Never imported at runtime.
"""

from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.contact_repository import ContactRepository
from admirable.domain.repositories.featured_figure_repository import FeaturedFigureRepository
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.setting_repository import SettingRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository
from admirable.domain.repositories.user_repository import UserRepository
from admirable.infrastructure.db.repositories.category_repository_impl import CategoryRepositoryImpl
from admirable.infrastructure.db.repositories.contact_repository_impl import ContactRepositoryImpl
from admirable.infrastructure.db.repositories.featured_figure_repository_impl import (
    FeaturedFigureRepositoryImpl,
)
from admirable.infrastructure.db.repositories.figure_repository_impl import FigureRepositoryImpl
from admirable.infrastructure.db.repositories.setting_repository_impl import SettingRepositoryImpl
from admirable.infrastructure.db.repositories.story_snippet_repository_impl import (
    StorySnippetRepositoryImpl,
)
from admirable.infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl


def _figure(impl: FigureRepositoryImpl) -> FigureRepository:
    return impl


def _story_snippet(impl: StorySnippetRepositoryImpl) -> StorySnippetRepository:
    return impl


def _category(impl: CategoryRepositoryImpl) -> CategoryRepository:
    return impl


def _featured_figure(impl: FeaturedFigureRepositoryImpl) -> FeaturedFigureRepository:
    return impl


def _contact(impl: ContactRepositoryImpl) -> ContactRepository:
    return impl


def _user(impl: UserRepositoryImpl) -> UserRepository:
    return impl


def _setting(impl: SettingRepositoryImpl) -> SettingRepository:
    return impl
