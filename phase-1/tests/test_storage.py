"""Tests for storage operations."""

from uuid import uuid4

from todo.models import Priority, Task


def test_add_and_get_task(empty_storage):
    """Can add and retrieve a task."""
    task = Task(title="Test Task")
    empty_storage.add(task)
    assert empty_storage.get(task.id) == task


def test_get_nonexistent_task(empty_storage):
    """Getting nonexistent task returns None."""
    assert empty_storage.get(uuid4()) is None


def test_get_all_tasks(storage_with_tasks):
    """Can retrieve all tasks."""
    all_tasks = storage_with_tasks.get_all()
    assert len(all_tasks) == 3


def test_update_task(empty_storage):
    """Can update task fields."""
    task = Task(title="Original")
    empty_storage.add(task)

    updated = empty_storage.update(task.id, title="Updated")
    assert updated is not None
    assert updated.title == "Updated"
    assert updated.updated_at > task.created_at


def test_update_nonexistent_task(empty_storage):
    """Updating nonexistent task returns None."""
    assert empty_storage.update(uuid4(), title="New") is None


def test_delete_task(empty_storage):
    """Can delete a task."""
    task = Task(title="To Delete")
    empty_storage.add(task)

    assert empty_storage.delete(task.id) is True
    assert empty_storage.get(task.id) is None


def test_delete_nonexistent_task(empty_storage):
    """Deleting nonexistent task returns False."""
    assert empty_storage.delete(uuid4()) is False


def test_get_pending(storage_with_tasks):
    """Can filter pending tasks."""
    pending = storage_with_tasks.get_pending()
    assert len(pending) == 2
    assert all(not task.is_completed for task in pending)


def test_get_completed(storage_with_tasks):
    """Can filter completed tasks."""
    completed = storage_with_tasks.get_completed()
    assert len(completed) == 1
    assert all(task.is_completed for task in completed)


def test_count(storage_with_tasks):
    """Can get task counts."""
    counts = storage_with_tasks.count()
    assert counts["total"] == 3
    assert counts["completed"] == 1
    assert counts["pending"] == 2


def test_mark_complete_sets_timestamp(empty_storage):
    """Marking task complete sets completed_at."""
    task = Task(title="Test")
    empty_storage.add(task)

    updated = empty_storage.update(task.id, is_completed=True)
    assert updated is not None
    assert updated.is_completed is True
    assert updated.completed_at is not None


def test_mark_incomplete_clears_timestamp(empty_storage):
    """Marking task incomplete clears completed_at."""
    task = Task(title="Test", is_completed=True)
    empty_storage.add(task)

    updated = empty_storage.update(task.id, is_completed=False)
    assert updated is not None
    assert updated.is_completed is False
    assert updated.completed_at is None
