from sqlalchemy import BigInteger, Column, ForeignKey, Table

from admirable.infrastructure.db.base import Base

category_figure_table = Table(
    "category_figure",
    Base.metadata,
    Column(
        "category_id",
        BigInteger,
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("figure_id", BigInteger, ForeignKey("figures.id", ondelete="CASCADE"), primary_key=True),
)
