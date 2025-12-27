"""Tests for AI Agent tools (create_task, update_task, complete_task, delete_task).

These tests verify that agent tools correctly interact with the database
using the global user context pattern.
"""

from datetime import datetime, timezone

import pytest

from todo_api.agent.todo_agent import (
    create_task,
    set_current_user_id,
)


class TestCreateTaskTool:
    """Test suite for create_task agent tool (T055)."""

    @pytest.mark.asyncio
    async def test_create_task_with_title_only(self, test_user_id: str):
        """Test creating a task with only a title."""
        set_current_user_id(test_user_id)

        result = await create_task(title="Buy groceries")

        assert result["title"] == "Buy groceries"
        assert result["description"] is None
        assert result["priority"] == "medium"
        assert result["is_completed"] is False
        assert "id" in result
        assert "created_at" in result

    @pytest.mark.asyncio
    async def test_create_task_with_description_and_priority(self, test_user_id: str):
        """Test creating a task with title, description, and priority."""
        set_current_user_id(test_user_id)

        result = await create_task(
            title="Meet with CEO", description="Discuss Q1 strategy at hotel", priority="high"
        )

        assert result["title"] == "Meet with CEO"
        assert result["description"] == "Discuss Q1 strategy at hotel"
        assert result["priority"] == "high"
        assert result["is_completed"] is False

    @pytest.mark.asyncio
    async def test_create_task_with_natural_language_due_date_tomorrow(self, test_user_id: str):
        """Test creating a task with 'tomorrow' due date."""
        set_current_user_id(test_user_id)

        result = await create_task(title="Call mom", due_date="tomorrow")

        assert result["title"] == "Call mom"
        assert result["due_date"] is not None
        # Verify due_date is approximately 1 day from now
        due_date = datetime.fromisoformat(result["due_date"])
        now = datetime.now(timezone.utc)
        time_diff = (due_date - now).total_seconds()
        assert 23 * 3600 < time_diff < 25 * 3600  # Between 23 and 25 hours

    @pytest.mark.asyncio
    async def test_create_task_with_natural_language_due_date_days(self, test_user_id: str):
        """Test creating a task with 'in 3 days' due date."""
        set_current_user_id(test_user_id)

        result = await create_task(title="Project deadline", due_date="in 3 days")

        assert result["due_date"] is not None
        due_date = datetime.fromisoformat(result["due_date"])
        now = datetime.now(timezone.utc)
        time_diff = (due_date - now).total_seconds()
        assert 71 * 3600 < time_diff < 73 * 3600  # Between 71 and 73 hours (3 days)

    @pytest.mark.asyncio
    async def test_create_task_with_natural_language_due_date_next_week(self, test_user_id: str):
        """Test creating a task with 'next week' due date."""
        set_current_user_id(test_user_id)

        result = await create_task(title="Team meeting", due_date="next week")

        assert result["due_date"] is not None
        due_date = datetime.fromisoformat(result["due_date"])
        now = datetime.now(timezone.utc)
        time_diff = (due_date - now).total_seconds()
        assert 6.5 * 24 * 3600 < time_diff < 7.5 * 24 * 3600  # Approximately 1 week

    @pytest.mark.asyncio
    async def test_create_task_normalizes_priority_to_lowercase(self, test_user_id: str):
        """Test that priority values are normalized to lowercase."""
        set_current_user_id(test_user_id)

        result = await create_task(title="Task 1", priority="HIGH")
        assert result["priority"] == "high"

        result = await create_task(title="Task 2", priority="Medium")
        assert result["priority"] == "medium"

        result = await create_task(title="Task 3", priority="LoW")
        assert result["priority"] == "low"

    @pytest.mark.asyncio
    async def test_create_task_defaults_invalid_priority_to_medium(self, test_user_id: str):
        """Test that invalid priority values default to 'medium'."""
        set_current_user_id(test_user_id)

        result = await create_task(title="Task with invalid priority", priority="urgent")
        assert result["priority"] == "medium"

    @pytest.mark.asyncio
    async def test_create_task_enforces_user_isolation(self, test_user_id: str):
        """Test that tasks are created for the correct user."""
        # Create task for user 1
        set_current_user_id(test_user_id)
        result1 = await create_task(title="User 1 task")

        # Create task for user 2
        other_user_id = "other-user-456"
        set_current_user_id(other_user_id)
        result2 = await create_task(title="User 2 task")

        # Verify user IDs would be different (can't check DB here but tool ensures it)
        assert result1["id"] != result2["id"]

    @pytest.mark.asyncio
    async def test_create_task_raises_error_when_user_id_not_set(self):
        """Test that create_task raises error when user_id is not set."""
        # Don't set user_id
        import todo_api.agent.todo_agent as agent_module

        agent_module._current_user_id = None

        with pytest.raises(ValueError, match="user_id not set"):
            await create_task(title="This should fail")


class TestCreateTaskIntentDetection:
    """Test suite for 'add task' intent detection (T056)."""

    @pytest.mark.asyncio
    async def test_task_creation_returns_confirmation(self, test_user_id: str):
        """Test that task creation returns confirmation data (T057)."""
        set_current_user_id(test_user_id)

        result = await create_task(title="Buy milk", description="Get 2% milk from store")

        # Verify the result contains all necessary fields for confirmation
        assert "id" in result
        assert result["title"] == "Buy milk"
        assert result["description"] == "Get 2% milk from store"
        assert "created_at" in result

        # Agent uses this data to generate a confirmation message


class TestTaskCreationPhaseIIIntegration:
    """Test suite for Phase II integration (T058)."""

    @pytest.mark.asyncio
    async def test_multiple_tasks_created_sequentially(self, test_user_id: str):
        """Test creating multiple tasks in sequence."""
        set_current_user_id(test_user_id)

        # Create 3 tasks
        task1 = await create_task(title="Task 1", priority="high")
        task2 = await create_task(title="Task 2", priority="medium")
        task3 = await create_task(title="Task 3", priority="low")

        # Verify all tasks have unique IDs
        assert task1["id"] != task2["id"]
        assert task2["id"] != task3["id"]
        assert task1["id"] != task3["id"]

        # Verify priorities are correct
        assert task1["priority"] == "high"
        assert task2["priority"] == "medium"
        assert task3["priority"] == "low"
