"""MCP tools for task management.

This module defines the task management tools exposed via FastMCP
that AI agents can use to interact with the todo database.
"""

from typing import Any
from uuid import UUID

from sqlmodel import select

from todo_api.database import AsyncSessionLocal
from todo_api.mcp.server import mcp
from todo_api.models import Task


@mcp.tool()
async def list_tasks(user_id: str) -> list[dict[str, Any]]:
    """List all tasks for a specific user.

    Args:
        user_id: The ID of the user whose tasks to retrieve

    Returns:
        List of task dictionaries with all task fields, ordered by created_at DESC
    """
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
        result = await session.execute(statement)
        tasks = result.scalars().all()

        # Convert to list of dictionaries
        return [
            {
                "id": str(task.id),
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "is_completed": task.is_completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            }
            for task in tasks
        ]
