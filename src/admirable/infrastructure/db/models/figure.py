from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Enum, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from admirable.domain.value_objects.audio_status import AudioStatus
from admirable.infrastructure.db.base import Base
from admirable.infrastructure.db.models.associations import category_figure_table
from admirable.infrastructure.db.models.category import CategoryModel
from admirable.infrastructure.db.types import ContentBlocksType, KeyFactsType

if TYPE_CHECKING:
    from admirable.infrastructure.db.models.featured_figure import FeaturedFigureModel
    from admirable.infrastructure.db.models.story_snippet import StorySnippetModel


class FigureModel(Base):
    __tablename__ = "figures"
    __table_args__ = (UniqueConstraint("slug", name="uq_figures_slug"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    avatar_path: Mapped[str | None] = mapped_column(String(255))
    short_description: Mapped[str | None] = mapped_column(Text)
    key_facts: Mapped[list | None] = mapped_column(KeyFactsType)  # type: ignore[type-arg]
    content_blocks: Mapped[list | None] = mapped_column(ContentBlocksType)  # type: ignore[type-arg]
    search_text: Mapped[str | None] = mapped_column(Text)
    audio_path: Mapped[str | None] = mapped_column(String(255))
    audio_status: Mapped[AudioStatus] = mapped_column(
        Enum(
            AudioStatus,
            name="audio_status_enum",
            native_enum=True,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=AudioStatus.IDLE,
    )
    audio_error: Mapped[str | None] = mapped_column(String(500))
    youtube_url: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime | None]
    updated_at: Mapped[datetime | None]

    categories: Mapped[list[CategoryModel]] = relationship(
        secondary=category_figure_table, back_populates="figures", lazy="raise"
    )
    story_snippets: Mapped[list[StorySnippetModel]] = relationship(
        back_populates="figure", lazy="raise", cascade="all, delete-orphan"
    )
    featured_figure: Mapped[FeaturedFigureModel | None] = relationship(
        back_populates="figure", lazy="raise", cascade="all, delete-orphan"
    )
