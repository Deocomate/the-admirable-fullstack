"""Single dependency-construction point shared by the web app and the worker.

Both call `build_request_scope`/`build_worker_scope` to get the same
`Container` of repositories and ports, so the two processes can never drift
into different wiring. Use cases are built on demand from a `Container`
(they're cheap dataclasses over these), not pre-instantiated here — there
are ~47 of them and most requests need only one or two.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncSession

from admirable.application.ports.clock_port import ClockPort
from admirable.application.ports.file_storage_port import FileStoragePort
from admirable.application.ports.mailer_port import MailerPort
from admirable.application.ports.password_hasher_port import PasswordHasherPort
from admirable.application.ports.task_queue_port import TaskQueuePort
from admirable.application.ports.text_to_speech_port import TextToSpeechPort
from admirable.application.ports.token_store_port import TokenStorePort
from admirable.config import Settings
from admirable.domain.repositories.category_repository import CategoryRepository
from admirable.domain.repositories.contact_repository import ContactRepository
from admirable.domain.repositories.featured_figure_repository import FeaturedFigureRepository
from admirable.domain.repositories.figure_repository import FigureRepository
from admirable.domain.repositories.setting_repository import SettingRepository
from admirable.domain.repositories.story_snippet_repository import StorySnippetRepository
from admirable.domain.repositories.user_repository import UserRepository
from admirable.infrastructure.clock import SystemClock
from admirable.infrastructure.db.repositories.category_repository_impl import (
    CategoryRepositoryImpl,
)
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
from admirable.infrastructure.db.session import create_engine, create_session_factory, session_scope
from admirable.infrastructure.mail.log_mailer import LogMailer
from admirable.infrastructure.mail.smtp_mailer import SmtpMailer
from admirable.infrastructure.queue.taskiq_queue import TaskiqQueue
from admirable.infrastructure.security.password_hasher import BcryptPasswordHasher
from admirable.infrastructure.security.redis_token_store import RedisTokenStore
from admirable.infrastructure.storage.local_storage import LocalFileStorage
from admirable.infrastructure.tts.edge_tts_adapter import EdgeTtsAdapter


@dataclass
class Container:
    # Repositories
    figures: FigureRepository
    story_snippets: StorySnippetRepository
    categories: CategoryRepository
    contacts: ContactRepository
    featured: FeaturedFigureRepository
    users: UserRepository
    settings_repo: SettingRepository

    # Ports
    storage: FileStoragePort
    tts: TextToSpeechPort
    queue: TaskQueuePort
    hasher: PasswordHasherPort
    mailer: MailerPort
    tokens: TokenStorePort
    clock: ClockPort

    media_url_prefix: str


def _build_mailer(settings: Settings) -> MailerPort:
    if settings.mail.driver == "smtp":
        return SmtpMailer(
            host=settings.mail.smtp_host,
            port=settings.mail.smtp_port,
            username=settings.mail.smtp_user,
            password=settings.mail.smtp_password,
            from_address=settings.mail.from_address,
            from_name=settings.mail.from_name,
            base_url=settings.app.base_url,
        )
    return LogMailer()


def build_request_scope(session: AsyncSession, settings: Settings, redis: Redis) -> Container:
    return Container(
        figures=FigureRepositoryImpl(session),
        story_snippets=StorySnippetRepositoryImpl(session),
        categories=CategoryRepositoryImpl(session),
        contacts=ContactRepositoryImpl(session),
        featured=FeaturedFigureRepositoryImpl(session),
        users=UserRepositoryImpl(session),
        settings_repo=SettingRepositoryImpl(session),
        storage=LocalFileStorage(settings.media.root),
        tts=EdgeTtsAdapter(
            voice=settings.tts.voice,
            rate=settings.tts.rate,
            volume=settings.tts.volume,
            pitch=settings.tts.pitch,
            max_chars_per_chunk=settings.tts.max_chars_per_chunk,
        ),
        queue=TaskiqQueue(),
        hasher=BcryptPasswordHasher(),
        mailer=_build_mailer(settings),
        tokens=RedisTokenStore(redis),
        clock=SystemClock(),
        media_url_prefix=settings.media.url_prefix,
    )


@asynccontextmanager
async def build_worker_scope(settings: Settings) -> AsyncIterator[Container]:
    """Opens its own engine/session/redis per task — the worker is a separate
    process from the web app and doesn't share its connection pools."""
    engine = create_engine(settings.db)
    session_factory = create_session_factory(engine)
    redis = from_url(settings.redis.url)
    try:
        async with session_scope(session_factory) as session:
            yield build_request_scope(session, settings, redis)
    finally:
        await redis.aclose()
        await engine.dispose()
