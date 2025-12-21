"""Task business logic service."""

from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.task import Task
from ..schemas.task import TaskCreateRequest, TaskListResponse, TaskUpdateRequest


class TaskService:
    """Service for task CRUD operations."""

    def __init__(self, session: AsyncSession):
        """Initialize service with database session."""
        self.session = session

    async def create(self, user_id: str, data: TaskCreateRequest) -> Task:
        """Create a new task for the user."""
        # Strip timezone info for PostgreSQL TIMESTAMP WITHOUT TIME ZONE
        target_date = None
        if data.target_completion_date:
            target_date = data.target_completion_date.replace(tzinfo=None)

        task = Task(
            user_id=user_id,
            title=data.title.strip(),
            description=data.description.strip(),
            priority=data.priority,
            target_completion_date=target_date,
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_all(self, user_id: str) -> TaskListResponse:
        """Get all tasks for a user with stats."""
        # Get all tasks
        result = await self.session.execute(
            select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
        )
        tasks = result.scalars().all()

        # Calculate stats
        total = len(tasks)
        completed = sum(1 for task in tasks if task.is_completed)
        pending = total - completed

        return TaskListResponse(
            tasks=tasks,
            total=total,
            completed=completed,
            pending=pending,
        )

    async def get_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        """Get a specific task by ID, ensuring it belongs to the user."""
        result = await self.session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def update(self, task_id: str, user_id: str, data: TaskUpdateRequest) -> Optional[Task]:
        """Update a task with partial data."""
        task = await self.get_by_id(task_id, user_id)
        if not task:
            return None

        # Update only provided fields
        if data.title is not None:
            task.title = data.title.strip()
        if data.description is not None:
            task.description = data.description.strip()
        if data.priority is not None:
            task.priority = data.priority
        if data.target_completion_date is not None:
            # Strip timezone info for PostgreSQL TIMESTAMP WITHOUT TIME ZONE
            task.target_completion_date = data.target_completion_date.replace(tzinfo=None)

        task.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def toggle_complete(self, task_id: str, user_id: str) -> Optional[Task]:
        """Toggle task completion status."""
        task = await self.get_by_id(task_id, user_id)
        if not task:
            return None

        task.is_completed = not task.is_completed
        task.completed_at = datetime.utcnow() if task.is_completed else None
        task.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: str, user_id: str) -> bool:
        """Delete a task."""
        task = await self.get_by_id(task_id, user_id)
        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True
