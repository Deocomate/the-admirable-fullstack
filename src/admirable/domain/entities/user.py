from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from admirable.domain.exceptions import LastSuperAdminDeletionError, SelfDeletionError
from admirable.domain.value_objects.role import Role


@dataclass
class User:
    id: int | None
    name: str
    email: str
    password_hash: str
    role: Role
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def is_superadmin(self) -> bool:
        return self.role == Role.SUPERADMIN

    def is_admin(self) -> bool:
        return self.role in (Role.SUPERADMIN, Role.ADMIN)

    def can_be_deleted_by(self, actor: User, superadmin_count: int) -> None:
        """Raises if deletion is not allowed; matches `UserService::deleteAdmin`."""
        if self.is_superadmin() and superadmin_count <= 1:
            raise LastSuperAdminDeletionError()
        if actor.id == self.id:
            raise SelfDeletionError()
