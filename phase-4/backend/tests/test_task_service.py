"""Tests for TaskService business logic."""

from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from todo_api.models.task import PriorityEnum, Task
from todo_api.schemas.task import TaskCreateRequest, TaskUpdateRequest
from todo_api.services.task_service import TaskService


@pytest.mark.asyncio
async def test_create_task(session: AsyncSession, test_user_id: str):
    """Test creating a task (T063)."""
    service = TaskService(session)
    data = TaskCreateRequest(
        title="Test Task",
        description="Test Description",
        priority=PriorityEnum.HIGH,
    )

    task = await service.create(test_user_id, data)

    assert task.id is not None
    assert task.user_id == test_user_id
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == PriorityEnum.HIGH
    assert task.is_completed is False
    assert task.created_at is not None
    assert task.updated_at is not None


@pytest.mark.asyncio
async def test_get_all_filters_by_user_id(session: AsyncSession):
    """Test get_all filters tasks by user_id (T060, T064)."""
    service = TaskService(session)
    user1_id = str(uuid4())
    user2_id = str(uuid4())

    # Create tasks for user 1
    data = TaskCreateRequest(title="User 1 Task", description="", priority=PriorityEnum.MEDIUM)
    await service.create(user1_id, data)
    await service.create(user1_id, data)

    # Create tasks for user 2
    await service.create(user2_id, data)

    # Get tasks for user 1
    response = await service.get_all(user1_id)

    assert response.total == 2
    assert response.completed == 0
    assert response.pending == 2
    assert len(response.tasks) == 2
    assert all(task.user_id == user1_id for task in response.tasks)


@pytest.mark.asyncio
async def test_get_by_id_returns_task(session: AsyncSession, test_user_id: str):
    """Test get_by_id returns correct task (T065)."""
    service = TaskService(session)
    data = TaskCreateRequest(title="Test Task", description="", priority=PriorityEnum.LOW)

    created_task = await service.create(test_user_id, data)
    retrieved_task = await service.get_by_id(created_task.id, test_user_id)

    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Test Task"


@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_other_user(session: AsyncSession):
    """Test get_by_id returns None for other user's task (T060)."""
    service = TaskService(session)
    user1_id = str(uuid4())
    user2_id = str(uuid4())

    data = TaskCreateRequest(title="User 1 Task", description="", priority=PriorityEnum.MEDIUM)
    task = await service.create(user1_id, data)

    # Try to get user 1's task as user 2
    result = await service.get_by_id(task.id, user2_id)

    assert result is None


@pytest.mark.asyncio
async def test_update_task(session: AsyncSession, test_user_id: str):
    """Test updating a task."""
    service = TaskService(session)
    data = TaskCreateRequest(title="Original", description="", priority=PriorityEnum.LOW)
    task = await service.create(test_user_id, data)

    update_data = TaskUpdateRequest(title="Updated", priority=PriorityEnum.HIGH)
    updated_task = await service.update(task.id, test_user_id, update_data)

    assert updated_task is not None
    assert updated_task.title == "Updated"
    assert updated_task.priority == PriorityEnum.HIGH


@pytest.mark.asyncio
async def test_toggle_complete_sets_completed(session: AsyncSession, test_user_id: str):
    """Test toggle_complete marks task as completed (T090)."""
    service = TaskService(session)
    data = TaskCreateRequest(title="Test Task", description="", priority=PriorityEnum.MEDIUM)
    task = await service.create(test_user_id, data)

    # Mark as completed
    completed_task = await service.toggle_complete(task.id, test_user_id)

    assert completed_task is not None
    assert completed_task.is_completed is True
    assert completed_task.completed_at is not None


@pytest.mark.asyncio
async def test_toggle_complete_unmarks_completed(session: AsyncSession, test_user_id: str):
    """Test toggle_complete unmarks completed task (T093)."""
    service = TaskService(session)
    data = TaskCreateRequest(title="Test Task", description="", priority=PriorityEnum.MEDIUM)
    task = await service.create(test_user_id, data)

    # Mark as completed
    await service.toggle_complete(task.id, test_user_id)

    # Toggle back to incomplete
    incomplete_task = await service.toggle_complete(task.id, test_user_id)

    assert incomplete_task is not None
    assert incomplete_task.is_completed is False
    assert incomplete_task.completed_at is None


@pytest.mark.asyncio
async def test_toggle_complete_sets_timestamp(session: AsyncSession, test_user_id: str):
    """Test toggle_complete sets completed_at timestamp (T092)."""
    service = TaskService(session)
    data = TaskCreateRequest(title="Test Task", description="", priority=PriorityEnum.MEDIUM)
    task = await service.create(test_user_id, data)

    # Mark as completed
    completed_task = await service.toggle_complete(task.id, test_user_id)

    assert completed_task.completed_at is not None
    assert completed_task.completed_at >= task.created_at


@pytest.mark.asyncio
async def test_delete_task(session: AsyncSession, test_user_id: str):
    """Test deleting a task."""
    service = TaskService(session)
    data = TaskCreateRequest(title="To Delete", description="", priority=PriorityEnum.LOW)
    task = await service.create(test_user_id, data)

    # Delete the task
    deleted = await service.delete(task.id, test_user_id)
    assert deleted is True

    # Verify it's gone
    result = await service.get_by_id(task.id, test_user_id)
    assert result is None
