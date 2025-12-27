"""FastMCP server instance for Todo task management tools.

This module creates and configures the FastMCP server that exposes
task management tools to AI agents.
"""

from fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP(
    name="todo-server",
    instructions=(
        "A task management server that provides tools for creating, reading, "
        "updating, and deleting todo tasks. All tools require a user_id parameter "
        "to ensure user data isolation. Tasks include title, description, priority "
        "(HIGH, MEDIUM, LOW), and status (pending or completed)."
    ),
)
