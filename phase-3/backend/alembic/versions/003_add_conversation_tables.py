"""Add conversation and message tables

Revision ID: 003
Revises: 002
Create Date: 2025-12-26

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversation table
    op.create_table(
        "conversation",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("user_id", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("NOW()")),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
    )

    # Create index on user_id and updated_at for "recent conversations" query
    op.create_index(
        "idx_conversation_user_updated",
        "conversation",
        ["user_id", sa.text("updated_at DESC")],
    )

    # Create message table
    op.create_table(
        "message",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.Text(), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("tool_calls", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("NOW()")),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversation.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.CheckConstraint("role IN ('user', 'assistant')", name="message_role_check"),
        sa.CheckConstraint("length(content) > 0", name="message_content_not_empty"),
    )

    # Create index on conversation_id and created_at for chronological message loading
    op.create_index(
        "idx_message_conversation_created",
        "message",
        ["conversation_id", "created_at"],
    )


def downgrade() -> None:
    # Drop tables in reverse order (messages first due to foreign key)
    op.drop_index("idx_message_conversation_created", table_name="message")
    op.drop_table("message")

    op.drop_index("idx_conversation_user_updated", table_name="conversation")
    op.drop_table("conversation")
