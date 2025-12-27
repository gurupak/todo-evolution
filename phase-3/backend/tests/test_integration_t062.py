"""Integration test for T062: Task creation via chat interface.

This test verifies the complete flow:
1. User sends "Add task to buy milk" via chat
2. AI agent calls create_task tool
3. Task is created in database
4. Task appears in Phase II UI (verified by querying database)
"""

import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.models import Conversation, Message, Task


@pytest.mark.asyncio
async def test_full_integration_add_task_via_chat(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """Full integration test: Chat 'Add task to buy milk' → Verify task in chat response → Verify task in Phase II UI."""

    # Step 1: Send chat message to create a task
    chat_payload = {"message": "Add task to buy milk, priority high, due tomorrow"}

    response = await client.post(
        f"/api/{test_user_id}/chat",
        json=chat_payload,
        headers=auth_headers,
    )

    assert response.status_code == 200
    chat_data = response.json()

    # Step 2: Verify chat response structure
    assert "conversation_id" in chat_data
    assert "response" in chat_data

    conversation_id = chat_data["conversation_id"]
    ai_response = chat_data["response"]

    # AI response should confirm task creation
    assert "milk" in ai_response.lower() or "task" in ai_response.lower()

    # Step 3: Verify conversation was created in database
    statement = select(Conversation).where(Conversation.id == conversation_id)
    db_result = await session.execute(statement)
    conversation = db_result.scalar_one_or_none()

    assert conversation is not None
    assert conversation.user_id == test_user_id

    # Step 4: Verify messages were saved
    message_statement = select(Message).where(Message.conversation_id == conversation_id)
    message_result = await session.execute(message_statement)
    messages = message_result.scalars().all()

    assert len(messages) >= 2  # At least user message + assistant response

    # Find user and assistant messages
    user_messages = [m for m in messages if m.role == "user"]
    assistant_messages = [m for m in messages if m.role == "assistant"]

    assert len(user_messages) >= 1
    assert len(assistant_messages) >= 1
    assert user_messages[0].content == chat_payload["message"]

    # Step 5: Verify task was created in database (Phase II UI would query this)
    task_statement = select(Task).where(Task.user_id == test_user_id)
    task_result = await session.execute(task_statement)
    tasks = task_result.scalars().all()

    assert len(tasks) >= 1

    # Find the task we just created
    milk_task = next((t for t in tasks if "milk" in t.title.lower()), None)
    assert milk_task is not None, "Task 'buy milk' should be created"

    # Step 6: Verify task properties
    assert milk_task.user_id == test_user_id
    assert "milk" in milk_task.title.lower()
    assert milk_task.priority.value == "high"  # We requested high priority
    assert milk_task.is_completed is False
    assert milk_task.due_date is not None  # We requested "due tomorrow"

    # Verify due_date is approximately 1 day from now
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    time_diff = (milk_task.due_date - now).total_seconds()
    assert 23 * 3600 < time_diff < 25 * 3600  # Between 23 and 25 hours

    print(f"\n✓ Integration test passed:")
    print(f"  - Conversation created: {conversation_id}")
    print(f"  - Messages saved: {len(messages)}")
    print(f"  - Task created: {milk_task.title} (ID: {milk_task.id})")
    print(f"  - Task priority: {milk_task.priority}")
    print(f"  - Task due date: {milk_task.due_date}")
    print(f"  - AI response: {ai_response[:100]}...")


@pytest.mark.asyncio
async def test_multiple_tasks_created_in_same_conversation(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """Test creating multiple tasks in the same conversation."""

    # Create first task
    response1 = await client.post(
        f"/api/{test_user_id}/chat",
        json={"message": "Add task: Buy groceries"},
        headers=auth_headers,
    )

    assert response1.status_code == 200
    data1 = response1.json()
    conversation_id = data1["conversation_id"]

    # Create second task in same conversation
    response2 = await client.post(
        f"/api/{test_user_id}/chat",
        json={
            "message": "Add another task: Call dentist for appointment",
            "conversation_id": conversation_id,
        },
        headers=auth_headers,
    )

    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["conversation_id"] == conversation_id

    # Verify both tasks exist in database
    task_statement = select(Task).where(Task.user_id == test_user_id)
    task_result = await session.execute(task_statement)
    tasks = task_result.scalars().all()

    assert len(tasks) >= 2

    task_titles = {t.title.lower() for t in tasks}
    assert any("groceries" in title for title in task_titles)
    assert any("dentist" in title or "call" in title for title in task_titles)

    print(f"\n✓ Multiple tasks created successfully:")
    for task in tasks:
        print(f"  - {task.title} (Priority: {task.priority})")


@pytest.mark.asyncio
async def test_task_appears_in_phase_ii_list_endpoint(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """Test that tasks created via chat appear in Phase II's list tasks endpoint."""

    # Create task via chat (Phase III)
    chat_response = await client.post(
        f"/api/{test_user_id}/chat",
        json={"message": "Create a task: Prepare presentation for meeting"},
        headers=auth_headers,
    )

    assert chat_response.status_code == 200

    # Query tasks using Phase II endpoint
    tasks_response = await client.get(
        f"/api/{test_user_id}/tasks",
        headers=auth_headers,
    )

    assert tasks_response.status_code == 200
    tasks_data = tasks_response.json()

    # Verify the task appears in the list
    task_titles = [task["title"] for task in tasks_data]
    assert any(
        "presentation" in title.lower() or "meeting" in title.lower() for title in task_titles
    )

    print(f"\n✓ Task appears in Phase II UI:")
    print(f"  - Total tasks: {len(tasks_data)}")
    print(f"  - Tasks: {task_titles}")


@pytest.mark.asyncio
async def test_task_creation_with_various_natural_language_inputs(
    client: AsyncClient,
    test_user_id: str,
    session: AsyncSession,
    auth_headers: dict,
):
    """Test task creation with different natural language patterns."""

    test_messages = [
        "Add a high priority task to review code",
        "Create task: Water plants, low priority",
        "I need to add a task for team standup meeting tomorrow",
        "New task: Submit expense report, medium priority, due in 3 days",
    ]

    for message in test_messages:
        response = await client.post(
            f"/api/{test_user_id}/chat",
            json={"message": message},
            headers=auth_headers,
        )

        assert response.status_code == 200, f"Failed for message: {message}"
        data = response.json()
        assert "response" in data
        assert len(data["response"]) > 0

    # Verify all tasks were created
    task_statement = select(Task).where(Task.user_id == test_user_id)
    task_result = await session.execute(task_statement)
    tasks = task_result.scalars().all()

    assert len(tasks) >= len(test_messages)

    print(f"\n✓ Natural language task creation:")
    print(f"  - Test messages: {len(test_messages)}")
    print(f"  - Tasks created: {len(tasks)}")
    for task in tasks:
        print(f"  - {task.title} (Priority: {task.priority}, Due: {task.due_date})")
