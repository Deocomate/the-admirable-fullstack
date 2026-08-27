from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from admirable.infrastructure.db.base import Base


class ContactModel(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(255))
    label: Mapped[str] = mapped_column(String(255))
    value: Mapped[str] = mapped_column(String(255))
    icon: Mapped[str | None] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime | None]
    updated_at: Mapped[datetime | None]
