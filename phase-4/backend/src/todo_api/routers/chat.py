"""Chat API router for conversational AI task management.

This module provides REST API endpoints for AI-powered chat conversations,
including JWT authentication, message validation, and error handling.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from agents.exceptions import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.database import get_session
from todo_api.middleware.auth import get_current_user_id, verify_user_authorization
from todo_api.services.chat_service import ChatService

# ============================================================================
# Request/Response Models
# ============================================================================


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    conversation_id: Optional[UUID] = Field(
        None, description="Existing conversation ID to resume (omit to start new conversation)"
    )
    message: str = Field(..., min_length=1, max_length=2000, description="User message content")


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""

    conversation_id: UUID = Field(..., description="Conversation ID (new or existing)")
    response: str = Field(..., description="AI assistant response")
    tool_calls: Optional[dict] = Field(None, description="MCP tools invoked (if any)")


class ConversationListResponse(BaseModel):
    """Response body for conversation list endpoint (T097)."""

    conversations: list[dict] = Field(
        ..., description="List of conversations ordered by updated_at DESC"
    )


class ConversationDetailResponse(BaseModel):
    """Response body for conversation detail endpoint (T094)."""

    id: UUID = Field(..., description="Conversation ID")
    created_at: str = Field(..., description="ISO timestamp when conversation was created")
    updated_at: str = Field(..., description="ISO timestamp when conversation was last updated")
    messages: list[dict] = Field(..., description="List of messages in chronological order")


class UpdateConversationRequest(BaseModel):
    """Request body for updating conversation."""

    title: str = Field(..., min_length=1, max_length=200, description="New conversation title")


# ============================================================================
# Router Configuration
# ============================================================================

router = APIRouter(
    prefix="/api",
    tags=["chat"],
    responses={
        401: {"description": "Unauthorized - missing or invalid JWT"},
        403: {"description": "Forbidden - user_id mismatch or guardrail blocked"},
        500: {"description": "Internal server error"},
    },
)


# ============================================================================
# Chat Endpoint
# ============================================================================


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send chat message to AI assistant",
    description=(
        "Send a message to the AI assistant and receive a response. "
        "The assistant manages todos through natural language using MCP tools. "
        "Conversation history is loaded from database and truncated if needed."
    ),
)
async def send_chat_message(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id),
) -> ChatResponse:
    """Send message to AI assistant and receive response.

    This endpoint orchestrates the entire chat workflow:
    1. Validate JWT and user_id match
    2. Validate message length (1-2000 characters)
    3. Load or create conversation
    4. Load conversation history (if resuming)
    5. Run AI agent with guardrails
    6. Save messages to database
    7. Return response

    Args:
        user_id: Path parameter - must match JWT user_id
        request: Chat request with message and optional conversation_id
        session: Database session (injected)
        current_user: Current user from JWT (injected)

    Returns:
        ChatResponse with conversation_id, response, and optional tool_calls

    Raises:
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 403: If guardrail blocks the message
        HTTPException 404: If conversation_id not found
        HTTPException 429: If rate limit exceeded
        HTTPException 500: If agent or database error
    """
    # T042: Cookie-based auth validation - verify user_id matches token
    authorized_user_id = verify_user_authorization(user_id, token_user_id)

    # T044: Message validation (1-2000 characters) - handled by Pydantic Field constraints
    # Already validated by ChatRequest model

    # Initialize ChatService
    chat_service = ChatService(session=session, user_id=authorized_user_id)

    try:
        # T043: Handle conversation_id parameter
        conversation = None
        conversation_history = None

        if request.conversation_id:
            # Resume existing conversation
            try:
                conversation_history = await chat_service.load_conversation_history(
                    conversation_id=request.conversation_id
                )
                conversation_id = request.conversation_id
            except ValueError:
                # Conversation not found or access denied
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or access denied",
                )
        else:
            # Create new conversation
            conversation = await chat_service.create_conversation()
            conversation_id = conversation.id

        # T045: Integrate ChatService - run agent with retry
        try:
            agent_result = await chat_service.run_agent_with_retry(
                user_message=request.message, conversation_history=conversation_history
            )
        except InputGuardrailTripwireTriggered:
            # T046: Handle guardrail blocks - input guardrail blocked off-topic message
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "I'm your todo assistant and can only help with task management. "
                    "I can help you: add tasks, view tasks, mark complete, delete tasks, "
                    "update details. What would you like to do?"
                ),
            )
        except OutputGuardrailTripwireTriggered:
            # Output guardrail blocked invalid response
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to generate valid response. Please try again.",
            )
        except Exception as e:
            # T046: Handle rate limits and other errors
            error_message = str(e).lower()

            if "rate" in error_message or "quota" in error_message or "429" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="High demand. Please wait 30s and try again.",
                    headers={"Retry-After": "30"},
                )

            # Generic agent error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to process request. Please try again.",
            )

        # Save messages to database
        try:
            await chat_service.save_messages(
                conversation_id=conversation_id,
                user_message=request.message,
                assistant_response=agent_result["response"],
                tool_calls=agent_result.get("tool_calls"),
            )
        except Exception as e:
            # Database error during save
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to save conversation. Please try again.",
            )

        # Return successful response
        return ChatResponse(
            conversation_id=conversation_id,
            response=agent_result["response"],
            tool_calls=agent_result.get("tool_calls"),
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# ============================================================================
# Phase 7 - User Story 7: Resume Previous Conversations (T097-T098)
# ============================================================================


@router.get(
    "/{user_id}/conversations",
    response_model=ConversationListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user's conversation list",
    description=(
        "Get list of all conversations for the authenticated user, "
        "sorted by updated_at in descending order (most recent first). "
        "Used for displaying conversation history and resuming previous chats."
    ),
)
async def get_conversations(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id),
) -> ConversationListResponse:
    """Get list of user's conversations (T097).

    Returns all conversations belonging to the user, sorted by most recently updated first.
    This enables users to view and resume previous conversations.

    Args:
        user_id: Path parameter - must match JWT user_id
        session: Database session (injected)
        token_user_id: Current user from JWT (injected)

    Returns:
        ConversationListResponse with list of conversations

    Raises:
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 500: If database error
    """
    from sqlmodel import desc, select

    from todo_api.models import Conversation

    # Validate user authorization
    authorized_user_id = verify_user_authorization(user_id, token_user_id)

    try:
        # T095: Query conversations sorted by updated_at DESC
        statement = (
            select(Conversation)
            .where(Conversation.user_id == authorized_user_id)
            .order_by(desc(Conversation.updated_at))
        )

        result = await session.execute(statement)
        conversations = result.scalars().all()

        # Convert to response format
        conversations_data = [
            {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
            }
            for conv in conversations
        ]

        return ConversationListResponse(conversations=conversations_data)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversations: {str(e)}",
        )


@router.get(
    "/{user_id}/conversations/{conversation_id}",
    response_model=ConversationDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get conversation by ID with messages",
    description=(
        "Get a specific conversation with all its messages. "
        "Supports pagination with limit and offset query parameters. "
        "Used for resuming conversations and displaying message history."
    ),
)
async def get_conversation_by_id(
    user_id: str,
    conversation_id: UUID,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id),
) -> ConversationDetailResponse:
    """Get conversation by ID with messages (T094, T096).

    Returns conversation details with messages in chronological order.
    Supports pagination for "Load more" functionality.

    Args:
        user_id: Path parameter - must match JWT user_id
        conversation_id: Conversation ID to retrieve
        limit: Maximum number of messages to return (default: 50, max: 100)
        offset: Number of messages to skip (default: 0)
        session: Database session (injected)
        token_user_id: Current user from JWT (injected)

    Returns:
        ConversationDetailResponse with conversation and messages

    Raises:
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 404: If conversation not found or access denied
        HTTPException 500: If database error
    """
    from sqlmodel import select

    from todo_api.models import Conversation, Message

    # Validate user authorization
    authorized_user_id = verify_user_authorization(user_id, token_user_id)

    # Validate pagination parameters
    if limit > 100:
        limit = 100
    if offset < 0:
        offset = 0

    try:
        # Query conversation with user ownership check
        conversation_statement = select(Conversation).where(
            Conversation.id == conversation_id, Conversation.user_id == authorized_user_id
        )

        conversation_result = await session.execute(conversation_statement)
        conversation = conversation_result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied",
            )

        # T096: Query messages with pagination
        messages_statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)  # Chronological order (oldest first)
            .offset(offset)
            .limit(limit)
        )

        messages_result = await session.execute(messages_statement)
        messages = messages_result.scalars().all()

        # Convert messages to response format
        messages_data = [
            {
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
                "tool_calls": msg.tool_calls,
            }
            for msg in messages
        ]

        return ConversationDetailResponse(
            id=conversation.id,
            created_at=conversation.created_at.isoformat(),
            updated_at=conversation.updated_at.isoformat(),
            messages=messages_data,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversation: {str(e)}",
        )


@router.patch(
    "/{user_id}/conversations/{conversation_id}",
    status_code=status.HTTP_200_OK,
    summary="Update conversation (rename)",
    description=(
        "Update conversation properties such as title. User must own the conversation to update it."
    ),
)
async def update_conversation(
    user_id: str,
    conversation_id: UUID,
    request_body: UpdateConversationRequest,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id),
):
    """Update conversation by ID (rename).

    Updates conversation properties like title.
    Only the conversation owner can update it.

    Args:
        user_id: Path parameter - must match JWT user_id
        conversation_id: Conversation ID to update
        request_body: Update request with new title
        session: Database session (injected)
        token_user_id: Current user from JWT (injected)

    Returns:
        200 OK with updated conversation data

    Raises:
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 404: If conversation not found or access denied
        HTTPException 500: If database error
    """
    from sqlmodel import select

    from todo_api.models import Conversation

    # Validate user authorization
    authorized_user_id = verify_user_authorization(user_id, token_user_id)

    try:
        # Verify conversation exists and user owns it
        conversation_statement = select(Conversation).where(
            Conversation.id == conversation_id, Conversation.user_id == authorized_user_id
        )

        conversation_result = await session.execute(conversation_statement)
        conversation = conversation_result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied",
            )

        # Update the title
        conversation.title = request_body.title
        conversation.updated_at = datetime.utcnow()

        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Return updated conversation
        return {
            "id": str(conversation.id),
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update conversation: {str(e)}",
        )


@router.delete(
    "/{user_id}/conversations/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete conversation by ID",
    description=(
        "Delete a specific conversation and all its messages. "
        "This action is permanent and cannot be undone. "
        "User must own the conversation to delete it."
    ),
)
async def delete_conversation(
    user_id: str,
    conversation_id: UUID,
    session: AsyncSession = Depends(get_session),
    token_user_id: str = Depends(get_current_user_id),
):
    """Delete conversation by ID.

    Permanently deletes a conversation and all associated messages.
    Only the conversation owner can delete it.

    Args:
        user_id: Path parameter - must match JWT user_id
        conversation_id: Conversation ID to delete
        session: Database session (injected)
        token_user_id: Current user from JWT (injected)

    Returns:
        204 No Content on success

    Raises:
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 404: If conversation not found or access denied
        HTTPException 500: If database error
    """
    from sqlmodel import delete, select

    from todo_api.models import Conversation, Message

    # Validate user authorization
    authorized_user_id = verify_user_authorization(user_id, token_user_id)

    try:
        # Verify conversation exists and user owns it
        conversation_statement = select(Conversation).where(
            Conversation.id == conversation_id, Conversation.user_id == authorized_user_id
        )

        conversation_result = await session.execute(conversation_statement)
        conversation = conversation_result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied",
            )

        # Delete all messages in the conversation first (cascade)
        delete_messages_statement = delete(Message).where(
            Message.conversation_id == conversation_id
        )
        await session.execute(delete_messages_statement)

        # Delete the conversation
        await session.delete(conversation)
        await session.commit()

        # Return 204 No Content (no response body needed)
        return None

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete conversation: {str(e)}",
        )
