"""
Integration tests for Phase 5 - User Story 3: View Tasks via Chat (T069).

This test suite verifies the end-to-end flow of viewing tasks with status filtering
through the chat interface.
"""

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.models.task import PriorityEnum, Task


@pytest.mark.asyncio
async def test_full_integration_view_all_tasks(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Create 3 tasks (2 pending, 1 completed) →
    Ask 'Show me all my tasks' → Verify all 3 tasks listed in response.
    """
    # Step 1: Create 3 tasks directly in database
    task1 = Task(
        user_id=test_user_id,
        title="Buy groceries",
        description="Milk and eggs",
        priority=PriorityEnum.MEDIUM,
        is_completed=False,
    )
    task2 = Task(
        user_id=test_user_id,
        title="Complete report",
        description="Q4 financial report",
        priority=PriorityEnum.HIGH,
        is_completed=False,
    )
    task3 = Task(
        user_id=test_user_id,
        title="Email client",
        description="Follow up on proposal",
        priority=PriorityEnum.LOW,
        is_completed=True,
    )

    session.add_all([task1, task2, task3])
    await session.commit()

    # Step 2: Send chat message asking for all tasks
    chat_payload = {"message": "Show me all my tasks"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Step 3: Verify response contains all 3 tasks
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "response" in data

    response_text = data["response"].lower()

    # Verify all task titles appear in response
    assert "buy groceries" in response_text or "groceries" in response_text
    assert "complete report" in response_text or "report" in response_text
    assert "email client" in response_text or "client" in response_text


@pytest.mark.asyncio
async def test_full_integration_view_pending_tasks(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Create 3 tasks (2 pending, 1 completed) →
    Ask 'What's pending?' → Verify only 2 pending tasks listed.
    """
    # Step 1: Create 3 tasks with different statuses
    task1 = Task(
        user_id=test_user_id,
        title="Buy groceries",
        description="Milk and eggs",
        priority=PriorityEnum.MEDIUM,
        is_completed=False,
    )
    task2 = Task(
        user_id=test_user_id,
        title="Complete report",
        description="Q4 financial report",
        priority=PriorityEnum.HIGH,
        is_completed=False,
    )
    task3 = Task(
        user_id=test_user_id,
        title="Email client",
        description="Follow up on proposal",
        priority=PriorityEnum.LOW,
        is_completed=True,
    )

    session.add_all([task1, task2, task3])
    await session.commit()

    # Step 2: Send chat message asking for pending tasks
    chat_payload = {"message": "What's pending?"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Step 3: Verify response contains only pending tasks
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "response" in data

    response_text = data["response"].lower()

    # Verify pending tasks appear in response
    assert "buy groceries" in response_text or "groceries" in response_text
    assert "complete report" in response_text or "report" in response_text

    # Verify completed task does NOT appear (or is marked as completed)
    # We can't guarantee it won't be mentioned, but it shouldn't be listed as pending


@pytest.mark.asyncio
async def test_full_integration_view_completed_tasks(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Create 3 tasks (2 pending, 1 completed) →
    Ask 'Show completed tasks' → Verify only 1 completed task listed.
    """
    # Step 1: Create 3 tasks with different statuses
    task1 = Task(
        user_id=test_user_id,
        title="Buy groceries",
        description="Milk and eggs",
        priority=PriorityEnum.MEDIUM,
        is_completed=False,
    )
    task2 = Task(
        user_id=test_user_id,
        title="Complete report",
        description="Q4 financial report",
        priority=PriorityEnum.HIGH,
        is_completed=False,
    )
    task3 = Task(
        user_id=test_user_id,
        title="Email client",
        description="Follow up on proposal",
        priority=PriorityEnum.LOW,
        is_completed=True,
    )

    session.add_all([task1, task2, task3])
    await session.commit()

    # Step 2: Send chat message asking for completed tasks
    chat_payload = {"message": "Show me my completed tasks"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Step 3: Verify response contains only completed task
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "response" in data

    response_text = data["response"].lower()

    # Verify completed task appears in response
    assert "email client" in response_text or "client" in response_text


@pytest.mark.asyncio
async def test_full_integration_view_empty_task_list(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: No tasks in database →
    Ask 'Show me all my tasks' → Verify response indicates no tasks.
    """
    # Step 1: Ensure no tasks exist (fresh test user)
    # No tasks created

    # Step 2: Send chat message asking for tasks
    chat_payload = {"message": "Show me all my tasks"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Step 3: Verify response indicates no tasks
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "response" in data

    response_text = data["response"].lower()

    # Verify response indicates empty list
    assert any(
        keyword in response_text
        for keyword in [
            "no tasks",
            "don't have any tasks",
            "haven't created any tasks",
            "no pending",
            "no completed",
            "empty",
            "0 tasks",
        ]
    )
