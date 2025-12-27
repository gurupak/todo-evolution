"""
Security tests for Phase 10 - User Story 8: Multi-User Conversation Isolation (T103-T106).

This test suite verifies that user data isolation is properly enforced across all endpoints and tools.
CRITICAL SECURITY REQUIREMENT: Users must NEVER be able to access other users' data.
"""

from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.models import Conversation, Message, Task
from todo_api.models.enums import PriorityEnum

# ============================================================================
# T103: User A cannot access User B's conversations
# ============================================================================


class TestConversationIsolation:
    """Test suite for conversation isolation between users (T103, T106)."""

    @pytest.mark.asyncio
    async def test_user_cannot_list_other_users_conversations(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /conversations only returns own conversations, not other users' (T103).

        Security requirement: User A must NOT see User B's conversations in list.
        """
        # Arrange - Create conversations for two different users
        user_a_id = test_user_id
        user_b_id = str(uuid4())

        # User A's conversations
        conv_a1 = Conversation(user_id=user_a_id)
        conv_a2 = Conversation(user_id=user_a_id)

        # User B's conversations (should NOT be visible to User A)
        conv_b1 = Conversation(user_id=user_b_id)
        conv_b2 = Conversation(user_id=user_b_id)

        session.add_all([conv_a1, conv_a2, conv_b1, conv_b2])
        await session.commit()

        # Act - User A requests their conversation list
        response = await client.get(
            f"/api/{user_a_id}/conversations",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert - User A only sees their own conversations
        assert response.status_code == 200
        data = response.json()
        conversations = data["conversations"]

        assert len(conversations) == 2, "User A should only see their 2 conversations"

        conversation_ids = {conv["id"] for conv in conversations}
        assert str(conv_a1.id) in conversation_ids
        assert str(conv_a2.id) in conversation_ids
        assert str(conv_b1.id) not in conversation_ids, (
            "SECURITY VIOLATION: User A can see User B's conversation!"
        )
        assert str(conv_b2.id) not in conversation_ids, (
            "SECURITY VIOLATION: User A can see User B's conversation!"
        )

    @pytest.mark.asyncio
    async def test_user_cannot_access_other_users_conversation_by_id(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /conversations/{id} returns 404 for other user's conversation (T106).

        Security requirement: User A must NOT access User B's conversation even with direct URL.
        Returns 404 (not 403) to avoid leaking existence.
        """
        # Arrange - Create conversation for User B
        user_b_id = str(uuid4())
        user_b_conversation = Conversation(user_id=user_b_id)
        session.add(user_b_conversation)
        await session.commit()
        await session.refresh(user_b_conversation)

        # Act - User A tries to access User B's conversation
        response = await client.get(
            f"/api/{test_user_id}/conversations/{user_b_conversation.id}",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert - Request is denied (404 to avoid leaking existence)
        assert response.status_code == 404
        assert "error" in response.json()

    @pytest.mark.asyncio
    async def test_user_cannot_send_message_in_other_users_conversation(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test POST /chat with other user's conversation_id is rejected (T106).

        Security requirement: User A must NOT be able to add messages to User B's conversation.
        """
        # Arrange - Create conversation for User B
        user_b_id = str(uuid4())
        user_b_conversation = Conversation(user_id=user_b_id)
        session.add(user_b_conversation)
        await session.commit()
        await session.refresh(user_b_conversation)

        # Act - User A tries to send message in User B's conversation
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json={
                "conversation_id": str(user_b_conversation.id),
                "message": "Trying to hijack conversation",
            },
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert - Request is denied
        assert response.status_code == 404
        assert "error" in response.json()

        # Verify no messages were added to User B's conversation
        statement = select(Message).where(Message.conversation_id == user_b_conversation.id)
        result = await session.execute(statement)
        messages = result.scalars().all()
        assert len(messages) == 0, (
            "SECURITY VIOLATION: Message was added to other user's conversation!"
        )


# ============================================================================
# T104: MCP tools filter by user_id
# ============================================================================


class TestMCPToolsIsolation:
    """Test suite for MCP tools user isolation (T104)."""

    @pytest.mark.asyncio
    async def test_list_tasks_only_returns_own_tasks(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test that list_tasks MCP tool only returns current user's tasks.

        Security requirement: User A's tasks must NOT appear in User B's task list.
        """
        # Arrange - Create tasks for two different users
        user_a_id = test_user_id
        user_b_id = str(uuid4())

        task_a = Task(
            user_id=user_a_id,
            title="User A's task",
            priority=PriorityEnum.HIGH,
            is_completed=False,
        )
        task_b = Task(
            user_id=user_b_id,
            title="User B's task (should not be visible)",
            priority=PriorityEnum.HIGH,
            is_completed=False,
        )

        session.add_all([task_a, task_b])
        await session.commit()

        # Act - User A asks AI to list tasks
        response = await client.post(
            f"/api/{user_a_id}/chat",
            json={"message": "Show me all my tasks"},
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert - Response should only mention User A's task
        assert response.status_code == 200
        data = response.json()
        response_text = data["response"].lower()

        # User A's task should be in response
        assert "user a" in response_text or "task" in response_text

        # User B's task should NOT be in response
        assert "user b" not in response_text, "SECURITY VIOLATION: Other user's task visible!"

    @pytest.mark.asyncio
    async def test_complete_task_only_affects_own_tasks(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test that complete_task tool cannot complete other user's tasks.

        Security requirement: User A must NOT be able to complete User B's tasks.
        """
        # Arrange - Create task for User B
        user_b_id = str(uuid4())
        task_b = Task(
            user_id=user_b_id,
            title="User B's private task",
            priority=PriorityEnum.MEDIUM,
            is_completed=False,
        )
        session.add(task_b)
        await session.commit()
        await session.refresh(task_b)

        # Act - User A tries to complete User B's task
        response = await client.post(
            f"/api/{user_a_id}/chat",
            json={"message": f"Mark task {task_b.id} as complete"},
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert - AI should return error (task not found)
        assert response.status_code == 200
        data = response.json()
        response_text = data["response"].lower()
        assert any(
            keyword in response_text
            for keyword in ["not found", "couldn't find", "unable", "doesn't exist"]
        )

        # Verify User B's task is still incomplete
        await session.refresh(task_b)
        assert task_b.is_completed is False, "SECURITY VIOLATION: Other user's task was modified!"

    @pytest.mark.asyncio
    async def test_delete_task_only_affects_own_tasks(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test that delete_task tool cannot delete other user's tasks.

        Security requirement: User A must NOT be able to delete User B's tasks.
        """
        # Arrange - Create task for User B
        user_b_id = str(uuid4())
        task_b = Task(
            user_id=user_b_id,
            title="User B's important task",
            priority=PriorityEnum.HIGH,
            is_completed=False,
        )
        session.add(task_b)
        await session.commit()
        await session.refresh(task_b)
        task_b_id = task_b.id

        # Act - User A tries to delete User B's task
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json={"message": f"Delete task {task_b.id}"},
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert - AI should return error (task not found)
        assert response.status_code == 200

        # Verify User B's task still exists
        statement = select(Task).where(Task.id == task_b_id)
        result = await session.execute(statement)
        still_exists = result.scalar_one_or_none()
        assert still_exists is not None, "SECURITY VIOLATION: Other user's task was deleted!"


# ============================================================================
# T105: JWT user_id mismatch returns 403
# ============================================================================


class TestJWTValidation:
    """Test suite for JWT user_id validation (T105)."""

    @pytest.mark.asyncio
    async def test_jwt_user_id_mismatch_returns_403(
        self,
        client: AsyncClient,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test that accessing endpoint with mismatched user_id returns 403.

        Security requirement: JWT user_id must match path user_id parameter.
        """
        # Arrange - Different user_id in path than in JWT
        different_user_id = str(uuid4())

        # Act - Try to access endpoint with mismatched user_id
        response = await client.post(
            f"/api/{different_user_id}/chat",
            json={"message": "Hello"},
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert - Request is forbidden
        assert response.status_code == 403
        assert "error" in response.json()

    @pytest.mark.asyncio
    async def test_missing_jwt_returns_401(
        self,
        client: AsyncClient,
        test_user_id: str,
    ):
        """Test that requests without JWT token return 401.

        Security requirement: All endpoints must require authentication.
        """
        # Act - Request without Authorization header
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json={"message": "Hello"},
            # No Authorization header
        )

        # Assert - Request is unauthorized
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_invalid_jwt_returns_401(
        self,
        client: AsyncClient,
        test_user_id: str,
    ):
        """Test that requests with invalid JWT return 401.

        Security requirement: Invalid tokens must be rejected.
        """
        # Act - Request with invalid JWT
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json={"message": "Hello"},
            headers={"Authorization": "Bearer invalid.jwt.token"},
        )

        # Assert - Request is unauthorized
        assert response.status_code == 401
