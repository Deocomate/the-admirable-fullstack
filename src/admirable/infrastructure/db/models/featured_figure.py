from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from admirable.infrastructure.db.base import Base
from admirable.infrastructure.db.models.figure import FigureModel


class FeaturedFigureModel(Base):
    __tablename__ = "featured_figures"
    __table_args__ = (UniqueConstraint("figure_id", name="uq_featured_figures_figure_id"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    figure_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("figures.id", ondelete="CASCADE")
    )
    priority: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime | None]
    updated_at: Mapped[datetime | None]

    figure: Mapped[FigureModel] = relationship(back_populates="featured_figure", lazy="raise")
