"""
Unit tests for Phase 6 - User Story 4: Complete Tasks via Chat (T070-T072).

This test suite verifies the complete_task agent tool functionality.
"""

from uuid import uuid4

import pytest

from todo_api.agent.todo_agent import complete_task, set_current_user_id
from todo_api.database import AsyncSessionLocal
from todo_api.models import Task
from todo_api.models.enums import PriorityEnum


class TestCompleteTaskTool:
    """Test suite for complete_task agent tool (T070)."""

    @pytest.mark.asyncio
    async def test_complete_task_by_id(self, test_user_id: str):
        """Test completing a task by its UUID."""
        set_current_user_id(test_user_id)

        # Create a task directly in database
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=test_user_id,
                title="Buy groceries",
                description="Milk and eggs",
                priority=PriorityEnum.MEDIUM,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Complete the task using the tool
        result = await complete_task(task_id=task_id)

        # Verify result
        assert result["id"] == task_id
        assert result["title"] == "Buy groceries"
        assert result["is_completed"] is True
        assert result["completed_at"] is not None

        # Verify in database
        async with AsyncSessionLocal() as session:
            from sqlmodel import select

            statement = select(Task).where(Task.id == task.id)
            db_result = await session.execute(statement)
            db_task = db_result.scalar_one()

            assert db_task.is_completed is True
            assert db_task.completed_at is not None

    @pytest.mark.asyncio
    async def test_complete_task_already_completed(self, test_user_id: str):
        """Test completing an already completed task (should succeed idempotently)."""
        set_current_user_id(test_user_id)

        # Create a completed task
        async with AsyncSessionLocal() as session:
            from datetime import datetime

            now_naive = datetime.utcnow()
            task = Task(
                user_id=test_user_id,
                title="Already done",
                priority=PriorityEnum.LOW,
                is_completed=True,
                completed_at=now_naive,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Complete it again
        result = await complete_task(task_id=task_id)

        # Should succeed
        assert result["is_completed"] is True
        assert result["completed_at"] is not None

    @pytest.mark.asyncio
    async def test_complete_task_not_found(self, test_user_id: str):
        """Test completing a non-existent task (T072)."""
        set_current_user_id(test_user_id)

        # Try to complete a task that doesn't exist
        fake_task_id = str(uuid4())

        with pytest.raises(ValueError, match=r"Task .* not found or access denied"):
            await complete_task(task_id=fake_task_id)

    @pytest.mark.asyncio
    async def test_complete_task_wrong_user(self, test_user_id: str):
        """Test completing another user's task (should fail with access denied)."""
        # Create task for different user
        other_user_id = str(uuid4())
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=other_user_id,
                title="Other user's task",
                priority=PriorityEnum.HIGH,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Try to complete it as test_user_id
        set_current_user_id(test_user_id)

        with pytest.raises(ValueError, match=r"Task .* not found or access denied"):
            await complete_task(task_id=task_id)

    @pytest.mark.asyncio
    async def test_complete_task_updates_timestamps(self, test_user_id: str):
        """Test that complete_task updates both completed_at and updated_at timestamps."""
        set_current_user_id(test_user_id)

        # Create a task
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=test_user_id,
                title="Task with timestamps",
                priority=PriorityEnum.MEDIUM,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)
            original_created_at = task.created_at

        # Complete the task
        result = await complete_task(task_id=task_id)

        # Verify timestamps
        assert result["completed_at"] is not None
        assert result["updated_at"] is not None
        assert result["created_at"] == original_created_at.isoformat()

        # completed_at and updated_at should be recent
        from datetime import datetime, timezone

        completed_at = datetime.fromisoformat(result["completed_at"])
        updated_at = datetime.fromisoformat(result["updated_at"])

        # Both should be within last 5 seconds
        now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
        time_diff_completed = abs((now_utc - completed_at).total_seconds())
        time_diff_updated = abs((now_utc - updated_at).total_seconds())

        assert time_diff_completed < 5
        assert time_diff_updated < 5
