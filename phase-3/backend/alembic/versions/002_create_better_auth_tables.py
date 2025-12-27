"""Create Better Auth tables (user, session, account, verification)

Revision ID: 002
Revises: 001
Create Date: 2025-12-20

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user table
    op.create_table(
        "user",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("emailVerified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("image", sa.Text(), nullable=True),
        sa.Column("createdAt", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column("updatedAt", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    # Create session table
    op.create_table(
        "session",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("expiresAt", sa.TIMESTAMP(), nullable=False),
        sa.Column("token", sa.Text(), nullable=False),
        sa.Column("createdAt", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column("updatedAt", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column("ipAddress", sa.Text(), nullable=True),
        sa.Column("userAgent", sa.Text(), nullable=True),
        sa.Column("userId", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
        sa.ForeignKeyConstraint(["userId"], ["user.id"], ondelete="CASCADE"),
    )

    # Create account table
    op.create_table(
        "account",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("accountId", sa.Text(), nullable=False),
        sa.Column("providerId", sa.Text(), nullable=False),
        sa.Column("userId", sa.Text(), nullable=False),
        sa.Column("accessToken", sa.Text(), nullable=True),
        sa.Column("refreshToken", sa.Text(), nullable=True),
        sa.Column("idToken", sa.Text(), nullable=True),
        sa.Column("accessTokenExpiresAt", sa.TIMESTAMP(), nullable=True),
        sa.Column("refreshTokenExpiresAt", sa.TIMESTAMP(), nullable=True),
        sa.Column("scope", sa.Text(), nullable=True),
        sa.Column("password", sa.Text(), nullable=True),
        sa.Column("createdAt", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column("updatedAt", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["userId"], ["user.id"], ondelete="CASCADE"),
    )

    # Create verification table
    op.create_table(
        "verification",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("identifier", sa.Text(), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("expiresAt", sa.TIMESTAMP(), nullable=False),
        sa.Column("createdAt", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column("updatedAt", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes
    op.create_index("ix_session_userId", "session", ["userId"])
    op.create_index("ix_account_userId", "account", ["userId"])
    op.create_index("ix_verification_identifier", "verification", ["identifier"])

    # Create trigger for user table updated_at
    op.execute("""
        CREATE TRIGGER update_user_updated_at
        BEFORE UPDATE ON "user"
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)

    # Create trigger for session table updated_at
    op.execute("""
        CREATE TRIGGER update_session_updated_at
        BEFORE UPDATE ON session
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)

    # Create trigger for account table updated_at
    op.execute("""
        CREATE TRIGGER update_account_updated_at
        BEFORE UPDATE ON account
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)

    # Create trigger for verification table updated_at
    op.execute("""
        CREATE TRIGGER update_verification_updated_at
        BEFORE UPDATE ON verification
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    op.drop_table("verification")
    op.drop_table("account")
    op.drop_table("session")
    op.drop_table("user")
