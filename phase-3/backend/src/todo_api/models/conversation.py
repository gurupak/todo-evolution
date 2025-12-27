"""Conversation model for chat conversations."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Conversation(SQLModel, table=True):
    """Represents a chat conversation between a user and the AI assistant.

    Each conversation contains an ordered sequence of messages and belongs to
    a single user. Conversations enable context retention and resumption across
    sessions.
    """

    __tablename__ = "conversation"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique identifier for the conversation",
    )

    user_id: str = Field(
        nullable=False,
        index=True,
        description="ID of the user who owns this conversation (references Better Auth user table)",
    )

    title: str | None = Field(
        default=None,
        max_length=200,
        description="Optional custom title for the conversation",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when the conversation was created",
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp of the last message in the conversation",
    )

    class Config:
        """SQLModel configuration."""

        validate_assignment = True
