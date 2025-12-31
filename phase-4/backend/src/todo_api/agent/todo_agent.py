"""Todo management AI agent with MCP tools and guardrails.

This module creates the main AI agent for natural language task management,
integrating task management tools and input/output guardrails.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from uuid import UUID

from agents import Agent, function_tool
from sqlmodel import select

from todo_api.agent.guardrails import response_validator_guard, todo_topic_guard
from todo_api.database import AsyncSessionLocal
from todo_api.models import Task
from todo_api.models.enums import PriorityEnum

# ============================================================================
# Agent Tools (Direct Implementation)
# ============================================================================

# Global variable to store current user_id (set by chat service before agent runs)
_current_user_id: str | None = None


def set_current_user_id(user_id: str):
    """Set the current user ID for tool execution."""
    global _current_user_id
    _current_user_id = user_id


@function_tool
async def list_tasks(
    status: Annotated[str | None, "Filter by status: 'all', 'pending', or 'completed'"] = "all",
) -> list[dict[str, Any]]:
    """List all tasks for the current user with optional status filtering.

    Args:
        status: Filter tasks by completion status:
            - 'all': Return all tasks (default)
            - 'pending': Return only incomplete tasks
            - 'completed': Return only completed tasks

    Returns:
        List of task dictionaries ordered by created_at DESC (newest first)
    """
    global _current_user_id

    if not _current_user_id:
        raise ValueError("user_id not set - internal error")

    # Normalize status parameter
    status_lower = status.lower() if status else "all"

    async with AsyncSessionLocal() as session:
        # Build query with status filter
        statement = select(Task).where(Task.user_id == _current_user_id)

        if status_lower == "pending":
            statement = statement.where(Task.is_completed == False)
        elif status_lower == "completed":
            statement = statement.where(Task.is_completed == True)
        # 'all' - no additional filter

        statement = statement.order_by(Task.created_at.desc())

        result = await session.execute(statement)
        tasks = result.scalars().all()

        return [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "is_completed": task.is_completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            }
            for task in tasks
        ]


@function_tool
async def create_task(
    title: Annotated[str, "Task title (1-200 characters)"],
    description: Annotated[str | None, "Optional task description (max 2000 characters)"] = None,
    priority: Annotated[str, "Task priority: 'high', 'medium', or 'low'"] = "medium",
    due_date: Annotated[
        str | None,
        "Optional due date in natural language (e.g., 'tomorrow', 'in 3 days', 'next week')",
    ] = None,
) -> dict[str, Any]:
    """Create a new task for the current user.

    Args:
        title: Task title (required, 1-200 chars)
        description: Optional task description (max 2000 chars)
        priority: Priority level - 'high', 'medium', or 'low' (default: 'medium')
        due_date: Optional due date in natural language

    Returns:
        Created task dictionary with id, title, description, priority, etc.
    """
    global _current_user_id

    if not _current_user_id:
        raise ValueError("user_id not set - internal error")

    # Validate and normalize priority
    priority_lower = priority.lower()
    if priority_lower not in {"high", "medium", "low"}:
        priority_lower = "medium"

    # Parse natural language due date (basic implementation)
    parsed_due_date = None
    if due_date:
        due_date_lower = due_date.lower().strip()
        now = datetime.now(timezone.utc)

        if "tomorrow" in due_date_lower:
            parsed_due_date = now + timedelta(days=1)
        elif "today" in due_date_lower:
            parsed_due_date = now
        elif "next week" in due_date_lower:
            parsed_due_date = now + timedelta(weeks=1)
        elif "week" in due_date_lower:
            parsed_due_date = now + timedelta(weeks=1)
        else:
            # Try to extract number of days (e.g., "in 3 days", "after 2 days")
            import re

            match = re.search(r"(\d+)\s*days?", due_date_lower)
            if match:
                days = int(match.group(1))
                parsed_due_date = now + timedelta(days=days)

        # Remove timezone info for PostgreSQL TIMESTAMP WITHOUT TIME ZONE
        if parsed_due_date:
            parsed_due_date = parsed_due_date.replace(tzinfo=None)

    async with AsyncSessionLocal() as session:
        task = Task(
            user_id=_current_user_id,
            title=title,
            description=description,
            priority=PriorityEnum(priority_lower),
            target_completion_date=parsed_due_date,
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

        # Construct return dict while session is still active
        result = {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "is_completed": task.is_completed,
            "target_completion_date": task.target_completion_date.isoformat()
            if task.target_completion_date
            else None,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }

    return result


@function_tool
async def update_task(
    task_id: Annotated[str, "Task ID (UUID)"],
    title: Annotated[str | None, "New task title (1-200 characters)"] = None,
    description: Annotated[str | None, "New task description (max 2000 characters)"] = None,
    priority: Annotated[str | None, "New priority: 'high', 'medium', or 'low'"] = None,
) -> dict[str, Any]:
    """Update an existing task.

    Args:
        task_id: Task ID (required)
        title: New task title (optional)
        description: New task description (optional)
        priority: New priority level (optional)

    Returns:
        Updated task dictionary
    """
    global _current_user_id

    if not _current_user_id:
        raise ValueError("user_id not set - internal error")

    async with AsyncSessionLocal() as session:
        # Fetch task and verify ownership
        statement = select(Task).where(Task.id == UUID(task_id), Task.user_id == _current_user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task {task_id} not found or access denied")

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            priority_lower = priority.lower()
            if priority_lower in {"high", "medium", "low"}:
                task.priority = PriorityEnum(priority_lower)

        # Remove timezone for PostgreSQL TIMESTAMP WITHOUT TIME ZONE
        task.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await session.commit()
        await session.refresh(task)

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "is_completed": task.is_completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }


@function_tool
async def complete_task(
    task_id: Annotated[str, "Task ID (UUID)"],
) -> dict[str, Any]:
    """Mark a task as completed.

    Args:
        task_id: Task ID (required)

    Returns:
        Updated task dictionary with is_completed=True
    """
    global _current_user_id

    if not _current_user_id:
        raise ValueError("user_id not set - internal error")

    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.id == UUID(task_id), Task.user_id == _current_user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task {task_id} not found or access denied")

        # Remove timezone for PostgreSQL TIMESTAMP WITHOUT TIME ZONE
        now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        task.is_completed = True
        task.completed_at = now_naive
        task.updated_at = now_naive
        await session.commit()
        await session.refresh(task)

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "is_completed": task.is_completed,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }


@function_tool
async def delete_task(
    task_id: Annotated[str, "Task ID (UUID)"],
) -> dict[str, str]:
    """Delete a task permanently.

    Args:
        task_id: Task ID (required)

    Returns:
        Confirmation message
    """
    global _current_user_id

    if not _current_user_id:
        raise ValueError("user_id not set - internal error")

    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.id == UUID(task_id), Task.user_id == _current_user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task {task_id} not found or access denied")

        task_title = task.title
        await session.delete(task)
        await session.commit()

        return {
            "message": f"Task '{task_title}' deleted successfully",
            "task_id": task_id,
        }


# ============================================================================
# Todo Agent Configuration
# ============================================================================

todo_agent = Agent(
    name="Todo Assistant",
    instructions=(
        "You are a helpful AI assistant for managing todo tasks. "
        "Your role is to help users create, view, update, complete, and delete tasks "
        "through natural language conversation.\n"
        "\n"
        "## Your Capabilities\n"
        "\n"
        "You can help users with:\n"
        "- **Creating tasks**: Use create_task() to add new tasks with title, description, priority, and optional due date\n"
        "- **Viewing tasks**: Use list_tasks(status) to show tasks:\n"
        "  - list_tasks('all') - show all tasks (default)\n"
        "  - list_tasks('pending') - show only incomplete tasks\n"
        "  - list_tasks('completed') - show only completed tasks\n"
        "- **Updating tasks**: Use update_task() to modify task title, description, or priority\n"
        "- **Completing tasks**: Use complete_task() to mark tasks as done\n"
        "- **Deleting tasks**: Use delete_task() to remove tasks permanently\n"
        "\n"
        "## Communication Style\n"
        "\n"
        "- Be conversational and friendly\n"
        "- When showing task lists from list_tasks(), ALWAYS include BOTH:\n"
        "  1. A friendly summary message\n"
        "  2. The exact JSON data block wrapped like this:\n"
        "     ```json\n"
        '     {"tasks": [exact task data from list_tasks()]}\n'
        "     ```\n"
        "- The frontend will parse this JSON and render beautiful task cards\n"
        "- Keep responses concise but helpful\n"
        "- After creating, updating, or completing a task, show the updated task list\n"
        "\n"
        "## Task Priority Levels\n"
        "\n"
        "- **high**: Urgent or important tasks (use when user says 'urgent', 'important', 'critical', 'asap')\n"
        "- **medium**: Regular tasks (default if not specified)\n"
        "- **low**: Optional or low-priority tasks (use when user says 'low priority', 'optional', 'when possible')\n"
        "\n"
        "## Natural Language Due Dates\n"
        "\n"
        "The create_task tool accepts natural language due dates like:\n"
        "- 'tomorrow', 'today'\n"
        "- 'in 3 days', 'after 2 days'\n"
        "- 'next week', 'in a week'\n"
        "\n"
        "Extract due dates from user messages and pass them to create_task.\n"
        "\n"
        "## Important Notes\n"
        "\n"
        "- ALWAYS use the tools to fetch/modify real task data - never make up tasks\n"
        "- All tools automatically use the current user's ID (no need to pass user_id)\n"
        "- When users say 'show', 'list', 'view' tasks, use list_tasks()\n"
        "- When users say 'add', 'create', 'new' task, use create_task()\n"
        "- When users want to mark tasks done, use complete_task()\n"
        "- When users want to change/edit tasks, use update_task()\n"
        "- When users want to remove/delete tasks, use delete_task()\n"
        "- If you encounter an error, explain it clearly and suggest what the user can do\n"
    ),
    tools=[list_tasks, create_task, update_task, complete_task, delete_task],
    input_guardrails=[todo_topic_guard],
    output_guardrails=[response_validator_guard],
)
