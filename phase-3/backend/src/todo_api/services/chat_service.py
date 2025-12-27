"""Chat service for AI agent orchestration and conversation management.

This service handles conversation lifecycle, message persistence, agent execution,
and error handling with retry logic.
"""

import asyncio
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from agents import Runner
from agents.exceptions import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.agent.todo_agent import todo_agent
from todo_api.models import Conversation, Message


class ChatService:
    """Service for managing AI chat conversations and agent execution."""

    # Token limit for conversation history (before truncation)
    MAX_CONVERSATION_TOKENS = 8000
    # Exponential backoff configuration
    MAX_RETRIES = 3
    INITIAL_RETRY_DELAY = 1.0  # seconds
    MAX_RETRY_DELAY = 10.0  # seconds

    def __init__(self, session: AsyncSession, user_id: str):
        """Initialize chat service.

        Args:
            session: Database session for persistence
            user_id: Current user's ID for data isolation
        """
        self.session = session
        self.user_id = user_id

    async def create_conversation(self) -> Conversation:
        """Create a new conversation for the user.

        Returns:
            New Conversation instance with generated ID
        """
        conversation = Conversation(user_id=self.user_id)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def load_conversation_history(
        self, conversation_id: UUID, max_messages: int = 50
    ) -> list[dict]:
        """Load conversation history with token truncation.

        Loads the most recent messages from the conversation, ordered chronologically.
        If the conversation has more than max_messages, only the most recent are loaded.
        This implements a simple form of token management by limiting message count.

        Args:
            conversation_id: Conversation to load history from
            max_messages: Maximum number of messages to load (default: 50)

        Returns:
            List of message dictionaries in chronological order, formatted for agent input

        Raises:
            ValueError: If conversation not found or access denied
        """
        # Verify conversation ownership
        statement = select(Conversation).where(
            Conversation.id == conversation_id, Conversation.user_id == self.user_id
        )
        result = await self.session.execute(statement)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise ValueError("Conversation not found or access denied")

        # Load messages (most recent first, then reverse for chronological order)
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(max_messages)
        )
        result = await self.session.execute(statement)
        messages = result.scalars().all()

        # Convert to agent input format (chronological order)
        history = []
        for message in reversed(messages):
            history.append({"role": message.role, "content": message.content})

        return history

    async def save_messages(
        self,
        conversation_id: UUID,
        user_message: str,
        assistant_response: str,
        tool_calls: Optional[dict] = None,
    ) -> tuple[Message, Message]:
        """Save user message and assistant response to database.

        Args:
            conversation_id: Conversation to add messages to
            user_message: User's message content
            assistant_response: AI assistant's response
            tool_calls: Optional tool call data from agent execution

        Returns:
            Tuple of (user_message_record, assistant_message_record)
        """
        # Create user message
        user_msg = Message(
            conversation_id=conversation_id, user_id=self.user_id, role="user", content=user_message
        )
        self.session.add(user_msg)

        # Create assistant message
        assistant_msg = Message(
            conversation_id=conversation_id,
            user_id=self.user_id,
            role="assistant",
            content=assistant_response,
            tool_calls=tool_calls,
        )
        self.session.add(assistant_msg)

        # Update conversation timestamp
        statement = select(Conversation).where(Conversation.id == conversation_id)
        result = await self.session.execute(statement)
        conversation = result.scalar_one()
        conversation.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(user_msg)
        await self.session.refresh(assistant_msg)

        return (user_msg, assistant_msg)

    async def run_agent_with_retry(
        self, user_message: str, conversation_history: Optional[list[dict]] = None
    ) -> dict:
        """Run AI agent with exponential backoff retry logic.

        Handles transient failures (rate limits, network issues) with exponential
        backoff. Guardrail exceptions are not retried as they indicate invalid input.

        Args:
            user_message: Current user message
            conversation_history: Previous messages in conversation (if any)

        Returns:
            Dict with 'response' (str) and optional 'tool_calls' (dict)

        Raises:
            InputGuardrailTripwireTriggered: If input guardrail blocks the message
            OutputGuardrailTripwireTriggered: If output guardrail blocks the response
            Exception: If all retries are exhausted
        """
        # Build input messages
        input_messages = conversation_history.copy() if conversation_history else []
        input_messages.append({"role": "user", "content": user_message})

        # Retry loop with exponential backoff
        last_exception = None
        delay = self.INITIAL_RETRY_DELAY

        for attempt in range(self.MAX_RETRIES):
            try:
                # Set user_id for tool execution
                from todo_api.agent.todo_agent import set_current_user_id

                set_current_user_id(self.user_id)

                # Run the agent
                print(f"DEBUG: Running agent attempt {attempt + 1}/{self.MAX_RETRIES}")
                result = await Runner.run(
                    todo_agent,
                    input_messages,
                    context={"user_id": self.user_id, "session": self.session},
                )
                print(f"DEBUG: Agent completed successfully")

                # Extract response and tool calls
                response_data = {
                    "response": result.final_output,
                    "tool_calls": getattr(result, "tool_calls", None),
                }

                return response_data

            except (InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered) as e:
                # Guardrail exceptions should not be retried
                print(f"DEBUG: Guardrail triggered: {type(e).__name__}")
                raise

            except Exception as e:
                print(f"DEBUG: Exception in agent: {type(e).__name__}: {str(e)}")
                last_exception = e

                # If this is the last attempt, raise the exception
                if attempt == self.MAX_RETRIES - 1:
                    raise

                # Wait with exponential backoff
                await asyncio.sleep(delay)
                delay = min(delay * 2, self.MAX_RETRY_DELAY)

        # This should not be reached, but just in case
        if last_exception:
            raise last_exception
        raise Exception("Agent execution failed with unknown error")
