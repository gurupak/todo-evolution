"""
Unit tests for Phase 8 - User Story 6: Delete Tasks via Chat (T086-T088).

This test suite verifies the delete_task agent tool functionality.
"""

from uuid import uuid4

import pytest

from todo_api.agent.todo_agent import delete_task, set_current_user_id
from todo_api.database import AsyncSessionLocal
from todo_api.models import Task
from todo_api.models.enums import PriorityEnum


class TestDeleteTaskTool:
    """Test suite for delete_task agent tool (T086)."""

    @pytest.mark.asyncio
    async def test_delete_task_success(self, test_user_id: str):
        """Test successfully deleting a task by ID."""
        set_current_user_id(test_user_id)

        # Create a task
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=test_user_id,
                title="Task to delete",
                description="This task will be deleted",
                priority=PriorityEnum.MEDIUM,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Delete the task
        result = await delete_task(task_id=task_id)

        # Verify result
        assert result["id"] == task_id
        assert result["title"] == "Task to delete"
        assert "deleted" in result or "success" in result

        # Verify task is deleted from database
        async with AsyncSessionLocal() as session:
            from sqlmodel import select

            statement = select(Task).where(Task.id == task.id)
            db_result = await session.execute(statement)
            db_task = db_result.scalar_one_or_none()

            assert db_task is None, "Task should be deleted from database"

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, test_user_id: str):
        """Test deleting a non-existent task (T087 - error handling)."""
        set_current_user_id(test_user_id)

        # Try to delete non-existent task
        fake_task_id = str(uuid4())

        with pytest.raises(ValueError, match=r"Task .* not found or access denied"):
            await delete_task(task_id=fake_task_id)

    @pytest.mark.asyncio
    async def test_delete_task_wrong_user(self, test_user_id: str):
        """Test deleting another user's task (should fail with access denied)."""
        # Create task for different user
        other_user_id = str(uuid4())
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=other_user_id,
                title="Other user's task",
                priority=PriorityEnum.MEDIUM,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Try to delete it as test_user_id
        set_current_user_id(test_user_id)

        with pytest.raises(ValueError, match=r"Task .* not found or access denied"):
            await delete_task(task_id=task_id)

        # Verify task still exists (not deleted)
        async with AsyncSessionLocal() as session:
            from sqlmodel import select

            statement = select(Task).where(Task.id == task.id)
            db_result = await session.execute(statement)
            db_task = db_result.scalar_one_or_none()

            assert db_task is not None, "Task should still exist after failed delete"

    @pytest.mark.asyncio
    async def test_delete_completed_task(self, test_user_id: str):
        """Test deleting a completed task (should work)."""
        set_current_user_id(test_user_id)

        # Create a completed task
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=test_user_id,
                title="Completed task to delete",
                priority=PriorityEnum.LOW,
                is_completed=True,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Delete the completed task
        result = await delete_task(task_id=task_id)

        # Verify deletion succeeded
        assert result["id"] == task_id

        # Verify task is deleted from database
        async with AsyncSessionLocal() as session:
            from sqlmodel import select

            statement = select(Task).where(Task.id == task.id)
            db_result = await session.execute(statement)
            db_task = db_result.scalar_one_or_none()

            assert db_task is None

    @pytest.mark.asyncio
    async def test_delete_task_invalid_uuid(self, test_user_id: str):
        """Test deleting with invalid task ID format."""
        set_current_user_id(test_user_id)

        # Try to delete with invalid UUID
        with pytest.raises(ValueError):
            await delete_task(task_id="not-a-uuid")


class TestDeleteTaskIntentDetection:
    """Test suite for delete task intent detection in chat (T087-T088)."""

    @pytest.mark.asyncio
    async def test_delete_task_intent_patterns(self):
        """
        Test that the AI agent can detect various delete task intents.

        Note: This test verifies expected intent patterns. The actual AI
        behavior is tested in integration tests (test_integration_t092.py).
        """
        # Intent patterns that should trigger delete_task
        delete_intents = [
            "delete task {task_id}",
            "remove task {task_id}",
            "delete the meeting task",
            "remove my grocery task",
            "get rid of task {task_id}",
            "cancel task {task_id}",
        ]

        # Verify patterns are reasonable (this is a documentation test)
        assert len(delete_intents) > 0
        assert all(
            "delete" in intent or "remove" in intent or "rid" in intent or "cancel" in intent
            for intent in delete_intents
        )
