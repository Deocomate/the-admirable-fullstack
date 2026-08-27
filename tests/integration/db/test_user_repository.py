from sqlalchemy.ext.asyncio import AsyncSession

from admirable.domain.entities.user import User
from admirable.domain.value_objects.role import Role
from admirable.infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl


def make_user(email: str, role: Role = Role.ADMIN) -> User:
    return User(id=None, name="Test Admin", email=email, password_hash="hashed", role=role)


async def test_add_and_get_by_email(db_session: AsyncSession) -> None:
    repo = UserRepositoryImpl(db_session)
    user = await repo.add(make_user("admin-it@example.com"))
    assert user.id is not None

    fetched = await repo.get_by_email("admin-it@example.com")
    assert fetched is not None
    assert fetched.id == user.id


async def test_count_all_admins(db_session: AsyncSession) -> None:
    repo = UserRepositoryImpl(db_session)
    before = await repo.count_all_admins()
    await repo.add(make_user("super1-it@example.com", role=Role.SUPERADMIN))
    await repo.add(make_user("super2-it@example.com", role=Role.SUPERADMIN))
    await repo.add(make_user("admin1-it@example.com", role=Role.ADMIN))

    assert await repo.count_all_admins() == before + 3


async def test_update_and_delete(db_session: AsyncSession) -> None:
    repo = UserRepositoryImpl(db_session)
    user = await repo.add(make_user("update-it@example.com"))
    user.name = "Renamed"
    updated = await repo.update(user)
    assert updated.name == "Renamed"

    await repo.delete(user.id)  # type: ignore[arg-type]
    assert await repo.get_by_id(user.id) is None  # type: ignore[arg-type]
