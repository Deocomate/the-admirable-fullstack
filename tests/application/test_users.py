from admirable.application.dto.user_dto import CreateUserCommand, UpdateUserCommand
from admirable.application.use_cases.users.create_user import CreateUser
from admirable.application.use_cases.users.list_users import ListUsers
from admirable.application.use_cases.users.update_user import UpdateUser
from admirable.domain.value_objects.role import Role
from tests.fakes.fake_password_hasher import FakePasswordHasher
from tests.fakes.fake_user_repository import FakeUserRepository


async def test_create_user_is_always_admin_role() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    created = await CreateUser(users, hasher).execute(
        CreateUserCommand(name="New Admin", email="new@example.com", password="secret123")
    )
    assert created.role == Role.ADMIN
    stored = await users.get_by_id(created.id)
    assert stored is not None
    assert stored.password_hash == "hashed:secret123"


async def test_update_user_without_password_keeps_hash() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    created = await CreateUser(users, hasher).execute(
        CreateUserCommand(name="Admin", email="a@example.com", password="original")
    )
    await UpdateUser(users, hasher).execute(
        UpdateUserCommand(user_id=created.id, name="Renamed", email="a@example.com")
    )
    stored = await users.get_by_id(created.id)
    assert stored is not None
    assert stored.name == "Renamed"
    assert stored.password_hash == "hashed:original"


async def test_update_user_with_password_rehashes() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    created = await CreateUser(users, hasher).execute(
        CreateUserCommand(name="Admin", email="a@example.com", password="original")
    )
    await UpdateUser(users, hasher).execute(
        UpdateUserCommand(
            user_id=created.id, name="Admin", email="a@example.com", password="newpass"
        )
    )
    stored = await users.get_by_id(created.id)
    assert stored is not None
    assert stored.password_hash == "hashed:newpass"


async def test_list_users() -> None:
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    await CreateUser(users, hasher).execute(
        CreateUserCommand(name="A", email="a@example.com", password="pw")
    )
    await CreateUser(users, hasher).execute(
        CreateUserCommand(name="B", email="b@example.com", password="pw")
    )
    result = await ListUsers(users).execute()
    assert len(result) == 2
