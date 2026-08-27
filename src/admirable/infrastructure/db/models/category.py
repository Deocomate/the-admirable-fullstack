from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from admirable.infrastructure.db.base import Base
from admirable.infrastructure.db.models.associations import category_figure_table

if TYPE_CHECKING:
    from admirable.infrastructure.db.models.figure import FigureModel


class CategoryModel(Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("slug", name="uq_categories_slug"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime | None]
    updated_at: Mapped[datetime | None]

    figures: Mapped[list[FigureModel]] = relationship(
        secondary=category_figure_table, back_populates="categories", lazy="raise"
    )
