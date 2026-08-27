from datetime import datetime

from sqlalchemy import BigInteger, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from admirable.domain.value_objects.audio_status import AudioStatus
from admirable.infrastructure.db.base import Base
from admirable.infrastructure.db.models.figure import FigureModel
from admirable.infrastructure.db.types import ContentBlocksType


class StorySnippetModel(Base):
    __tablename__ = "story_snippets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    figure_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("figures.id", ondelete="CASCADE")
    )
    title: Mapped[str] = mapped_column(String(255))
    subtitle: Mapped[str | None] = mapped_column(String(255))
    content_blocks: Mapped[list | None] = mapped_column(ContentBlocksType)  # type: ignore[type-arg]
    search_text: Mapped[str | None] = mapped_column(Text)
    image_path: Mapped[str | None] = mapped_column(String(255))
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

    figure: Mapped[FigureModel] = relationship(back_populates="story_snippets", lazy="raise")
