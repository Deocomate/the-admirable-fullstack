from datetime import datetime

from sqlalchemy import BigInteger, Enum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from admirable.domain.value_objects.role import Role
from admirable.infrastructure.db.base import Base


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(
        Enum(
            Role, name="role_enum", native_enum=True, values_callable=lambda e: [m.value for m in e]
        )
    )
    created_at: Mapped[datetime | None]
    updated_at: Mapped[datetime | None]
