"""Tests for data models."""

from todo.models import Priority, Task


def test_task_minimal_creation():
    """Task can be created with just title."""
    task = Task(title="Test Task")
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.priority == Priority.MEDIUM
    assert task.is_completed is False
    assert task.id is not None
    assert task.created_at is not None
    assert task.updated_at is not None
    assert task.completed_at is None


def test_task_full_creation():
    """Task can be created with all optional fields."""
    task = Task(
        title="Test Task",
        description="Test Description",
        priority=Priority.HIGH,
        is_completed=True,
    )
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == Priority.HIGH
    assert task.is_completed is True


def test_task_unique_ids():
    """Each task gets unique UUID."""
    task1 = Task(title="Task 1")
    task2 = Task(title="Task 2")
    assert task1.id != task2.id


def test_priority_values():
    """Priority enum has expected values."""
    assert Priority.HIGH.value == "high"
    assert Priority.MEDIUM.value == "medium"
    assert Priority.LOW.value == "low"


def test_priority_comparison():
    """Priority enum values can be compared."""
    task = Task(title="Test", priority=Priority.HIGH)
    assert task.priority == Priority.HIGH
    assert task.priority != Priority.LOW
