"""Pytest fixtures for todo application tests."""

import pytest

from todo.models import Priority, Task
from todo.storage import InMemoryStorage


@pytest.fixture
def empty_storage() -> InMemoryStorage:
    """Create an empty storage instance."""
    return InMemoryStorage()


@pytest.fixture
def storage_with_tasks() -> InMemoryStorage:
    """Create storage with sample tasks."""
    storage = InMemoryStorage()
    storage.add(Task(title="Task 1", priority=Priority.HIGH))
    storage.add(Task(title="Task 2", priority=Priority.MEDIUM))
    task3 = Task(title="Task 3", priority=Priority.LOW, is_completed=True)
    storage.add(task3)
    return storage


@pytest.fixture
def sample_task() -> Task:
    """Create a sample task."""
    return Task(title="Sample Task", description="Test description", priority=Priority.MEDIUM)
