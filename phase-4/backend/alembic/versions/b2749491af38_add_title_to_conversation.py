"""add_title_to_conversation

Revision ID: b2749491af38
Revises: 003
Create Date: 2025-12-27 20:13:08.730248

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "b2749491af38"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add title column to conversation table
    op.add_column("conversation", sa.Column("title", sa.String(length=200), nullable=True))


def downgrade() -> None:
    # Remove title column from conversation table
    op.drop_column("conversation", "title")
