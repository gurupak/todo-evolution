"""Tests for MCP (Model Context Protocol) tools.

These tests verify that MCP tools correctly interact with the database
and enforce user data isolation.
"""

from uuid import uuid4

import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from todo_api.mcp.tools import list_tasks

from todo_api.models import PriorityEnum, Task


class TestListTasksTool:
    """Test suite for list_tasks MCP tool."""

    @pytest.mark.asyncio
    async def test_list_tasks_returns_all_user_tasks(
        self, session: AsyncSession, test_user_id: str
    ):
        """Test that list_tasks returns all tasks for a given user."""
        # Create test tasks for the user
        task1 = Task(
            user_id=test_user_id,
            title="Buy groceries",
            description="Milk, eggs, bread",
            priority=PriorityEnum.HIGH,
            status="pending",
        )
        task2 = Task(
            user_id=test_user_id,
            title="Call mom",
            description="Birthday call",
            priority=PriorityEnum.MEDIUM,
            status="completed",
        )
        session.add(task1)
        session.add(task2)
        await session.commit()

        # Call list_tasks tool
        result = await list_tasks(user_id=test_user_id, session=session)

        # Verify results
        assert len(result) == 2
        titles = {task["title"] for task in result}
        assert "Buy groceries" in titles
        assert "Call mom" in titles

    @pytest.mark.asyncio
    async def test_list_tasks_filters_by_user_id(self, session: AsyncSession, test_user_id: str):
        """Test that list_tasks only returns tasks for the specified user."""
        # Create task for test user
        task1 = Task(
            user_id=test_user_id,
            title="Test user task",
            priority=PriorityEnum.LOW,
            status="pending",
        )
        session.add(task1)

        # Create task for different user
        other_user_id = "other-user-123"
        task2 = Task(
            user_id=other_user_id,
            title="Other user task",
            priority=PriorityEnum.HIGH,
            status="pending",
        )
        session.add(task2)
        await session.commit()

        # Call list_tasks for test user
        result = await list_tasks(user_id=test_user_id, session=session)

        # Verify only test user's task is returned
        assert len(result) == 1
        assert result[0]["title"] == "Test user task"
        assert result[0]["user_id"] == test_user_id

    @pytest.mark.asyncio
    async def test_list_tasks_returns_empty_list_for_user_with_no_tasks(
        self, session: AsyncSession, test_user_id: str
    ):
        """Test that list_tasks returns empty list when user has no tasks."""
        result = await list_tasks(user_id=test_user_id, session=session)
        assert result == []

    @pytest.mark.asyncio
    async def test_list_tasks_includes_all_task_fields(
        self, session: AsyncSession, test_user_id: str
    ):
        """Test that list_tasks returns all relevant task fields."""
        task = Task(
            user_id=test_user_id,
            title="Complete project",
            description="Finish Phase III implementation",
            priority=PriorityEnum.HIGH,
            status="pending",
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

        result = await list_tasks(user_id=test_user_id, session=session)

        assert len(result) == 1
        task_dict = result[0]
        assert "id" in task_dict
        assert task_dict["user_id"] == test_user_id
        assert task_dict["title"] == "Complete project"
        assert task_dict["description"] == "Finish Phase III implementation"
        assert task_dict["priority"] == "HIGH"
        assert task_dict["status"] == "pending"
        assert "created_at" in task_dict
        assert "updated_at" in task_dict

    @pytest.mark.asyncio
    async def test_list_tasks_orders_by_created_at_desc(
        self, session: AsyncSession, test_user_id: str
    ):
        """Test that list_tasks returns tasks in reverse chronological order."""
        # Create tasks with slight delay to ensure different timestamps
        task1 = Task(
            user_id=test_user_id, title="First task", priority=PriorityEnum.LOW, status="pending"
        )
        session.add(task1)
        await session.commit()

        task2 = Task(
            user_id=test_user_id, title="Second task", priority=PriorityEnum.LOW, status="pending"
        )
        session.add(task2)
        await session.commit()

        result = await list_tasks(user_id=test_user_id, session=session)

        # Verify newest task is first
        assert len(result) == 2
        assert result[0]["title"] == "Second task"
        assert result[1]["title"] == "First task"
