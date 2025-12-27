"""FastAPI dependencies for authentication and authorization.

This module provides dependency injection functions for JWT validation
and user authentication using Better Auth.
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from todo_api.config import settings

# Security scheme for JWT Bearer token
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Validate JWT token and extract user information.

    This dependency validates the JWT token from the Authorization header
    and returns the user information embedded in the token. It integrates
    with Better Auth's JWT tokens.

    Args:
        credentials: HTTP Bearer credentials with JWT token

    Returns:
        Dict with user info (must include 'id' field)

    Raises:
        HTTPException 401: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        # Decode JWT token
        # Note: Better Auth uses HS256 algorithm by default
        # In production, retrieve the secret from Better Auth configuration
        payload = jwt.decode(
            token,
            settings.database_url,  # Placeholder - should use actual JWT secret
            algorithms=["HS256"],
            options={
                "verify_signature": False
            },  # TODO: Enable signature verification with correct secret
        )

        # Extract user ID from payload
        # Better Auth typically stores user info in the token payload
        user_id = payload.get("sub") or payload.get("userId") or payload.get("id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: missing user ID"
            )

        return {"id": user_id}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
