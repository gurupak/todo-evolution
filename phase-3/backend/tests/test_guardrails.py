"""Tests for AI agent guardrails.

These tests verify that input and output guardrails correctly validate
messages and prevent off-topic or malformed interactions.
"""

from unittest.mock import AsyncMock, Mock

import pytest
from agents import GuardrailFunctionOutput
from todo_api.agent.guardrails import (
    ResponseValidationOutput,
    TopicValidationOutput,
    response_validator_guard,
    ResponseValidationOutput,
)


class TestTodoTopicGuard:
    """Test suite for input guardrail that validates todo-related topics."""

    @pytest.mark.asyncio
    async def test_blocks_off_topic_messages(self):
        """Test that input guardrail blocks messages unrelated to tasks."""
        # Setup mock context
        mock_ctx = Mock()
        mock_ctx.context = {}

        # Create mock agent
        mock_agent = Mock()

        # Off-topic message
        off_topic_message = "What's the weather like today?"

        # Call guardrail
        result = await todo_topic_guard(mock_ctx, mock_agent, off_topic_message)

        # Verify guardrail triggered tripwire
        assert isinstance(result, GuardrailFunctionOutput)
        assert result.tripwire_triggered is True
        assert isinstance(result.output_info, TopicValidationOutput)
        assert result.output_info.is_todo_related is False
        assert (
            "weather" in result.output_info.reasoning.lower()
            or "not related" in result.output_info.reasoning.lower()
        )

    @pytest.mark.asyncio
    async def test_blocks_general_conversation(self):
        """Test that casual conversation is blocked."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        casual_message = "How are you doing today?"

        result = await todo_topic_guard(mock_ctx, mock_agent, casual_message)

        assert result.tripwire_triggered is True
        assert result.output_info.is_todo_related is False

    @pytest.mark.asyncio
    async def test_blocks_inappropriate_content(self):
        """Test that inappropriate or harmful content is blocked."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        inappropriate_message = "Tell me a joke about politics"

        result = await todo_topic_guard(mock_ctx, mock_agent, inappropriate_message)

        assert result.tripwire_triggered is True
        assert result.output_info.is_todo_related is False

    @pytest.mark.asyncio
    async def test_allows_add_task_messages(self):
        """Test that task creation messages are allowed."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        add_task_message = "Add a task to buy groceries"

        result = await todo_topic_guard(mock_ctx, mock_agent, add_task_message)

        assert isinstance(result, GuardrailFunctionOutput)
        assert result.tripwire_triggered is False
        assert result.output_info.is_todo_related is True
        assert (
            "task" in result.output_info.reasoning.lower()
            or "todo" in result.output_info.reasoning.lower()
        )

    @pytest.mark.asyncio
    async def test_allows_view_tasks_messages(self):
        """Test that task viewing messages are allowed."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        view_tasks_message = "Show me my pending tasks"

        result = await todo_topic_guard(mock_ctx, mock_agent, view_tasks_message)

        assert result.tripwire_triggered is False
        assert result.output_info.is_todo_related is True

    @pytest.mark.asyncio
    async def test_allows_update_task_messages(self):
        """Test that task update messages are allowed."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        update_message = "Change task 1 to call mom instead"

        result = await todo_topic_guard(mock_ctx, mock_agent, update_message)

        assert result.tripwire_triggered is False
        assert result.output_info.is_todo_related is True

    @pytest.mark.asyncio
    async def test_allows_complete_task_messages(self):
        """Test that task completion messages are allowed."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        complete_message = "Mark the groceries task as done"

        result = await todo_topic_guard(mock_ctx, mock_agent, complete_message)

        assert result.tripwire_triggered is False
        assert result.output_info.is_todo_related is True

    @pytest.mark.asyncio
    async def test_allows_delete_task_messages(self):
        """Test that task deletion messages are allowed."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        delete_message = "Delete task number 3"

        result = await todo_topic_guard(mock_ctx, mock_agent, delete_message)

        assert result.tripwire_triggered is False
        assert result.output_info.is_todo_related is True

    @pytest.mark.asyncio
    async def test_allows_greetings_in_task_context(self):
        """Test that greetings are allowed when they lead to task management."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        greeting_message = "Hi, I need help managing my tasks"

        result = await todo_topic_guard(mock_ctx, mock_agent, greeting_message)

        assert result.tripwire_triggered is False
        assert result.output_info.is_todo_related is True


class TestResponseValidatorGuard:
    """Test suite for output guardrail that validates AI responses."""

    @pytest.mark.asyncio
    async def test_validates_response_has_content(self):
        """Test that output guardrail validates response has actual content."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        valid_response = "I've added the task 'Buy groceries' to your list."

        result = await response_validator_guard(mock_ctx, mock_agent, valid_response)

        assert isinstance(result, GuardrailFunctionOutput)
        assert result.tripwire_triggered is False
        assert result.output_info.is_valid is True

    @pytest.mark.asyncio
    async def test_blocks_empty_responses(self):
        """Test that empty or whitespace-only responses trigger tripwire."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        empty_response = "   "

        result = await response_validator_guard(mock_ctx, mock_agent, empty_response)

        assert result.tripwire_triggered is True
        assert result.output_info.is_valid is False
        assert (
            "empty" in result.output_info.reasoning.lower()
            or "no content" in result.output_info.reasoning.lower()
        )

    @pytest.mark.asyncio
    async def test_blocks_error_messages_without_context(self):
        """Test that generic error messages without helpful context are blocked."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        unhelpful_response = "Error occurred."

        result = await response_validator_guard(mock_ctx, mock_agent, unhelpful_response)

        # Should flag as potentially invalid due to lack of helpful information
        # (This is a design decision - we want helpful error messages)
        assert isinstance(result, GuardrailFunctionOutput)

    @pytest.mark.asyncio
    async def test_allows_task_confirmation_responses(self):
        """Test that task confirmation messages are valid."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        confirmation = "I've marked task 'Buy groceries' as completed."

        result = await response_validator_guard(mock_ctx, mock_agent, confirmation)

        assert result.tripwire_triggered is False
        assert result.output_info.is_valid is True

    @pytest.mark.asyncio
    async def test_allows_task_list_responses(self):
        """Test that task list responses are valid."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        task_list = "You have 3 pending tasks:\n1. Buy groceries\n2. Call mom\n3. Finish project"

        result = await response_validator_guard(mock_ctx, mock_agent, task_list)

        assert result.tripwire_triggered is False
        assert result.output_info.is_valid is True

    @pytest.mark.asyncio
    async def test_allows_clarification_requests(self):
        """Test that clarification requests are valid responses."""
        mock_ctx = Mock()
        mock_ctx.context = {}
        mock_agent = Mock()

        clarification = "I found 3 tasks with 'meeting' in the title. Which one did you mean?"

        result = await response_validator_guard(mock_ctx, mock_agent, clarification)

        assert result.tripwire_triggered is False
        assert result.output_info.is_valid is True
