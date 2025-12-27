"""Tests for Task API endpoints."""

from uuid import uuid4

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task_endpoint(client: AsyncClient, test_user_id: str, test_jwt_token: str):
    """Test POST /tasks endpoint creates task (T066)."""
    response = await client.post(
        f"/api/{test_user_id}/tasks",
        json={
            "title": "New Task",
            "description": "Task description",
            "priority": "high",
        },
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["description"] == "Task description"
    assert data["priority"] == "high"
    assert data["is_completed"] is False


@pytest.mark.asyncio
async def test_list_tasks_endpoint(client: AsyncClient, test_user_id: str, test_jwt_token: str):
    """Test GET /tasks endpoint lists tasks (T067)."""
    # Create a task first
    await client.post(
        f"/api/{test_user_id}/tasks",
        json={"title": "Task 1", "description": "", "priority": "medium"},
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    # List tasks
    response = await client.get(
        f"/api/{test_user_id}/tasks",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert "total" in data
    assert "completed" in data
    assert "pending" in data
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_get_task_by_id_endpoint(client: AsyncClient, test_user_id: str, test_jwt_token: str):
    """Test GET /tasks/{id} endpoint gets specific task (T068)."""
    # Create a task
    create_response = await client.post(
        f"/api/{test_user_id}/tasks",
        json={"title": "Specific Task", "description": "", "priority": "low"},
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )
    task_id = create_response.json()["id"]

    # Get the task
    response = await client.get(
        f"/api/{test_user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"


@pytest.mark.asyncio
async def test_validation_error_empty_title(
    client: AsyncClient, test_user_id: str, test_jwt_token: str
):
    """Test validation error for empty title (T069)."""
    response = await client.post(
        f"/api/{test_user_id}/tasks",
        json={"title": "", "description": "", "priority": "medium"},
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_access_other_user_task_returns_403(client: AsyncClient, test_jwt_token: str):
    """Test accessing another user's task returns 403 (T061)."""
    # Create a task for user 1
    user1_id = "550e8400-e29b-41d4-a716-446655440000"
    create_response = await client.post(
        f"/api/{user1_id}/tasks",
        json={"title": "User 1 Task", "description": "", "priority": "high"},
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )
    task_id = create_response.json()["id"]

    # Try to access it as user 2
    user2_id = "550e8400-e29b-41d4-a716-446655440001"
    response = await client.get(
        f"/api/{user2_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_missing_jwt_returns_401(client: AsyncClient, test_user_id: str):
    """Test missing JWT returns 401 (T062)."""
    response = await client.get(f"/api/{test_user_id}/tasks")

    # Should be 403 because HTTPBearer requires Authorization header
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_task_endpoint(client: AsyncClient, test_user_id: str, test_jwt_token: str):
    """Test PUT /tasks/{id} endpoint updates task."""
    # Create a task
    create_response = await client.post(
        f"/api/{test_user_id}/tasks",
        json={"title": "Original", "description": "", "priority": "low"},
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )
    task_id = create_response.json()["id"]

    # Update the task
    response = await client.put(
        f"/api/{test_user_id}/tasks/{task_id}",
        json={"title": "Updated", "priority": "high"},
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["priority"] == "high"


@pytest.mark.asyncio
async def test_toggle_complete_endpoint(
    client: AsyncClient, test_user_id: str, test_jwt_token: str
):
    """Test PATCH /tasks/{id}/complete endpoint toggles completion."""
    # Create a task
    create_response = await client.post(
        f"/api/{test_user_id}/tasks",
        json={"title": "To Complete", "description": "", "priority": "medium"},
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )
    task_id = create_response.json()["id"]

    # Toggle to completed
    response = await client.patch(
        f"/api/{test_user_id}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["is_completed"] is True


@pytest.mark.asyncio
async def test_delete_task_endpoint(client: AsyncClient, test_user_id: str, test_jwt_token: str):
    """Test DELETE /tasks/{id} endpoint deletes task."""
    # Create a task
    create_response = await client.post(
        f"/api/{test_user_id}/tasks",
        json={"title": "To Delete", "description": "", "priority": "low"},
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )
    task_id = create_response.json()["id"]

    # Delete the task
    response = await client.delete(
        f"/api/{test_user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["id"] == task_id
