"""
Integration tests for Phase 9 - User Story 7: Resume Previous Conversations (T102).

This test suite verifies the end-to-end flow of resuming conversations.
"""

import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.models import Conversation, Message


@pytest.mark.asyncio
async def test_full_integration_resume_conversation(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    test_jwt_token: str,
):
    """
    Integration test: Create conversation with 10 messages →
    Reload page → Verify all messages present (T102).

    This simulates:
    1. User has a conversation with AI
    2. User closes browser/tab
    3. User returns and loads conversation list
    4. User clicks on conversation to resume
    5. All message history is loaded correctly
    """
    # Step 1: Create a conversation with 10 messages
    conversation = Conversation(user_id=test_user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    conversation_id = str(conversation.id)

    messages = []
    for i in range(10):
        msg = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Test message {i}",
        )
        session.add(msg)
        messages.append(msg)

    await session.commit()

    # Step 2: Simulate page reload - Get conversation list
    list_response = await client.get(
        f"/api/{test_user_id}/conversations",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert list_response.status_code == 200
    conversations = list_response.json()["conversations"]
    assert len(conversations) >= 1

    # Find our conversation in the list
    our_conversation = None
    for conv in conversations:
        if conv["id"] == conversation_id:
            our_conversation = conv
            break

    assert our_conversation is not None, "Conversation should appear in list"

    # Step 3: Load the specific conversation to resume it
    detail_response = await client.get(
        f"/api/{test_user_id}/conversations/{conversation_id}",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert detail_response.status_code == 200
    conversation_data = detail_response.json()

    # Step 4: Verify all 10 messages are present
    assert "messages" in conversation_data
    assert len(conversation_data["messages"]) == 10

    # Verify messages are in correct order and have correct content
    for i, msg_data in enumerate(conversation_data["messages"]):
        assert msg_data["content"] == f"Test message {i}"
        expected_role = "user" if i % 2 == 0 else "assistant"
        assert msg_data["role"] == expected_role

    # Step 5: Verify we can continue the conversation
    continue_response = await client.post(
        f"/api/{test_user_id}/chat",
        json={"conversation_id": conversation_id, "message": "Continuing the conversation"},
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert continue_response.status_code == 200
    continued_data = continue_response.json()
    assert continued_data["conversation_id"] == conversation_id
    assert "response" in continued_data


@pytest.mark.asyncio
async def test_integration_conversation_history_pagination(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    test_jwt_token: str,
):
    """
    Integration test: Create conversation with many messages →
    Load messages with pagination (load more functionality).
    """
    # Create conversation with 50 messages
    conversation = Conversation(user_id=test_user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)

    for i in range(50):
        msg = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Message {i}",
        )
        session.add(msg)

    await session.commit()

    # Load first 20 messages
    response1 = await client.get(
        f"/api/{test_user_id}/conversations/{conversation.id}?limit=20",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response1.status_code == 200
    data1 = response1.json()
    assert len(data1["messages"]) == 20
    assert data1["messages"][0]["content"] == "Message 0"

    # Load next 20 messages
    response2 = await client.get(
        f"/api/{test_user_id}/conversations/{conversation.id}?limit=20&offset=20",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response2.status_code == 200
    data2 = response2.json()
    assert len(data2["messages"]) == 20
    assert data2["messages"][0]["content"] == "Message 20"

    # Load remaining messages
    response3 = await client.get(
        f"/api/{test_user_id}/conversations/{conversation.id}?limit=20&offset=40",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response3.status_code == 200
    data3 = response3.json()
    assert len(data3["messages"]) == 10  # Only 10 remaining
    assert data3["messages"][0]["content"] == "Message 40"


@pytest.mark.asyncio
async def test_integration_multiple_conversations_isolation(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    test_jwt_token: str,
):
    """
    Integration test: Create multiple conversations →
    Verify each conversation maintains separate history.
    """
    # Create 3 different conversations with different messages
    conversations_data = []

    for conv_num in range(3):
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Add unique messages to each conversation
        for msg_num in range(5):
            msg = Message(
                conversation_id=conversation.id,
                user_id=test_user_id,
                role="user" if msg_num % 2 == 0 else "assistant",
                content=f"Conv{conv_num} Message{msg_num}",
            )
            session.add(msg)

        await session.commit()
        conversations_data.append(conversation)

    # Verify each conversation has its own messages
    for conv_num, conversation in enumerate(conversations_data):
        response = await client.get(
            f"/api/{test_user_id}/conversations/{conversation.id}",
            headers={"Authorization": f"Bearer {test_jwt_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["messages"]) == 5

        # Verify messages belong to this specific conversation
        for msg_num, msg_data in enumerate(data["messages"]):
            expected_content = f"Conv{conv_num} Message{msg_num}"
            assert msg_data["content"] == expected_content


@pytest.mark.asyncio
async def test_integration_conversation_list_order(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    test_jwt_token: str,
):
    """
    Integration test: Create conversations at different times →
    Verify list shows most recently updated first.
    """
    from datetime import datetime, timedelta, timezone

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Create 3 conversations with different update times
    old_conv = Conversation(user_id=test_user_id)
    old_conv.updated_at = now - timedelta(days=3)

    mid_conv = Conversation(user_id=test_user_id)
    mid_conv.updated_at = now - timedelta(days=1)

    new_conv = Conversation(user_id=test_user_id)
    new_conv.updated_at = now

    session.add_all([old_conv, mid_conv, new_conv])
    await session.commit()
    await session.refresh(old_conv)
    await session.refresh(mid_conv)
    await session.refresh(new_conv)

    # Get conversation list
    response = await client.get(
        f"/api/{test_user_id}/conversations",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 200
    conversations = response.json()["conversations"]

    # Verify order: newest first
    assert conversations[0]["id"] == str(new_conv.id)
    assert conversations[1]["id"] == str(mid_conv.id)
    assert conversations[2]["id"] == str(old_conv.id)
