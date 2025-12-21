"""SQLModel database models."""

from enum import Enum


class PriorityEnum(str, Enum):
    """Task priority levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
