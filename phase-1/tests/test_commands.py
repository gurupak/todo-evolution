"""Tests for command handlers."""

from unittest.mock import MagicMock, patch

from todo.commands import add_task, delete_task, list_tasks, mark_complete, mark_incomplete
from todo.models import Priority, Task


@patch("todo.commands._prompt_due_date")
@patch("todo.commands.questionary")
def test_add_task_creates_task(mock_questionary, mock_prompt_due_date, empty_storage):
    """Add task creates and stores a task."""
    # Mock user input: title, description
    mock_questionary.text.return_value.ask.side_effect = ["Buy milk", "Whole milk"]
    # Mock due date selection (no due date selected)
    mock_prompt_due_date.return_value = None
    # Mock priority selection
    mock_questionary.select.return_value.ask.return_value = Priority.MEDIUM

    add_task(empty_storage)

    tasks = empty_storage.get_all()
    assert len(tasks) == 1
    assert tasks[0].title == "Buy milk"
    assert tasks[0].description == "Whole milk"
    assert tasks[0].due_date is None
    assert tasks[0].priority == Priority.MEDIUM


@patch("todo.commands.questionary")
def test_add_task_cancelled(mock_questionary, empty_storage):
    """Add task handles cancellation."""
    # User cancels (Ctrl+C)
    mock_questionary.text.return_value.ask.return_value = None

    add_task(empty_storage)

    assert len(empty_storage.get_all()) == 0


@patch("todo.commands.display")
def test_list_tasks_empty(mock_display, empty_storage):
    """List tasks shows empty state when no tasks."""
    list_tasks(empty_storage)
    mock_display.show_empty_state.assert_called_once()


@patch("todo.commands.display")
def test_list_tasks_displays_table(mock_display, storage_with_tasks):
    """List tasks displays table with tasks."""
    list_tasks(storage_with_tasks)
    mock_display.show_task_table.assert_called_once()


@patch("todo.commands.questionary")
@patch("todo.commands._prompt_select_task")
def test_mark_complete_changes_status(mock_select, mock_questionary, empty_storage):
    """Mark complete changes task status."""
    task = Task(title="Test Task")
    empty_storage.add(task)

    mock_select.return_value = task

    mark_complete(empty_storage)

    updated = empty_storage.get(task.id)
    assert updated is not None
    assert updated.is_completed is True
    assert updated.completed_at is not None


@patch("todo.commands.questionary")
@patch("todo.commands._prompt_select_task")
def test_mark_incomplete_changes_status(mock_select, mock_questionary, empty_storage):
    """Mark incomplete changes task status."""
    task = Task(title="Test Task", is_completed=True)
    empty_storage.add(task)

    mock_select.return_value = task

    mark_incomplete(empty_storage)

    updated = empty_storage.get(task.id)
    assert updated is not None
    assert updated.is_completed is False
    assert updated.completed_at is None


@patch("todo.commands.questionary")
@patch("todo.commands._prompt_select_task")
def test_delete_task_confirmed(mock_select, mock_questionary, empty_storage):
    """Delete task removes task when confirmed."""
    task = Task(title="Test Task")
    empty_storage.add(task)

    mock_select.return_value = task
    mock_questionary.select.return_value.ask.return_value = True  # Confirm deletion

    delete_task(empty_storage)

    assert empty_storage.get(task.id) is None


@patch("todo.commands.questionary")
@patch("todo.commands._prompt_select_task")
def test_delete_task_cancelled(mock_select, mock_questionary, empty_storage):
    """Delete task keeps task when cancelled."""
    task = Task(title="Test Task")
    empty_storage.add(task)

    mock_select.return_value = task
    mock_questionary.select.return_value.ask.return_value = False  # Cancel deletion

    delete_task(empty_storage)

    assert empty_storage.get(task.id) is not None
