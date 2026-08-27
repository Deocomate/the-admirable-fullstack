import pytest

from admirable.application.dto.auth_dto import (
    LoginCommand,
    RequestPasswordResetCommand,
    ResetPasswordCommand,
)
from admirable.application.use_cases.auth.login import InvalidCredentialsError, Login
from admirable.application.use_cases.auth.request_password_reset import RequestPasswordReset
from admirable.application.use_cases.auth.reset_password import (
    InvalidResetTokenError,
    ResetPassword,
)
from admirable.domain.entities.user import User
from admirable.domain.value_objects.role import Role
from tests.fakes.fake_mailer import FakeMailer
from tests.fakes.fake_password_hasher import FakePasswordHasher
from tests.fakes.fake_token_store import FakeTokenStore
from tests.fakes.fake_user_repository import FakeUserRepository


async def _seed_user(users: FakeUserRepository, hasher: FakePasswordHasher) -> User:
    return await users.add(
        User(
            id=None,
            name="Admin",
            email="admin@example.com",
            password_hash=hasher.hash("correct-password"),
            role=Role.ADMIN,
        )
    )


async def test_login_success() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    await _seed_user(users, hasher)

    result = await Login(users, hasher).execute(
        LoginCommand(email="admin@example.com", password="correct-password")
    )
    assert result.email == "admin@example.com"


async def test_login_wrong_password_raises() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    await _seed_user(users, hasher)

    with pytest.raises(InvalidCredentialsError):
        await Login(users, hasher).execute(
            LoginCommand(email="admin@example.com", password="wrong")
        )


async def test_login_unknown_email_raises() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()

    with pytest.raises(InvalidCredentialsError):
        await Login(users, hasher).execute(LoginCommand(email="nobody@example.com", password="x"))


async def test_login_rehashes_when_needed() -> None:
    users = FakeUserRepository()
    user = await users.add(
        User(id=None, name="A", email="a@example.com", password_hash="legacy-hash", role=Role.ADMIN)
    )
    hasher = FakePasswordHasher(rehash_needed_for={"legacy-hash"})

    class LegacyHasher(FakePasswordHasher):
        def verify(self, password: str, password_hash: str) -> bool:
            return password_hash == "legacy-hash" and password == "correct-password"

    legacy_hasher = LegacyHasher(rehash_needed_for={"legacy-hash"})
    await Login(users, legacy_hasher).execute(
        LoginCommand(email="a@example.com", password="correct-password")
    )
    stored = await users.get_by_id(user.id)  # type: ignore[arg-type]
    assert stored is not None
    assert stored.password_hash == "hashed:correct-password"
    _ = hasher


async def test_request_password_reset_sends_mail_for_existing_user() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    await _seed_user(users, hasher)
    tokens = FakeTokenStore()
    mailer = FakeMailer()

    await RequestPasswordReset(users, tokens, mailer).execute(
        RequestPasswordResetCommand(email="admin@example.com")
    )
    assert len(mailer.sent) == 1


async def test_request_password_reset_silent_for_unknown_email() -> None:
    users = FakeUserRepository()
    tokens = FakeTokenStore()
    mailer = FakeMailer()

    await RequestPasswordReset(users, tokens, mailer).execute(
        RequestPasswordResetCommand(email="nobody@example.com")
    )
    assert mailer.sent == []


async def test_reset_password_success() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    await _seed_user(users, hasher)
    tokens = FakeTokenStore()
    token = await tokens.issue("admin@example.com")

    await ResetPassword(users, tokens, hasher).execute(
        ResetPasswordCommand(token=token, email="admin@example.com", password="brand-new")
    )
    stored = await users.get_by_email("admin@example.com")
    assert stored is not None
    assert stored.password_hash == "hashed:brand-new"


async def test_reset_password_invalid_token_raises() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    tokens = FakeTokenStore()

    with pytest.raises(InvalidResetTokenError):
        await ResetPassword(users, tokens, hasher).execute(
            ResetPasswordCommand(token="bogus", email="admin@example.com", password="x")
        )


async def test_reset_password_token_is_single_use() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    await _seed_user(users, hasher)
    tokens = FakeTokenStore()
    token = await tokens.issue("admin@example.com")

    await ResetPassword(users, tokens, hasher).execute(
        ResetPasswordCommand(token=token, email="admin@example.com", password="first")
    )
    with pytest.raises(InvalidResetTokenError):
        await ResetPassword(users, tokens, hasher).execute(
            ResetPasswordCommand(token=token, email="admin@example.com", password="second")
        )
