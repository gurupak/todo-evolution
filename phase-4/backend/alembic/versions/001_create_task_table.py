"""Create task table

Revision ID: 001
Revises:
Create Date: 2025-12-20

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create priority enum if it doesn't exist
    op.execute("CREATE TYPE IF NOT EXISTS priority_enum AS ENUM ('high', 'medium', 'low')")

    # Create task table
    op.create_table(
        "task",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.String(1000), nullable=False, server_default=""),
        sa.Column(
            "priority",
            sa.Enum("high", "medium", "low", name="priority_enum"),
            nullable=False,
            server_default="medium",
        ),
        sa.Column("is_completed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column("completed_at", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes
    op.create_index("ix_task_user_id", "task", ["user_id"])
    op.create_index("ix_task_created_at", "task", [sa.text("created_at DESC")])
    op.create_index("ix_task_is_completed", "task", ["is_completed"])
    op.create_index("ix_task_user_completed", "task", ["user_id", "is_completed"])

    # Create updated_at trigger
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    op.execute("""
        CREATE TRIGGER update_task_updated_at
        BEFORE UPDATE ON task
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)

    # Create completed_at trigger
    op.execute("""
        CREATE OR REPLACE FUNCTION update_completed_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.is_completed = true AND OLD.is_completed = false THEN
                NEW.completed_at = now();
            ELSIF NEW.is_completed = false AND OLD.is_completed = true THEN
                NEW.completed_at = NULL;
            END IF;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    op.execute("""
        CREATE TRIGGER update_task_completed_at
        BEFORE UPDATE ON task
        FOR EACH ROW
        EXECUTE FUNCTION update_completed_at_column();
    """)


def downgrade() -> None:
    op.drop_table("task")
    op.execute("DROP TYPE priority_enum")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")
    op.execute("DROP FUNCTION IF EXISTS update_completed_at_column()")
    op.execute('DROP FUNCTION IF EXISTS update_completed_at_column()')
