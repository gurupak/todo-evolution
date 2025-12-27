"""Task SQLModel for persistent storage."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from todo_api.models.enums import PriorityEnum


class Task(SQLModel, table=True):
    """Task model for persistent storage."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Better Auth uses string IDs
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    is_completed: bool = Field(default=False)
    target_completion_date: Optional[datetime] = None  # User-set target date
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    class Config:
        """SQLModel configuration."""

        use_enum_values = True
