"""Tests for Conversation and Message models."""

from datetime import datetime
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from todo_api.models import Conversation, Message


class TestConversationModel:
    """Tests for Conversation model creation and validation."""

    @pytest.mark.asyncio
    async def test_conversation_model_creation(self, session: AsyncSession, test_user_id: str):
        """Test creating a Conversation model with valid data.

        Verifies:
        - Conversation can be created with user_id
        - ID is auto-generated as UUID
        - created_at and updated_at are auto-set
        - Model can be saved to database
        """
        # Arrange & Act
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Assert
        assert conversation.id is not None
        assert isinstance(conversation.id, UUID)
        assert conversation.user_id == test_user_id
        assert isinstance(conversation.created_at, datetime)
        assert isinstance(conversation.updated_at, datetime)
        assert conversation.created_at <= conversation.updated_at

    @pytest.mark.asyncio
    async def test_conversation_requires_user_id(self, session: AsyncSession):
        """Test that Conversation requires user_id (cannot be None).

        Verifies:
        - user_id is a required field
        - Creating conversation without user_id raises validation error
        """
        # Arrange & Act & Assert
        with pytest.raises(Exception):  # ValidationError or IntegrityError
            conversation = Conversation()
            session.add(conversation)
            await session.commit()

    @pytest.mark.asyncio
    async def test_conversation_timestamps_default(self, session: AsyncSession, test_user_id: str):
        """Test that created_at and updated_at have default values.

        Verifies:
        - Timestamps are automatically set when not provided
        - Both timestamps are set to current time
        """
        # Arrange & Act
        before = datetime.utcnow()
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        after = datetime.utcnow()

        # Assert
        assert before <= conversation.created_at <= after
        assert before <= conversation.updated_at <= after


class TestMessageModel:
    """Tests for Message model creation with user/assistant roles."""

    @pytest.mark.asyncio
    async def test_message_model_with_user_role(self, session: AsyncSession, test_user_id: str):
        """Test creating a Message with role='user'.

        Verifies:
        - Message can be created with user role
        - All required fields are set correctly
        - tool_calls is None for user messages
        """
        # Arrange
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Act
        message = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="user",
            content="Add task to buy groceries",
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)

        # Assert
        assert message.id is not None
        assert isinstance(message.id, UUID)
        assert message.conversation_id == conversation.id
        assert message.user_id == test_user_id
        assert message.role == "user"
        assert message.content == "Add task to buy groceries"
        assert message.tool_calls is None
        assert isinstance(message.created_at, datetime)

    @pytest.mark.asyncio
    async def test_message_model_with_assistant_role(
        self, session: AsyncSession, test_user_id: str
    ):
        """Test creating a Message with role='assistant' and tool_calls.

        Verifies:
        - Message can be created with assistant role
        - tool_calls can contain JSON data
        - All fields are persisted correctly
        """
        # Arrange
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        tool_calls_data = [
            {
                "tool": "add_task",
                "arguments": {"user_id": test_user_id, "title": "Buy groceries"},
                "result": {"success": True, "task_id": "task-123"},
            }
        ]

        # Act
        message = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="assistant",
            content="I've added the task 'Buy groceries' to your list.",
            tool_calls=tool_calls_data,
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)

        # Assert
        assert message.role == "assistant"
        assert message.content == "I've added the task 'Buy groceries' to your list."
        assert message.tool_calls is not None
        assert isinstance(message.tool_calls, list)
        assert len(message.tool_calls) == 1
        assert message.tool_calls[0]["tool"] == "add_task"

    @pytest.mark.asyncio
    async def test_message_requires_all_fields(self, session: AsyncSession, test_user_id: str):
        """Test that Message requires conversation_id, user_id, role, and content.

        Verifies:
        - All required fields must be provided
        - Missing fields raise validation errors
        """
        # Arrange
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Act & Assert - missing content
        with pytest.raises(Exception):
            message = Message(conversation_id=conversation.id, user_id=test_user_id, role="user")
            session.add(message)
            await session.commit()

    @pytest.mark.asyncio
    async def test_message_content_not_empty(self, session: AsyncSession, test_user_id: str):
        """Test that Message content cannot be empty string.

        Verifies:
        - Database CHECK constraint enforces non-empty content
        - Empty content raises IntegrityError
        """
        # Arrange
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Act & Assert
        with pytest.raises(Exception):  # IntegrityError from CHECK constraint
            message = Message(
                conversation_id=conversation.id,
                user_id=test_user_id,
                role="user",
                content="",  # Empty string should fail
            )
            session.add(message)
            await session.commit()

    @pytest.mark.asyncio
    async def test_message_created_at_default(self, session: AsyncSession, test_user_id: str):
        """Test that created_at has default value.

        Verifies:
        - created_at is automatically set when not provided
        - Timestamp is set to current time
        """
        # Arrange
        conversation = Conversation(user_id=test_user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Act
        before = datetime.utcnow()
        message = Message(
            conversation_id=conversation.id,
            user_id=test_user_id,
            role="user",
            content="Test message",
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)
        after = datetime.utcnow()

        # Assert
        assert before <= message.created_at <= after
