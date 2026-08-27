"""baseline schema

Revision ID: 0001
Revises:
Create Date: 2026-08-27

Defines the cleaned target schema (8 business tables). Drops the 7 Laravel
infrastructure tables (cache, cache_locks, jobs, job_batches, failed_jobs,
sessions, password_reset_tokens) by simply never creating them — sessions and
password-reset tokens move to Redis.
"""

# SQLAlchemy's stubs type dialect-specific create_table kwargs (mysql_charset,
# mysql_collate, mysql_engine) as `bool | None`, which is a known stub gap,
# not a real type mismatch — https://github.com/sqlalchemy/sqlalchemy/issues
# mypy: disable-error-code="arg-type"

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_MYSQL_OPTS = {
    "mysql_charset": "utf8mb4",
    "mysql_collate": "utf8mb4_unicode_ci",
    "mysql_engine": "InnoDB",
}
_AUDIO_STATUS_VALUES = ("idle", "processing", "completed", "failed", "cancelled")


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.UniqueConstraint("slug", name="uq_categories_slug"),
        **_MYSQL_OPTS,
    )

    op.create_table(
        "figures",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("avatar_path", sa.String(255), nullable=True),
        sa.Column("short_description", sa.Text, nullable=True),
        sa.Column("key_facts", sa.JSON, nullable=True),
        sa.Column("content_blocks", sa.JSON, nullable=True),
        sa.Column("search_text", sa.Text, nullable=True),
        sa.Column("audio_path", sa.String(255), nullable=True),
        sa.Column(
            "audio_status",
            sa.Enum(*_AUDIO_STATUS_VALUES, name="audio_status_enum"),
            nullable=False,
            server_default="idle",
        ),
        sa.Column("audio_error", sa.String(500), nullable=True),
        sa.Column("youtube_url", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.UniqueConstraint("slug", name="uq_figures_slug"),
        **_MYSQL_OPTS,
    )

    op.create_table(
        "category_figure",
        sa.Column(
            "category_id",
            sa.BigInteger,
            sa.ForeignKey("categories.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "figure_id",
            sa.BigInteger,
            sa.ForeignKey("figures.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        **_MYSQL_OPTS,
    )

    op.create_table(
        "story_snippets",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "figure_id",
            sa.BigInteger,
            sa.ForeignKey("figures.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("subtitle", sa.String(255), nullable=True),
        sa.Column("content_blocks", sa.JSON, nullable=True),
        sa.Column("search_text", sa.Text, nullable=True),
        sa.Column("image_path", sa.String(255), nullable=True),
        sa.Column("audio_path", sa.String(255), nullable=True),
        sa.Column(
            "audio_status",
            sa.Enum(*_AUDIO_STATUS_VALUES, name="audio_status_enum"),
            nullable=False,
            server_default="idle",
        ),
        sa.Column("audio_error", sa.String(500), nullable=True),
        sa.Column("youtube_url", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        **_MYSQL_OPTS,
    )

    op.create_table(
        "featured_figures",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "figure_id",
            sa.BigInteger,
            sa.ForeignKey("figures.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("priority", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.UniqueConstraint("figure_id", name="uq_featured_figures_figure_id"),
        **_MYSQL_OPTS,
    )

    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("superadmin", "admin", name="role_enum"), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.UniqueConstraint("email", name="uq_users_email"),
        **_MYSQL_OPTS,
    )

    op.create_table(
        "settings",
        sa.Column("key", sa.String(255), primary_key=True),
        sa.Column("value", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        **_MYSQL_OPTS,
    )

    op.create_table(
        "contacts",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("type", sa.String(255), nullable=False),
        sa.Column("label", sa.String(255), nullable=False),
        sa.Column("value", sa.String(255), nullable=False),
        sa.Column("icon", sa.String(255), nullable=True),
        sa.Column("sort_order", sa.Integer, nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        **_MYSQL_OPTS,
    )

    op.execute(
        "ALTER TABLE figures ADD FULLTEXT KEY ft_figures_search "
        "(name, short_description, search_text) WITH PARSER ngram"
    )
    op.execute(
        "ALTER TABLE story_snippets ADD FULLTEXT KEY ft_story_snippets_search "
        "(title, subtitle, search_text) WITH PARSER ngram"
    )


def downgrade() -> None:
    op.drop_table("contacts")
    op.drop_table("settings")
    op.drop_table("users")
    op.drop_table("featured_figures")
    op.drop_table("story_snippets")
    op.drop_table("category_figure")
    op.drop_table("figures")
    op.drop_table("categories")
