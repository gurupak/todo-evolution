"""Task request/response schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..models import PriorityEnum


class TaskCreateRequest(BaseModel):
    """Request schema for creating a task."""

    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    target_completion_date: Optional[datetime] = None


class TaskUpdateRequest(BaseModel):
    """Request schema for updating a task."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[PriorityEnum] = None
    target_completion_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    """Response schema for a single task."""

    id: UUID
    user_id: str  # Better Auth uses string IDs, not UUID
    title: str
    description: str
    priority: PriorityEnum
    is_completed: bool
    target_completion_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class TaskListResponse(BaseModel):
    """Response schema for task list with stats."""

    tasks: list[TaskResponse]
    total: int
    completed: int
    pending: int
