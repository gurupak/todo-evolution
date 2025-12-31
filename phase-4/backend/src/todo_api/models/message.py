"""Message model for conversation messages."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import JSON, Column, Text
from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    """Represents a single message within a conversation.

    Messages alternate between user and assistant roles, maintaining the full
    dialogue history. Each message stores its content, optional tool calls
    (for assistant messages), and metadata.
    """

    __tablename__ = "message"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique identifier for the message",
    )

    conversation_id: UUID = Field(
        foreign_key="conversation.id",
        nullable=False,
        index=True,
        description="ID of the conversation this message belongs to",
    )

    user_id: str = Field(
        nullable=False,
        index=True,
        description="ID of the user who owns this conversation (for isolation, references Better Auth user table)",
    )

    role: str = Field(
        nullable=False, max_length=20, description="Message sender role: 'user' or 'assistant'"
    )

    content: str = Field(
        sa_column=Column("content", Text, nullable=False), description="Message text content"
    )

    tool_calls: Optional[dict] = Field(
        default=None,
        sa_column=Column("tool_calls", JSON),
        description="AI tool invocations (assistant messages only)",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when the message was created",
    )

    class Config:
        """SQLModel configuration."""

        validate_assignment = True
