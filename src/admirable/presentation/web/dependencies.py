"""FastAPI dependency providers. Routers never construct a repository or
adapter directly — everything comes from `get_container`, the same factory
the worker uses (see `infrastructure/container.py`).

Pattern for a new router: add a small `get_<use_case>_uc` provider here that
takes `Container = Depends(get_container)` and returns the constructed use
case. Phase 9/10 routers follow this same pattern for their own use cases.
"""

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from fastapi.params import Depends as DependsParam
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from admirable.application.dto.auth_dto import AuthenticatedUserDTO
from admirable.application.use_cases.admin.get_dashboard import GetDashboard
from admirable.application.use_cases.audio.cancel_audio_generation import CancelAudioGeneration
from admirable.application.use_cases.audio.get_audio_status import GetAudioStatus
from admirable.application.use_cases.audio.request_audio_generation import RequestAudioGeneration
from admirable.application.use_cases.auth.login import Login
from admirable.application.use_cases.auth.request_password_reset import RequestPasswordReset
from admirable.application.use_cases.auth.reset_password import ResetPassword
from admirable.application.use_cases.categories.create_category import CreateCategory
from admirable.application.use_cases.categories.delete_category import DeleteCategory
from admirable.application.use_cases.categories.get_category import GetCategory
from admirable.application.use_cases.categories.list_categories import (
    ListCategories as ListCategoriesAdmin,
)
from admirable.application.use_cases.categories.update_category import UpdateCategory
from admirable.application.use_cases.contacts.create_contact import CreateContact
from admirable.application.use_cases.contacts.delete_contact import DeleteContact
from admirable.application.use_cases.contacts.get_contact import GetContact
from admirable.application.use_cases.contacts.list_contacts import ListContacts
from admirable.application.use_cases.contacts.update_contact import UpdateContact
from admirable.application.use_cases.featured.add_featured import AddFeatured
from admirable.application.use_cases.featured.list_featured import ListFeatured
from admirable.application.use_cases.featured.remove_featured import RemoveFeatured
from admirable.application.use_cases.featured.reorder_featured import ReorderFeatured
from admirable.application.use_cases.figures.create_figure import CreateFigure
from admirable.application.use_cases.figures.delete_figure import DeleteFigure
from admirable.application.use_cases.figures.get_figure import GetFigure
from admirable.application.use_cases.figures.list_figures import ListFigures
from admirable.application.use_cases.figures.update_figure import UpdateFigure
from admirable.application.use_cases.public.get_about_us_page import GetAboutUsPage
from admirable.application.use_cases.public.get_category_page import GetCategoryPage
from admirable.application.use_cases.public.get_contact_page import GetContactPage
from admirable.application.use_cases.public.get_figure_detail import GetFigureDetail
from admirable.application.use_cases.public.get_home_page import GetHomePage
from admirable.application.use_cases.public.get_story_detail import GetStoryDetail
from admirable.application.use_cases.public.list_categories import ListCategories
from admirable.application.use_cases.public.search_figures import SearchFigures
from admirable.application.use_cases.settings.get_about_us import GetAboutUs
from admirable.application.use_cases.settings.update_about_us import UpdateAboutUs
from admirable.application.use_cases.stories.create_story import CreateStory
from admirable.application.use_cases.stories.delete_story import DeleteStory
from admirable.application.use_cases.stories.get_story import GetStory
from admirable.application.use_cases.stories.list_stories import ListStories
from admirable.application.use_cases.stories.update_story import UpdateStory
from admirable.application.use_cases.users.create_user import CreateUser
from admirable.application.use_cases.users.delete_user import DeleteUser
from admirable.application.use_cases.users.get_user import GetUser
from admirable.application.use_cases.users.list_users import ListUsers
from admirable.application.use_cases.users.update_user import UpdateUser
from admirable.config import Settings, get_settings
from admirable.domain.value_objects.role import Role
from admirable.infrastructure.container import Container, build_request_scope
from admirable.infrastructure.db.session import session_scope
from admirable.presentation.web.exceptions import (
    AlreadyAuthenticatedError,
    ForbiddenError,
    NotAuthenticatedError,
)
from admirable.presentation.web.middleware.session import Session


def get_settings_dep() -> Settings:
    return get_settings()


async def get_redis(request: Request) -> Redis:
    return request.app.state.redis  # type: ignore[no-any-return]


async def get_db_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with session_scope(request.app.state.session_factory) as session:
        yield session


async def get_container(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    settings: Annotated[Settings, Depends(get_settings_dep)],
    redis: Annotated[Redis, Depends(get_redis)],
) -> Container:
    return build_request_scope(session, settings, redis)


def get_session(request: Request) -> Session:
    session = getattr(request.state, "session", None)
    if session is None:
        raise RuntimeError("RedisSessionMiddleware is not installed")
    return session  # type: ignore[no-any-return]


async def get_current_user(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    container: Annotated[Container, Depends(get_container)],
) -> AuthenticatedUserDTO | None:
    user_id = session.get("user_id")
    user_dto: AuthenticatedUserDTO | None = None
    if user_id is not None:
        user = await container.users.get_by_id(user_id)
        if user is not None:
            user_dto = AuthenticatedUserDTO(
                id=user.id,  # type: ignore[arg-type]
                name=user.name,
                email=user.email,
                role=user.role,
            )
    # Cached on request.state so the `current_user()` Jinja global (which has
    # no way to await a DB call) can read it without a second lookup.
    request.state.current_user = user_dto
    return user_dto


async def require_auth(
    current_user: Annotated[AuthenticatedUserDTO | None, Depends(get_current_user)],
) -> AuthenticatedUserDTO:
    if current_user is None:
        raise NotAuthenticatedError()
    return current_user


async def require_guest(
    current_user: Annotated[AuthenticatedUserDTO | None, Depends(get_current_user)],
) -> None:
    if current_user is not None:
        raise AlreadyAuthenticatedError()


def require_role(*roles: Role) -> DependsParam:
    async def _dependency(
        user: Annotated[AuthenticatedUserDTO, Depends(require_auth)],
    ) -> AuthenticatedUserDTO:
        if user.role not in roles:
            raise ForbiddenError()
        return user

    return Depends(_dependency)  # type: ignore[no-any-return]


async def get_login_use_case(container: Annotated[Container, Depends(get_container)]) -> Login:
    return Login(container.users, container.hasher)


async def get_dashboard_uc(
    container: Annotated[Container, Depends(get_container)],
) -> GetDashboard:
    return GetDashboard(
        container.users, container.categories, container.figures, container.story_snippets
    )


async def get_request_password_reset_use_case(
    container: Annotated[Container, Depends(get_container)],
) -> RequestPasswordReset:
    return RequestPasswordReset(container.users, container.tokens, container.mailer)


async def get_reset_password_use_case(
    container: Annotated[Container, Depends(get_container)],
) -> ResetPassword:
    return ResetPassword(container.users, container.tokens, container.hasher)


async def get_home_page_uc(container: Annotated[Container, Depends(get_container)]) -> GetHomePage:
    return GetHomePage(
        container.figures, container.categories, container.story_snippets, container.featured
    )


async def get_list_categories_uc(
    container: Annotated[Container, Depends(get_container)],
) -> ListCategories:
    return ListCategories(container.categories)


async def get_category_page_uc(
    container: Annotated[Container, Depends(get_container)],
) -> GetCategoryPage:
    return GetCategoryPage(container.figures, container.categories, container.story_snippets)


async def get_figure_detail_uc(
    container: Annotated[Container, Depends(get_container)],
) -> GetFigureDetail:
    return GetFigureDetail(container.figures, container.categories, container.story_snippets)


async def get_story_detail_uc(
    container: Annotated[Container, Depends(get_container)],
) -> GetStoryDetail:
    return GetStoryDetail(container.story_snippets, container.figures, container.categories)


async def get_search_figures_uc(
    container: Annotated[Container, Depends(get_container)],
) -> SearchFigures:
    return SearchFigures(container.figures, container.categories, container.story_snippets)


async def get_about_us_page_uc(
    container: Annotated[Container, Depends(get_container)],
) -> GetAboutUsPage:
    return GetAboutUsPage(container.settings_repo)


async def get_contact_page_uc(
    container: Annotated[Container, Depends(get_container)],
) -> GetContactPage:
    return GetContactPage(container.contacts)


# ── Admin: categories ────────────────────────────────────────────────────
async def get_list_categories_admin_uc(
    container: Annotated[Container, Depends(get_container)],
) -> ListCategoriesAdmin:
    return ListCategoriesAdmin(container.categories)


async def get_get_category_uc(
    container: Annotated[Container, Depends(get_container)],
) -> GetCategory:
    return GetCategory(container.categories)


async def get_create_category_uc(
    container: Annotated[Container, Depends(get_container)],
) -> CreateCategory:
    return CreateCategory(container.categories)


async def get_update_category_uc(
    container: Annotated[Container, Depends(get_container)],
) -> UpdateCategory:
    return UpdateCategory(container.categories)


async def get_delete_category_uc(
    container: Annotated[Container, Depends(get_container)],
) -> DeleteCategory:
    return DeleteCategory(container.categories)


# ── Admin: contacts ──────────────────────────────────────────────────────
async def get_list_contacts_uc(
    container: Annotated[Container, Depends(get_container)],
) -> ListContacts:
    return ListContacts(container.contacts)


async def get_get_contact_uc(container: Annotated[Container, Depends(get_container)]) -> GetContact:
    return GetContact(container.contacts)


async def get_create_contact_uc(
    container: Annotated[Container, Depends(get_container)],
) -> CreateContact:
    return CreateContact(container.contacts)


async def get_update_contact_uc(
    container: Annotated[Container, Depends(get_container)],
) -> UpdateContact:
    return UpdateContact(container.contacts)


async def get_delete_contact_uc(
    container: Annotated[Container, Depends(get_container)],
) -> DeleteContact:
    return DeleteContact(container.contacts)


# ── Admin: users (superadmin-only) ──────────────────────────────────────
async def get_list_users_uc(container: Annotated[Container, Depends(get_container)]) -> ListUsers:
    return ListUsers(container.users)


async def get_get_user_uc(container: Annotated[Container, Depends(get_container)]) -> GetUser:
    return GetUser(container.users)


async def get_create_user_uc(
    container: Annotated[Container, Depends(get_container)],
) -> CreateUser:
    return CreateUser(container.users, container.hasher)


async def get_update_user_uc(
    container: Annotated[Container, Depends(get_container)],
) -> UpdateUser:
    return UpdateUser(container.users, container.hasher)


async def get_delete_user_uc(
    container: Annotated[Container, Depends(get_container)],
) -> DeleteUser:
    return DeleteUser(container.users)


# ── Admin: stories ───────────────────────────────────────────────────────
async def get_list_stories_uc(
    container: Annotated[Container, Depends(get_container)],
) -> ListStories:
    return ListStories(container.story_snippets, container.figures)


async def get_get_story_uc(container: Annotated[Container, Depends(get_container)]) -> GetStory:
    return GetStory(container.story_snippets, container.figures)


async def get_create_story_uc(
    container: Annotated[Container, Depends(get_container)],
) -> CreateStory:
    return CreateStory(container.story_snippets, container.figures, container.storage)


async def get_update_story_uc(
    container: Annotated[Container, Depends(get_container)],
) -> UpdateStory:
    return UpdateStory(container.story_snippets, container.figures, container.storage)


async def get_delete_story_uc(
    container: Annotated[Container, Depends(get_container)],
) -> DeleteStory:
    return DeleteStory(container.story_snippets, container.storage)


# ── Admin: figures ───────────────────────────────────────────────────────
async def get_list_figures_uc(
    container: Annotated[Container, Depends(get_container)],
) -> ListFigures:
    return ListFigures(container.figures, container.categories, container.story_snippets)


async def get_get_figure_uc(container: Annotated[Container, Depends(get_container)]) -> GetFigure:
    return GetFigure(container.figures, container.categories)


async def get_create_figure_uc(
    container: Annotated[Container, Depends(get_container)],
) -> CreateFigure:
    return CreateFigure(container.figures, container.storage)


async def get_update_figure_uc(
    container: Annotated[Container, Depends(get_container)],
) -> UpdateFigure:
    return UpdateFigure(container.figures, container.storage)


async def get_delete_figure_uc(
    container: Annotated[Container, Depends(get_container)],
) -> DeleteFigure:
    return DeleteFigure(container.figures, container.story_snippets, container.storage)


# ── Admin: featured figures ──────────────────────────────────────────────
async def get_list_featured_uc(
    container: Annotated[Container, Depends(get_container)],
) -> ListFeatured:
    return ListFeatured(container.featured, container.categories)


async def get_add_featured_uc(
    container: Annotated[Container, Depends(get_container)],
) -> AddFeatured:
    return AddFeatured(container.featured, container.figures)


async def get_remove_featured_uc(
    container: Annotated[Container, Depends(get_container)],
) -> RemoveFeatured:
    return RemoveFeatured(container.featured)


async def get_reorder_featured_uc(
    container: Annotated[Container, Depends(get_container)],
) -> ReorderFeatured:
    return ReorderFeatured(container.featured)


# ── Admin: settings (About Us) ───────────────────────────────────────────
async def get_get_about_us_admin_uc(
    container: Annotated[Container, Depends(get_container)],
) -> GetAboutUs:
    return GetAboutUs(container.settings_repo)


async def get_update_about_us_uc(
    container: Annotated[Container, Depends(get_container)],
) -> UpdateAboutUs:
    return UpdateAboutUs(container.settings_repo)


# ── Admin: audio ─────────────────────────────────────────────────────────
async def get_request_audio_generation_uc(
    container: Annotated[Container, Depends(get_container)],
) -> RequestAudioGeneration:
    return RequestAudioGeneration(container.figures, container.story_snippets, container.queue)


async def get_cancel_audio_generation_uc(
    container: Annotated[Container, Depends(get_container)],
) -> CancelAudioGeneration:
    return CancelAudioGeneration(container.figures, container.story_snippets)


async def get_get_audio_status_uc(
    container: Annotated[Container, Depends(get_container)],
    settings: Annotated[Settings, Depends(get_settings_dep)],
) -> GetAudioStatus:
    return GetAudioStatus(container.figures, container.story_snippets, settings.media.url_prefix)
