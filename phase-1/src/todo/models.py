"""Data models for the todo application."""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4


class Priority(Enum):
    """Task priority levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    """Represents a todo task."""

    title: str
    description: str = ""
    due_date: date | None = None
    priority: Priority = Priority.MEDIUM
    is_completed: bool = False
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
