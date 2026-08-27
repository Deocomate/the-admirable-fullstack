import pytest

from admirable.application.use_cases.users.delete_user import DeleteUser
from admirable.domain.entities.user import User
from admirable.domain.exceptions import CannotDeleteSuperAdminError, SelfDeletionError
from admirable.domain.value_objects.role import Role
from tests.fakes.fake_user_repository import FakeUserRepository


async def test_cannot_delete_superadmin() -> None:
    users = FakeUserRepository()
    target = await users.add(
        User(
            id=None,
            name="Root",
            email="root@example.com",
            password_hash="h",
            role=Role.SUPERADMIN,
        )
    )
    other_admin = await users.add(
        User(id=None, name="Admin", email="admin@example.com", password_hash="h", role=Role.ADMIN)
    )

    with pytest.raises(CannotDeleteSuperAdminError):
        await DeleteUser(users).execute(target.id, actor=other_admin)  # type: ignore[arg-type]


async def test_cannot_delete_self() -> None:
    users = FakeUserRepository()
    admin_a = await users.add(
        User(id=None, name="A", email="a@example.com", password_hash="h", role=Role.ADMIN)
    )

    with pytest.raises(SelfDeletionError):
        await DeleteUser(users).execute(admin_a.id, actor=admin_a)  # type: ignore[arg-type]


async def test_can_delete_regular_admin() -> None:
    users = FakeUserRepository()
    superadmin = await users.add(
        User(
            id=None,
            name="Root",
            email="root@example.com",
            password_hash="h",
            role=Role.SUPERADMIN,
        )
    )
    target = await users.add(
        User(id=None, name="Admin", email="admin@example.com", password_hash="h", role=Role.ADMIN)
    )

    await DeleteUser(users).execute(target.id, actor=superadmin)  # type: ignore[arg-type]

    assert await users.get_by_id(target.id) is None  # type: ignore[arg-type]
