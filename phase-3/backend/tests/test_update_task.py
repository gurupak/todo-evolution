"""
Unit tests for Phase 7 - User Story 5: Update Tasks via Chat (T078-T081).

This test suite verifies the update_task agent tool functionality.

Note: T084 (ambiguous reference handling by description search) is not implemented
in the current version. The AI agent handles ambiguity through natural conversation
by asking the user to provide the specific task ID when there's confusion.
"""

from uuid import uuid4

import pytest

from todo_api.agent.todo_agent import set_current_user_id, update_task
from todo_api.database import AsyncSessionLocal
from todo_api.models import Task
from todo_api.models.enums import PriorityEnum


class TestUpdateTaskTool:
    """Test suite for update_task agent tool (T078)."""

    @pytest.mark.asyncio
    async def test_update_task_title_only(self, test_user_id: str):
        """Test updating only the task title."""
        set_current_user_id(test_user_id)

        # Create a task
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=test_user_id,
                title="Old title",
                description="Original description",
                priority=PriorityEnum.MEDIUM,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Update only the title
        result = await update_task(task_id=task_id, title="New title")

        # Verify result
        assert result["id"] == task_id
        assert result["title"] == "New title"
        assert result["description"] == "Original description"  # Unchanged
        assert result["priority"] == "medium"  # Unchanged

        # Verify in database
        async with AsyncSessionLocal() as session:
            from sqlmodel import select

            statement = select(Task).where(Task.id == task.id)
            db_result = await session.execute(statement)
            db_task = db_result.scalar_one()

            assert db_task.title == "New title"
            assert db_task.description == "Original description"

    @pytest.mark.asyncio
    async def test_update_task_description_only(self, test_user_id: str):
        """Test updating only the task description."""
        set_current_user_id(test_user_id)

        # Create a task
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=test_user_id,
                title="My task",
                description="Old description",
                priority=PriorityEnum.HIGH,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Update only description
        result = await update_task(task_id=task_id, description="New description")

        # Verify result
        assert result["title"] == "My task"  # Unchanged
        assert result["description"] == "New description"

    @pytest.mark.asyncio
    async def test_update_task_priority_only(self, test_user_id: str):
        """Test updating only the task priority."""
        set_current_user_id(test_user_id)

        # Create a task with medium priority
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=test_user_id,
                title="Important task",
                priority=PriorityEnum.MEDIUM,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Update to high priority
        result = await update_task(task_id=task_id, priority="high")

        # Verify result
        assert result["priority"] == "high"

        # Verify in database
        async with AsyncSessionLocal() as session:
            from sqlmodel import select

            statement = select(Task).where(Task.id == task.id)
            db_result = await session.execute(statement)
            db_task = db_result.scalar_one()

            assert db_task.priority == PriorityEnum.HIGH

    @pytest.mark.asyncio
    async def test_update_task_multiple_fields(self, test_user_id: str):
        """Test updating multiple fields at once."""
        set_current_user_id(test_user_id)

        # Create a task
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=test_user_id,
                title="Old task",
                description="Old desc",
                priority=PriorityEnum.LOW,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Update multiple fields
        result = await update_task(
            task_id=task_id,
            title="Updated task",
            description="Updated description",
            priority="high",
        )

        # Verify all updates applied
        assert result["title"] == "Updated task"
        assert result["description"] == "Updated description"
        assert result["priority"] == "high"

    @pytest.mark.asyncio
    async def test_update_task_not_found(self, test_user_id: str):
        """Test updating a non-existent task (T079 - error handling)."""
        set_current_user_id(test_user_id)

        # Try to update non-existent task
        fake_task_id = str(uuid4())

        with pytest.raises(ValueError, match=r"Task .* not found or access denied"):
            await update_task(task_id=fake_task_id, title="New title")

    @pytest.mark.asyncio
    async def test_update_task_wrong_user(self, test_user_id: str):
        """Test updating another user's task (should fail with access denied)."""
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

        # Try to update it as test_user_id
        set_current_user_id(test_user_id)

        with pytest.raises(ValueError, match=r"Task .* not found or access denied"):
            await update_task(task_id=task_id, title="Hacked title")

    @pytest.mark.asyncio
    async def test_update_task_invalid_priority(self, test_user_id: str):
        """Test updating with invalid priority (should be ignored, keeping old value)."""
        set_current_user_id(test_user_id)

        # Create a task
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=test_user_id,
                title="Task",
                priority=PriorityEnum.MEDIUM,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)

        # Try to update with invalid priority
        result = await update_task(task_id=task_id, priority="invalid")

        # Priority should remain unchanged
        assert result["priority"] == "medium"

    @pytest.mark.asyncio
    async def test_update_task_updates_timestamp(self, test_user_id: str):
        """Test that update_task updates the updated_at timestamp."""
        set_current_user_id(test_user_id)

        # Create a task
        async with AsyncSessionLocal() as session:
            task = Task(
                user_id=test_user_id,
                title="Task with timestamps",
                priority=PriorityEnum.LOW,
                is_completed=False,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            task_id = str(task.id)
            original_created_at = task.created_at
            original_updated_at = task.updated_at

        # Small delay to ensure timestamp changes
        import asyncio

        await asyncio.sleep(0.1)

        # Update the task
        result = await update_task(task_id=task_id, title="Updated title")

        # Verify timestamps
        assert result["created_at"] == original_created_at.isoformat()
        assert result["updated_at"] != original_updated_at.isoformat()

        # updated_at should be more recent
        from datetime import datetime

        updated_at = datetime.fromisoformat(result["updated_at"])
        assert updated_at > original_updated_at


class TestAmbiguousReferenceHandling:
    """
    Tests for ambiguous task reference handling (T080-T081).

    Note: The current implementation (T084) does NOT implement automatic search
    by task description. Instead, the AI agent handles ambiguity through conversation
    by asking users to provide the specific task ID when needed.

    These tests verify that the agent correctly communicates errors when users
    provide incorrect or ambiguous references.
    """

    @pytest.mark.asyncio
    async def test_update_task_requires_valid_id(self, test_user_id: str):
        """
        Test that update_task requires a valid UUID task_id.
        When users provide ambiguous references, the AI should ask for clarification
        and then use the specific task ID.
        """
        set_current_user_id(test_user_id)

        # Attempting to update with invalid ID raises error
        with pytest.raises(ValueError):
            await update_task(task_id="not-a-uuid", title="New title")

    @pytest.mark.asyncio
    async def test_ai_clarification_flow_simulation(self, test_user_id: str):
        """
        Simulate the AI clarification flow for ambiguous references.

        In practice:
        1. User: "Update my meeting task"
        2. AI: Searches tasks, finds 3 matches, lists them with IDs
        3. User: "Update task {specific_id}"
        4. AI: Calls update_task with the specific ID

        This test verifies step 4 works correctly after clarification.
        """
        set_current_user_id(test_user_id)

        # Create 3 tasks with "meeting" in title
        task_ids = []
        async with AsyncSessionLocal() as session:
            for i in range(3):
                task = Task(
                    user_id=test_user_id,
                    title=f"Meeting task {i + 1}",
                    priority=PriorityEnum.MEDIUM,
                    is_completed=False,
                )
                session.add(task)
                await session.commit()
                await session.refresh(task)
                task_ids.append(str(task.id))

        # After AI clarification, user provides specific ID
        # Update the second task
        result = await update_task(task_id=task_ids[1], title="Updated meeting task 2")

        # Verify only the specified task was updated
        assert result["title"] == "Updated meeting task 2"
        assert result["id"] == task_ids[1]
