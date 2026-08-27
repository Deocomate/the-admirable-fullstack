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
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from admirable.application.dto.auth_dto import AuthenticatedUserDTO
from admirable.application.use_cases.auth.login import Login
from admirable.application.use_cases.auth.request_password_reset import RequestPasswordReset
from admirable.application.use_cases.auth.reset_password import ResetPassword
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
                id=user.id, name=user.name, email=user.email, role=user.role  # type: ignore[arg-type]
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


def require_role(*roles: Role) -> object:
    async def _dependency(
        user: Annotated[AuthenticatedUserDTO, Depends(require_auth)],
    ) -> AuthenticatedUserDTO:
        if user.role not in roles:
            raise ForbiddenError()
        return user

    return Depends(_dependency)


async def get_login_use_case(container: Annotated[Container, Depends(get_container)]) -> Login:
    return Login(container.users, container.hasher)


async def get_request_password_reset_use_case(
    container: Annotated[Container, Depends(get_container)],
) -> RequestPasswordReset:
    return RequestPasswordReset(container.users, container.tokens, container.mailer)


async def get_reset_password_use_case(
    container: Annotated[Container, Depends(get_container)],
) -> ResetPassword:
    return ResetPassword(container.users, container.tokens, container.hasher)
