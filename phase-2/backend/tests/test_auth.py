"""Tests for JWT authentication middleware."""

import time

import pytest
from httpx import AsyncClient
from jose import jwt

from todo_api.config import settings


@pytest.mark.asyncio
async def test_valid_token(client: AsyncClient, test_user_id: str, test_jwt_token: str):
    """Test request with valid JWT token succeeds (T050)."""
    response = await client.get(
        f"/api/{test_user_id}/tasks",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_expired_token(client: AsyncClient, test_user_id: str):
    """Test request with expired JWT token returns 401 (T051)."""
    # Create an expired token (expiry set to 1 second ago)
    payload = {
        "sub": test_user_id,
        "email": "test@example.com",
        "exp": int(time.time()) - 1,  # Expired 1 second ago
    }
    expired_token = jwt.encode(payload, settings.better_auth_secret, algorithm="HS256")

    response = await client.get(
        f"/api/{test_user_id}/tasks",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_invalid_token(client: AsyncClient, test_user_id: str):
    """Test request with invalid JWT token returns 401 (T052)."""
    response = await client.get(
        f"/api/{test_user_id}/tasks",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_missing_token(client: AsyncClient, test_user_id: str):
    """Test request without JWT token returns 403 (T053)."""
    response = await client.get(f"/api/{test_user_id}/tasks")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_user_id_mismatch(client: AsyncClient, test_jwt_token: str):
    """Test accessing another user's resources returns 403 (T058)."""
    other_user_id = "550e8400-e29b-41d4-a716-446655440001"
    response = await client.get(
        f"/api/{other_user_id}/tasks",
        headers={"Authorization": f"Bearer {test_jwt_token}"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to access this resource"
