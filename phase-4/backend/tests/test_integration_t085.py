"""
Integration tests for Phase 7 - User Story 5: Update Tasks via Chat (T085).

This test suite verifies the end-to-end flow of updating tasks through the chat interface.
"""

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.models.task import PriorityEnum, Task


@pytest.mark.asyncio
async def test_full_integration_update_task_via_chat(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Create task 'Buy groceries' →
    Chat 'Update task {id} to "Buy milk and eggs"' →
    Verify task updated in chat response and Phase II UI.
    """
    # Step 1: Create a task directly in database
    task = Task(
        user_id=test_user_id,
        title="Buy groceries",
        description="Shopping list",
        priority=PriorityEnum.MEDIUM,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Step 2: Send chat message to update the task
    chat_payload = {"message": f'Update task {task_id} title to "Buy milk and eggs"'}

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

    # Verify update is mentioned in response
    assert any(keyword in response_text for keyword in ["update", "changed", "modified"])

    # Step 4: Verify task is updated in database (Phase II UI would see this)
    await session.refresh(task)
    assert task.title == "Buy milk and eggs"
    assert task.description == "Shopping list"  # Unchanged


@pytest.mark.asyncio
async def test_integration_update_task_priority(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Create task →
    Chat 'Change task {id} to high priority' →
    Verify priority updated.
    """
    # Create a medium priority task
    task = Task(
        user_id=test_user_id,
        title="Complete report",
        priority=PriorityEnum.MEDIUM,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Update priority via chat
    chat_payload = {"message": f"Change task {task_id} to high priority"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Verify success
    assert response.status_code == 200

    # Verify priority updated in database
    await session.refresh(task)
    assert task.priority == PriorityEnum.HIGH


@pytest.mark.asyncio
async def test_integration_update_task_multiple_fields(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Update multiple task fields in one chat message.
    """
    # Create a task
    task = Task(
        user_id=test_user_id,
        title="Old task",
        description="Old description",
        priority=PriorityEnum.LOW,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Update multiple fields
    chat_payload = {
        "message": f'Update task {task_id}: change title to "New task", '
        f'description to "New description", and set priority to high'
    }

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Verify success
    assert response.status_code == 200

    # Verify all fields updated
    await session.refresh(task)
    assert task.title == "New task"
    assert task.description == "New description"
    assert task.priority == PriorityEnum.HIGH


@pytest.mark.asyncio
async def test_integration_update_nonexistent_task(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Try to update non-existent task →
    AI should return error message about task not found.
    """
    from uuid import uuid4

    fake_task_id = str(uuid4())

    # Try to update non-existent task
    chat_payload = {"message": f"Update task {fake_task_id} to 'New title'"}

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
async def test_integration_update_task_natural_language(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: Use natural language to update task.
    AI should understand intent and extract the new values.
    """
    # Create a task
    task = Task(
        user_id=test_user_id,
        title="Call client",
        priority=PriorityEnum.LOW,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Use natural language
    chat_payload = {
        "message": f"Change task {task_id} to call important client instead, "
        f"and make it high priority"
    }

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # Verify success
    assert response.status_code == 200

    # Verify updates (AI should extract "call important client" as new title)
    await session.refresh(task)
    # Note: The exact title depends on AI interpretation, but priority should update
    assert task.priority == PriorityEnum.HIGH


@pytest.mark.asyncio
async def test_integration_ambiguous_reference_clarification(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """
    Integration test: User provides ambiguous reference →
    AI asks for clarification by listing matching tasks with IDs.

    Note: This tests the AI's conversational ability to handle ambiguity,
    not automatic task search (which is not implemented in T084).
    """
    # Create 3 tasks with "meeting" in title
    tasks = []
    for i in range(3):
        task = Task(
            user_id=test_user_id,
            title=f"Meeting with client {i + 1}",
            priority=PriorityEnum.MEDIUM,
            is_completed=False,
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        tasks.append(task)

    # User provides ambiguous reference
    chat_payload = {"message": "Update my meeting task to reschedule for tomorrow"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    # AI should respond (exact behavior depends on AI, but it should handle gracefully)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

    # In a real scenario, AI would:
    # 1. List the 3 tasks with their IDs
    # 2. Ask user to specify which one
    # 3. User replies with specific task ID
    # 4. AI calls update_task with that ID

    # For this test, we just verify the AI responded without crashing
    assert len(data["response"]) > 0
