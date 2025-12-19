"""In-memory task storage."""

from datetime import datetime
from uuid import UUID

from todo.models import Task


class InMemoryStorage:
    """In-memory task storage using dictionary."""

    def __init__(self) -> None:
        """Initialize empty task storage."""
        self._tasks: dict[UUID, Task] = {}

    def add(self, task: Task) -> Task:
        """Add a new task to storage."""
        self._tasks[task.id] = task
        return task

    def get(self, task_id: UUID) -> Task | None:
        """Get a task by ID, or None if not found."""
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """Get all tasks."""
        return list(self._tasks.values())

    def update(self, task_id: UUID, **kwargs) -> Task | None:
        """Update a task's fields. Returns updated task or None if not found."""
        task = self._tasks.get(task_id)
        if task is None:
            return None

        # Update specified fields
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

        # Always update updated_at timestamp
        task.updated_at = datetime.now()

        # Handle completion status changes
        if "is_completed" in kwargs:
            if kwargs["is_completed"]:
                task.completed_at = datetime.now()
            else:
                task.completed_at = None

        return task

    def delete(self, task_id: UUID) -> bool:
        """Delete a task. Returns True if deleted, False if not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def get_pending(self) -> list[Task]:
        """Get all incomplete tasks."""
        return [task for task in self._tasks.values() if not task.is_completed]

    def get_completed(self) -> list[Task]:
        """Get all completed tasks."""
        return [task for task in self._tasks.values() if task.is_completed]

    def count(self) -> dict[str, int]:
        """Get task counts (total, completed, pending)."""
        completed = sum(1 for task in self._tasks.values() if task.is_completed)
        total = len(self._tasks)
        return {"total": total, "completed": completed, "pending": total - completed}
