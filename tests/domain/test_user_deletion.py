import pytest

from admirable.domain.entities.user import User
from admirable.domain.exceptions import CannotDeleteSuperAdminError, SelfDeletionError
from admirable.domain.value_objects.role import Role


def make_user(**overrides: object) -> User:
    defaults: dict[str, object] = dict(
        id=1, name="Admin", email="admin@example.com", password_hash="hash", role=Role.ADMIN
    )
    defaults.update(overrides)
    return User(**defaults)  # type: ignore[arg-type]


def test_cannot_delete_superadmin() -> None:
    """Matches `UserService::deleteAdmin`: a superadmin can never be deleted,
    not just "the last one" — this holds even with multiple superadmins."""
    target = make_user(id=1, role=Role.SUPERADMIN)
    actor = make_user(id=2, role=Role.SUPERADMIN)
    with pytest.raises(CannotDeleteSuperAdminError):
        target.can_be_deleted_by(actor)


def test_cannot_delete_self() -> None:
    target = make_user(id=2, role=Role.ADMIN)
    actor = make_user(id=2, role=Role.ADMIN)
    with pytest.raises(SelfDeletionError):
        target.can_be_deleted_by(actor)


def test_can_delete_other_admin() -> None:
    target = make_user(id=2, role=Role.ADMIN)
    actor = make_user(id=1, role=Role.SUPERADMIN)
    target.can_be_deleted_by(actor)
