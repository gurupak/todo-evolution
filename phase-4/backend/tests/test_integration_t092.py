"""
Integration tests for Phase 8 - User Story 6: Delete Tasks via Chat (T089, T092).

This test suite verifies the end-to-end flow of deleting tasks through the chat interface.
"""

import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.models.task import PriorityEnum, Task


@pytest.mark.asyncio
async def test_full_integration_delete_task_via_chat(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    test_jwt_token: str,
):
    """
    Integration test: Create task 'Meeting with Bob' →
    Chat 'Delete task {id}' →
    Verify task deleted in chat response and Phase II UI (T089, T092).
    """
    # Step 1: Create a task directly in database
    task = Task(
        user_id=test_user_id,
        title="Meeting with Bob",
        description="Quarterly review meeting",
        priority=PriorityEnum.HIGH,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Step 2: Send chat message to delete the task
    chat_payload = {"message": f"Delete task {task_id}"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    # Step 3: Verify chat response indicates success
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "response" in data

    response_text = data["response"].lower()

    # Verify deletion is mentioned in response
    assert any(
        keyword in response_text for keyword in ["delete", "removed", "cancelled", "gone"]
    ), f"Expected deletion confirmation in response: {response_text}"

    # Step 4: Verify task is deleted from database (Phase II UI would NOT see this task)
    statement = select(Task).where(Task.id == task.id)
    result = await session.execute(statement)
    deleted_task = result.scalar_one_or_none()

    assert deleted_task is None, "Task should be deleted from database"


@pytest.mark.asyncio
async def test_integration_delete_task_by_description(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    test_jwt_token: str,
):
    """
    Integration test: Create task →
    Chat 'Remove my meeting task' (reference by description) →
    AI should ask for clarification or use task ID.
    """
    # Create a task
    task = Task(
        user_id=test_user_id,
        title="Team meeting",
        description="Weekly standup",
        priority=PriorityEnum.MEDIUM,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Try to delete by description (AI should handle this)
    chat_payload = {"message": "Delete my team meeting task"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    # AI should respond (exact behavior depends on AI, but it should handle gracefully)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

    # In a real scenario, AI would either:
    # 1. Ask user to provide task ID
    # 2. List matching tasks and ask for confirmation
    # 3. Delete if only one match found

    # For this test, we just verify the AI responded without crashing
    assert len(data["response"]) > 0


@pytest.mark.asyncio
async def test_integration_delete_nonexistent_task(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    test_jwt_token: str,
):
    """
    Integration test: Try to delete non-existent task →
    AI should return error message about task not found (T088).
    """
    from uuid import uuid4

    fake_task_id = str(uuid4())

    # Try to delete non-existent task
    chat_payload = {"message": f"Delete task {fake_task_id}"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    # Should still return 200 (chat succeeded, but tool reported error)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

    response_text = data["response"].lower()

    # AI should communicate the error to user
    assert any(
        keyword in response_text
        for keyword in ["not found", "doesn't exist", "couldn't find", "unable", "no task"]
    ), f"Expected error message in response: {response_text}"


@pytest.mark.asyncio
async def test_integration_delete_other_users_task(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    test_jwt_token: str,
):
    """
    Integration test: Create task for user A, try to delete as user A using another user's ID →
    Should fail with access denied.
    """
    from uuid import uuid4

    # Create task for different user
    other_user_id = str(uuid4())
    task = Task(
        user_id=other_user_id,
        title="Other user's task",
        priority=PriorityEnum.LOW,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Try to delete it as test_user_id
    chat_payload = {"message": f"Delete task {task_id}"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    # Should still return 200 (chat succeeded, but tool reported error)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

    response_text = data["response"].lower()

    # AI should communicate the error to user
    assert any(
        keyword in response_text
        for keyword in ["not found", "access denied", "couldn't find", "unable"]
    )

    # Verify task still exists (not deleted)
    statement = select(Task).where(Task.id == task.id)
    result = await session.execute(statement)
    still_exists = result.scalar_one_or_none()

    assert still_exists is not None, "Task should still exist after failed delete"


@pytest.mark.asyncio
async def test_integration_delete_completed_task(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    test_jwt_token: str,
):
    """
    Integration test: Delete a completed task →
    Should succeed (completed tasks can be deleted).
    """
    # Create a completed task
    task = Task(
        user_id=test_user_id,
        title="Completed task",
        description="Already done",
        priority=PriorityEnum.LOW,
        is_completed=True,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)

    # Delete the completed task
    chat_payload = {"message": f"Delete task {task_id}"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    # Verify success
    assert response.status_code == 200

    # Verify task is deleted from database
    statement = select(Task).where(Task.id == task.id)
    result = await session.execute(statement)
    deleted_task = result.scalar_one_or_none()

    assert deleted_task is None


@pytest.mark.asyncio
async def test_integration_delete_confirmation_message(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    test_jwt_token: str,
):
    """
    Integration test: Verify AI provides clear confirmation message after deletion (T088).
    """
    # Create a task
    task = Task(
        user_id=test_user_id,
        title="Task to remove",
        priority=PriorityEnum.MEDIUM,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = str(task.id)
    task_title = task.title

    # Delete the task
    chat_payload = {"message": f"Remove task {task_id}"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    response_text = data["response"].lower()

    # Verify confirmation message includes deletion confirmation
    assert any(keyword in response_text for keyword in ["deleted", "removed", "cancelled", "gone"])

    # Optional: Check if task title is mentioned in confirmation
    # (AI should provide context about what was deleted)
    # This is a nice-to-have, not strictly required
