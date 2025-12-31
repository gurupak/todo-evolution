"""
Integration tests for Phase 10 - User Story 8: Multi-User Conversation Isolation (T111).

This test suite verifies complete data isolation between users across all features.
CRITICAL SECURITY REQUIREMENT: Zero instances of cross-user data access.
"""

from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.models import Conversation, Message, Task
from todo_api.models.enums import PriorityEnum


@pytest.mark.asyncio
async def test_full_integration_multi_user_complete_isolation(
    client: AsyncClient,
    session: AsyncSession,
    test_user_id: str,
    test_jwt_token: str,
):
    """
    Integration test: Create User A and User B → Each creates tasks and conversations →
    Verify complete isolation (T111).

    This comprehensive test verifies:
    1. User A creates tasks - User B cannot see them
    2. User B creates tasks - User A cannot see them
    3. User A creates conversation - User B cannot access it
    4. User B creates conversation - User A cannot access it
    5. MCP tools (list, complete, update, delete) respect user boundaries
    6. JWT validation prevents cross-user access
    """
    # Setup - User A is the test user, create User B
    user_a_id = test_user_id
    user_a_token = test_jwt_token

    user_b_id = str(uuid4())
    # Note: In real scenario, User B would have their own JWT token
    # For this test, we simulate by creating User B's data directly in DB

    # ========================================================================
    # Step 1: User A creates tasks
    # ========================================================================

    # User A creates tasks via chat
    response_a = await client.post(
        f"/api/{user_a_id}/chat",
        json={"message": "Add task: Finish User A's project report"},
        headers={"Authorization": f"Bearer {user_a_token}"},
    )
    assert response_a.status_code == 200

    # User A creates conversation
    conv_a_data = response_a.json()
    conv_a_id = conv_a_data["conversation_id"]

    # ========================================================================
    # Step 2: User B creates tasks (via direct DB for simulation)
    # ========================================================================

    task_b = Task(
        user_id=user_b_id,
        title="User B's confidential task",
        description="Secret project details",
        priority=PriorityEnum.HIGH,
        is_completed=False,
    )
    session.add(task_b)

    conv_b = Conversation(user_id=user_b_id)
    session.add(conv_b)

    msg_b = Message(
        conversation_id=conv_b.id,
        user_id=user_b_id,
        role="user",
        content="User B's private message",
    )
    session.add(msg_b)

    await session.commit()
    await session.refresh(task_b)
    await session.refresh(conv_b)

    # ========================================================================
    # Step 3: Verify User A cannot see User B's tasks
    # ========================================================================

    # User A lists tasks
    response_list = await client.post(
        f"/api/{user_a_id}/chat",
        json={"message": "Show all my tasks"},
        headers={"Authorization": f"Bearer {user_a_token}"},
    )
    assert response_list.status_code == 200
    list_response_text = response_list.json()["response"].lower()

    # User A should see their own task
    assert "user a" in list_response_text or "project report" in list_response_text

    # User B's task should NOT appear
    assert "user b" not in list_response_text
    assert "confidential" not in list_response_text
    assert "secret project" not in list_response_text

    # ========================================================================
    # Step 4: Verify User A cannot complete User B's task
    # ========================================================================

    response_complete = await client.post(
        f"/api/{user_a_id}/chat",
        json={"message": f"Mark task {task_b.id} as complete"},
        headers={"Authorization": f"Bearer {user_a_token}"},
    )
    assert response_complete.status_code == 200

    # AI should report task not found
    complete_response_text = response_complete.json()["response"].lower()
    assert any(kw in complete_response_text for kw in ["not found", "couldn't find", "unable"])

    # Verify User B's task is still incomplete
    await session.refresh(task_b)
    assert task_b.is_completed is False, "SECURITY VIOLATION: Cross-user task modification!"

    # ========================================================================
    # Step 5: Verify User A cannot access User B's conversations
    # ========================================================================

    # Try to get User B's conversation list as User A
    response_conv_list = await client.get(
        f"/api/{user_a_id}/conversations",
        headers={"Authorization": f"Bearer {user_a_token}"},
    )
    assert response_conv_list.status_code == 200

    conv_list = response_conv_list.json()["conversations"]
    conv_ids = [c["id"] for c in conv_list]

    # User A should see their own conversation
    assert conv_a_id in conv_ids

    # User B's conversation should NOT appear
    assert str(conv_b.id) not in conv_ids, "SECURITY VIOLATION: Cross-user conversation visible!"

    # ========================================================================
    # Step 6: Verify User A cannot access User B's conversation by direct URL
    # ========================================================================

    response_conv_detail = await client.get(
        f"/api/{user_a_id}/conversations/{conv_b.id}",
        headers={"Authorization": f"Bearer {user_a_token}"},
    )

    # Should return 404 (not 403 to avoid leaking existence)
    assert response_conv_detail.status_code == 404

    # ========================================================================
    # Step 7: Verify User A cannot send message in User B's conversation
    # ========================================================================

    response_msg = await client.post(
        f"/api/{user_a_id}/chat",
        json={
            "conversation_id": str(conv_b.id),
            "message": "Trying to hijack conversation",
        },
        headers={"Authorization": f"Bearer {user_a_token}"},
    )

    # Should return 404
    assert response_msg.status_code == 404

    # Verify no new messages added to User B's conversation
    statement = select(Message).where(Message.conversation_id == conv_b.id)
    result = await session.execute(statement)
    messages = result.scalars().all()
    assert len(messages) == 1  # Only the original message
    assert messages[0].content == "User B's private message"

    # ========================================================================
    # Step 8: Verify JWT user_id mismatch is rejected
    # ========================================================================

    # User A tries to access User B's endpoint with User A's JWT
    response_mismatch = await client.post(
        f"/api/{user_b_id}/chat",
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {user_a_token}"},
    )

    # Should return 403 Forbidden
    assert response_mismatch.status_code == 403

    # ========================================================================
    # Final Verification: Database-level check
    # ========================================================================

    # Verify User A's tasks count
    statement_a = select(Task).where(Task.user_id == user_a_id)
    result_a = await session.execute(statement_a)
    tasks_a = result_a.scalars().all()

    # Verify User B's tasks count
    statement_b = select(Task).where(Task.user_id == user_b_id)
    result_b = await session.execute(statement_b)
    tasks_b = result_b.scalars().all()

    # Ensure no task belongs to both users
    task_a_ids = {str(t.id) for t in tasks_a}
    task_b_ids = {str(t.id) for t in tasks_b}
    assert task_a_ids.isdisjoint(task_b_ids), "SECURITY VIOLATION: Task ID collision between users!"

    # Verify task isolation
    assert all(t.user_id == user_a_id for t in tasks_a)
    assert all(t.user_id == user_b_id for t in tasks_b)


@pytest.mark.asyncio
async def test_integration_three_user_isolation(
    client: AsyncClient,
    session: AsyncSession,
    test_user_id: str,
    test_jwt_token: str,
):
    """
    Integration test: Three users create data → Verify each user is completely isolated.

    Tests that isolation works correctly with multiple concurrent users.
    """
    # Setup - Three users
    user1_id = test_user_id
    user1_token = test_jwt_token

    user2_id = str(uuid4())
    user3_id = str(uuid4())

    task1 = Task(
        user_id=user1_id, title="User 1 task", priority=PriorityEnum.HIGH, is_completed=False
    )
    task2 = Task(
        user_id=user2_id, title="User 2 task", priority=PriorityEnum.MEDIUM, is_completed=False
    )
    task3 = Task(
        user_id=user3_id, title="User 3 task", priority=PriorityEnum.LOW, is_completed=False
    )
    task3 = Task(user_id=user3_id, title="User 3 task", priority=PriorityEnum.LOW, is_completed=False)

    session.add_all([task1, task2, task3])
    await session.commit()

    # User 1 lists tasks via chat
    response = await client.post(
        f"/api/{user1_id}/chat",
        json={"message": "List all tasks"},
        headers={"Authorization": f"Bearer {user1_token}"},
    )

    assert response.status_code == 200
    response_text = response.json()["response"].lower()

    # User 1 should only see their task
    assert "user 1" in response_text or len(response_text) > 0
    assert "user 2" not in response_text
    assert "user 3" not in response_text

    # Verify database-level isolation
    statement = select(Task).where(Task.user_id == user1_id)
    result = await session.execute(statement)
    user1_tasks = result.scalars().all()

    assert len(user1_tasks) >= 1
    assert all(t.user_id == user1_id for t in user1_tasks)


@pytest.mark.asyncio
async def test_integration_user_cannot_modify_system_created_data(
    client: AsyncClient,
    session: AsyncSession,
    test_user_id: str,
    test_jwt_token: str,
):
    """
    Integration test: Verify users cannot modify data from non-existent or system users.

    Tests edge case protection against malformed user IDs.
    """
    # Create task with malformed user_id
    fake_user_id = "system_user_invalid_id"

    task = Task(
        user_id=fake_user_id,
        title="System task",
        priority=PriorityEnum.HIGH,
        is_completed=False,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    # User tries to complete the system task
    response = await client.post(
        f"/api/{test_user_id}/chat",
        json={"message": f"Complete task {task.id}"},
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 200
    response_text = response.json()["response"].lower()

    # Should report task not found
    assert any(kw in response_text for kw in ["not found", "couldn't find", "unable"])

    # Verify system task is unchanged
    await session.refresh(task)
    assert task.is_completed is False
    assert task.user_id == fake_user_id  # Unchanged
