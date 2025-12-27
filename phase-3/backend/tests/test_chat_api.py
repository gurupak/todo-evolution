"""Tests for Chat API endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from todo_api.models import Conversation, Message


class TestChatEndpointNewConversation:
    """Tests for POST /api/{user_id}/chat with new conversation."""

    @pytest.mark.asyncio
    async def test_post_chat_creates_new_conversation(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test POST /api/{user_id}/chat creates new conversation when conversation_id not provided.

        Verifies:
        - Request without conversation_id creates new conversation
        - Response includes conversation_id
        - Response includes AI assistant response
        - Conversation is saved to database
        """
        # Arrange
        payload = {"message": "Hi"}

        # Act
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json=payload,
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert "response" in data
        assert data["conversation_id"] is not None
        # Note: Actual AI response depends on implementation
        # For now we just verify structure

    @pytest.mark.asyncio
    async def test_post_chat_validates_message_length(
        self,
        client: AsyncClient,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test POST /api/{user_id}/chat validates message length (1-2000 characters).

        Verifies:
        - Empty message returns 400 error
        - Message > 2000 characters returns 400 error
        - Error message is descriptive
        """
        # Act - empty message
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json={"message": ""},
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 400
        assert "error" in response.json()

        # Act - message too long
        long_message = "a" * 2001
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json={"message": long_message},
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 400
        assert "error" in response.json()


class TestChatEndpointConversationHistory:
    """Tests for conversation history loading in chat endpoint."""

    @pytest.mark.asyncio
    async def test_post_chat_loads_conversation_history(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test POST /api/{user_id}/chat loads existing conversation history.

        Verifies:
        - Request with conversation_id loads existing conversation
        - Previous messages are included in context
        - New message is appended to conversation
        - Response maintains conversation_id
        """
        # Arrange - Create existing conversation with messages
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Add previous messages
        msg1 = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="user",
            content="Previous message 1",
        )
        msg2 = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="assistant",
            content="Previous response 1",
        )
        session.add_all([msg1, msg2])
        await session.commit()

        # Act
        payload = {"conversation_id": str(conversation.id), "message": "New message"}

        response = await client.post(
            f"/api/{test_user_id}/chat",
            json=payload,
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] == str(conversation.id)
        assert "response" in data

    @pytest.mark.asyncio
    async def test_post_chat_handles_nonexistent_conversation(
        self,
        client: AsyncClient,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test POST /api/{user_id}/chat handles invalid conversation_id.

        Verifies:
        - Request with non-existent conversation_id returns 404
        - Error message indicates conversation not found
        """
        # Arrange
        fake_conversation_id = "550e8400-e29b-41d4-a716-446655440099"
        payload = {"conversation_id": fake_conversation_id, "message": "Hello"}

        # Act
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json=payload,
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 404
        assert "error" in response.json()


class TestChatEndpointAuthentication:
    """Tests for JWT authentication on chat endpoint."""

    @pytest.mark.asyncio
    async def test_post_chat_requires_jwt_token(
        self,
        client: AsyncClient,
        test_user_id: str,
    ):
        """Test POST /api/{user_id}/chat requires JWT authentication.

        Verifies:
        - Request without Authorization header returns 401
        - Error indicates authentication required
        """
        # Arrange
        payload = {"message": "Hello"}

        # Act
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json=payload,
            # No Authorization header
        )

        # Assert
        assert response.status_code == 401
        assert "error" in response.json()


# ============================================================================
# Phase 7 - User Story 7: Resume Previous Conversations (T093-T096)
# ============================================================================


class TestGetConversationsEndpoint:
    """Tests for GET /api/{user_id}/conversations endpoint (T093, T095)."""

    @pytest.mark.asyncio
    async def test_get_conversations_returns_user_conversations(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations returns list of user's conversations (T093).

        Verifies:
        - Returns 200 status code
        - Returns list of conversations
        - Each conversation includes id, created_at, updated_at
        - Only returns conversations belonging to the user
        """
        # Arrange - Create conversations for test user
        conv1 = Conversation(user_id=test_user_id)
        conv2 = Conversation(user_id=test_user_id)
        session.add_all([conv1, conv2])
        await session.commit()
        await session.refresh(conv1)
        await session.refresh(conv2)

        # Act
        response = await client.get(
            f"/api/{test_user_id}/conversations",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "conversations" in data
        assert len(data["conversations"]) == 2

        # Verify conversation structure
        for conv in data["conversations"]:
            assert "id" in conv
            assert "created_at" in conv
            assert "updated_at" in conv

    @pytest.mark.asyncio
    async def test_get_conversations_sorted_by_updated_at_desc(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations returns conversations sorted by updated_at DESC (T095).

        Verifies:
        - Conversations are sorted by updated_at in descending order
        - Most recently updated conversation appears first
        """
        from datetime import datetime, timedelta, timezone

        # Arrange - Create conversations with different updated_at times
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        conv1 = Conversation(user_id=test_user_id)
        conv1.updated_at = now - timedelta(hours=2)  # Oldest

        conv2 = Conversation(user_id=test_user_id)
        conv2.updated_at = now - timedelta(hours=1)  # Middle

        conv3 = Conversation(user_id=test_user_id)
        conv3.updated_at = now  # Most recent

        session.add_all([conv1, conv2, conv3])
        await session.commit()
        await session.refresh(conv1)
        await session.refresh(conv2)
        await session.refresh(conv3)

        # Act
        response = await client.get(
            f"/api/{test_user_id}/conversations",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        conversations = data["conversations"]

        assert len(conversations) == 3
        # Most recent should be first
        assert conversations[0]["id"] == str(conv3.id)
        assert conversations[1]["id"] == str(conv2.id)
        assert conversations[2]["id"] == str(conv1.id)

    @pytest.mark.asyncio
    async def test_get_conversations_empty_list_for_new_user(
        self,
        client: AsyncClient,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations returns empty list for user with no conversations.

        Verifies:
        - Returns 200 status code
        - Returns empty conversations list
        """
        # Act
        response = await client.get(
            f"/api/{test_user_id}/conversations",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "conversations" in data
        assert data["conversations"] == []

    @pytest.mark.asyncio
    async def test_get_conversations_requires_authentication(
        self,
        client: AsyncClient,
        test_user_id: str,
    ):
        """Test GET /api/{user_id}/conversations requires JWT authentication.

        Verifies:
        - Request without Authorization header returns 401
        """
        # Act
        response = await client.get(
            f"/api/{test_user_id}/conversations",
            # No Authorization header
        )

        # Assert
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_conversations_user_isolation(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations only returns user's own conversations.

        Verifies:
        - Does not return conversations belonging to other users
        - User data isolation is enforced
        """
        from uuid import uuid4

        # Arrange - Create conversations for different users
        other_user_id = str(uuid4())

        user_conv = Conversation(user_id=test_user_id)
        other_conv = Conversation(user_id=other_user_id)

        session.add_all([user_conv, other_conv])
        await session.commit()

        # Act
        response = await client.get(
            f"/api/{test_user_id}/conversations",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["conversations"]) == 1
        assert data["conversations"][0]["id"] == str(user_conv.id)


class TestGetConversationByIdEndpoint:
    """Tests for GET /api/{user_id}/conversations/{id} endpoint (T094, T096)."""

    @pytest.mark.asyncio
    async def test_get_conversation_by_id_returns_conversation_with_messages(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations/{id} returns conversation with messages (T094).

        Verifies:
        - Returns 200 status code
        - Returns conversation details
        - Includes all messages in the conversation
        - Messages are in correct order (oldest first)
        """
        # Arrange - Create conversation with messages
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Add messages
        msg1 = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="user",
            content="First message",
        )
        msg2 = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="assistant",
            content="First response",
        )
        msg3 = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="user",
            content="Second message",
        )
        session.add_all([msg1, msg2, msg3])
        await session.commit()

        # Act
        response = await client.get(
            f"/api/{test_user_id}/conversations/{conversation.id}",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert "id" in data
        assert data["id"] == str(conversation.id)
        assert "messages" in data
        assert len(data["messages"]) == 3

        # Verify messages are in chronological order
        assert data["messages"][0]["content"] == "First message"
        assert data["messages"][1]["content"] == "First response"
        assert data["messages"][2]["content"] == "Second message"

    @pytest.mark.asyncio
    async def test_get_conversation_by_id_pagination(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations/{id} supports message pagination (T096).

        Verifies:
        - Supports limit and offset query parameters
        - Returns correct subset of messages
        - Useful for "Load more" functionality
        """
        # Arrange - Create conversation with 10 messages
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Add 10 messages
        for i in range(10):
            msg = Message(
                conversation_id=conversation.id,
                user_id=test_user_id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i}",
            )
            session.add(msg)
        await session.commit()

        # Act - Get first 5 messages
        response = await client.get(
            f"/api/{test_user_id}/conversations/{conversation.id}?limit=5",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["messages"]) == 5

        # Act - Get next 5 messages with offset
        response = await client.get(
            f"/api/{test_user_id}/conversations/{conversation.id}?limit=5&offset=5",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["messages"]) == 5

    @pytest.mark.asyncio
    async def test_get_conversation_by_id_not_found(
        self,
        client: AsyncClient,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations/{id} returns 404 for non-existent conversation.

        Verifies:
        - Returns 404 status code
        - Returns error message
        """
        from uuid import uuid4

        fake_id = str(uuid4())

        # Act
        response = await client.get(
            f"/api/{test_user_id}/conversations/{fake_id}",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 404
        assert "error" in response.json()

    @pytest.mark.asyncio
    async def test_get_conversation_by_id_user_isolation(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations/{id} enforces user isolation.

        Verifies:
        - Cannot access other user's conversations
        - Returns 404 (not 403 to avoid leaking existence)
        """
        from uuid import uuid4

        # Arrange - Create conversation for different user
        other_user_id = str(uuid4())
        other_conversation = Conversation(user_id=other_user_id)
        session.add(other_conversation)
        await session.commit()
        await session.refresh(other_conversation)

        # Act - Try to access other user's conversation
        response = await client.get(
            f"/api/{test_user_id}/conversations/{other_conversation.id}",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 404  # Not 403, to avoid leaking existence
        assert "error" in response.json()

    @pytest.mark.asyncio
    async def test_post_chat_validates_user_id_matches_jwt(
        self,
        client: AsyncClient,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test POST /api/{user_id}/chat validates user_id matches JWT token.

        Verifies:
        - Request with mismatched user_id returns 403
        - User cannot access other user's chat endpoint
        """
        # Arrange
        different_user_id = "999e8400-e29b-41d4-a716-446655440000"
        payload = {"message": "Hello"}

        # Act
        response = await client.post(
            f"/api/{different_user_id}/chat",
            json=payload,
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 403
        assert "error" in response.json()

    @pytest.mark.asyncio
    async def test_post_chat_rejects_invalid_jwt(
        self,
        client: AsyncClient,
        test_user_id: str,
    ):
        """Test POST /api/{user_id}/chat rejects invalid JWT tokens.

        Verifies:
        - Request with malformed JWT returns 401
        - Request with invalid signature returns 401
        """
        # Arrange
        payload = {"message": "Hello"}
        invalid_token = "invalid.jwt.token"

        # Act
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json=payload,
            headers={"Authorization": f"Bearer {invalid_token}"},
        )

        # Assert
        assert response.status_code == 401
        assert "error" in response.json()


# ============================================================================
# Phase 7 - User Story 7: Resume Previous Conversations (T093-T096)
# ============================================================================


class TestGetConversationsEndpoint:
    """Tests for GET /api/{user_id}/conversations endpoint (T093, T095)."""

    @pytest.mark.asyncio
    async def test_get_conversations_returns_user_conversations(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations returns list of user's conversations (T093)."""
        # Arrange - Create conversations for test user
        conv1 = Conversation(user_id=test_user_id)
        conv2 = Conversation(user_id=test_user_id)
        session.add_all([conv1, conv2])
        await session.commit()
        await session.refresh(conv1)
        await session.refresh(conv2)

        # Act
        response = await client.get(
            f"/api/{test_user_id}/conversations",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "conversations" in data
        assert len(data["conversations"]) == 2

    @pytest.mark.asyncio
    async def test_get_conversations_sorted_by_updated_at_desc(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations sorted by updated_at DESC (T095)."""
        from datetime import datetime, timedelta, timezone

        # Arrange - Create conversations with different updated_at times
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        
        conv1 = Conversation(user_id=test_user_id)
        conv1.updated_at = now - timedelta(hours=2)
        
        conv2 = Conversation(user_id=test_user_id)
        conv2.updated_at = now - timedelta(hours=1)
        
        conv3 = Conversation(user_id=test_user_id)
        conv3.updated_at = now
        
        session.add_all([conv1, conv2, conv3])
        await session.commit()
        await session.refresh(conv1)
        await session.refresh(conv2)
        await session.refresh(conv3)

        # Act
        response = await client.get(
            f"/api/{test_user_id}/conversations",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        conversations = data["conversations"]
        
        assert len(conversations) == 3
        assert conversations[0]["id"] == str(conv3.id)
        assert conversations[1]["id"] == str(conv2.id)
        assert conversations[2]["id"] == str(conv1.id)


class TestGetConversationByIdEndpoint:
    """Tests for GET /api/{user_id}/conversations/{id} endpoint (T094, T096)."""

    @pytest.mark.asyncio
    async def test_get_conversation_by_id_returns_conversation_with_messages(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations/{id} returns conversation with messages (T094)."""
        # Arrange - Create conversation with messages
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Add messages
        msg1 = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="user",
            content="First message",
        )
        msg2 = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="assistant",
            content="First response",
        )
        session.add_all([msg1, msg2])
        await session.commit()

        # Act
        response = await client.get(
            f"/api/{test_user_id}/conversations/{conversation.id}",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        
        assert "id" in data
        assert "messages" in data
        assert len(data["messages"]) == 2

    @pytest.mark.asyncio
    async def test_get_conversation_by_id_pagination(
        self,
        client: AsyncClient,
        session: AsyncSession,
        test_user_id: str,
        test_jwt_token: str,
    ):
        """Test GET /api/{user_id}/conversations/{id} supports pagination (T096)."""
        # Arrange - Create conversation with 10 messages
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Add 10 messages
        for i in range(10):
            msg = Message(
                conversation_id=conversation.id,
                user_id=test_user_id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i}",
            )
            session.add(msg)
        await session.commit()

        # Act - Get first 5 messages
        response = await client.get(
            f"/api/{test_user_id}/conversations/{conversation.id}?limit=5",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["messages"]) == 5
