"""
Integration tests for Phase 6 - User Story 4: Complete Tasks via Chat (T077).

This test suite verifies the end-to-end flow of completing tasks through the chat interface.
"""

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.models.task import PriorityEnum, Task


@pytest.mark.asyncio
async def test_full_integration_complete_task_via_chat(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Create task 'Buy groceries' →
    Chat 'Finished groceries' or 'Mark groceries as complete' →
    Verify task marked complete in chat response and Phase II UI.
    """
    # Step 1: Create a pending task directly in database
    task = Task(
        user_id=test_user_id,
        title="Buy groceries",
        description="Milk, eggs, and bread",
        priority=PriorityEnum.HIGH,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Step 2: Send chat message to complete the task
    chat_payload = {"message": f"Mark task {task_id} as complete"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Step 3: Verify chat response indicates success
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "response" in data

    response_text = data["response"].lower()

    # Verify completion is mentioned in response
    assert any(keyword in response_text for keyword in ["complete", "done", "finished", "marked"])

    # Step 4: Verify task is completed in database (Phase II UI would see this)
    await session.refresh(task)
    assert task.is_completed is True
    assert task.completed_at is not None


@pytest.mark.asyncio
async def test_integration_complete_task_by_natural_language(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Create task →
    Use natural language 'I finished buying groceries' →
    AI should understand intent and complete the task.
    """
    # Step 1: Create a pending task
    task = Task(
        user_id=test_user_id,
        title="Buy groceries",
        description="Shopping for the week",
        priority=PriorityEnum.MEDIUM,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Step 2: Use natural language to indicate completion
    # Note: The AI needs the task ID to know which task to complete
    chat_payload = {"message": f"I finished task {task_id}"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Step 3: Verify success
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

    # Step 4: Verify task completed in database
    await session.refresh(task)
    assert task.is_completed is True


@pytest.mark.asyncio
async def test_integration_complete_nonexistent_task(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Try to complete a non-existent task →
    AI should return error message about task not found.
    """
    from uuid import uuid4

    fake_task_id = str(uuid4())

    # Try to complete non-existent task
    chat_payload = {"message": f"Complete task {fake_task_id}"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Should still return 200 (chat succeeded, but tool reported error)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

    response_text = data["response"].lower()

    # AI should communicate the error to user
    assert any(
        keyword in response_text
        for keyword in ["not found", "doesn't exist", "couldn't find", "unable"]
    )


@pytest.mark.asyncio
async def test_integration_complete_already_completed_task(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Complete an already completed task →
    Should succeed idempotently with appropriate message.
    """
    from datetime import datetime

    # Create a completed task
    now_naive = datetime.utcnow()
    task = Task(
        user_id=test_user_id,
        title="Email client",
        priority=PriorityEnum.LOW,
        is_completed=True,
        completed_at=now_naive,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Try to complete it again
    chat_payload = {"message": f"Mark task {task_id} as done"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Should succeed
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

    # Task should still be completed
    await session.refresh(task)
    assert task.is_completed is True
