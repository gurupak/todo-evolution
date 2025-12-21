"""Better Auth session authentication middleware."""

from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session


def parse_cookie_header(cookie_header: Optional[str], cookie_name: str) -> Optional[str]:
    """Parse a specific cookie from Cookie header string."""
    if not cookie_header:
        return None

    # Parse cookies from header like "cookie1=value1; cookie2=value2"
    cookies = {}
    for cookie in cookie_header.split(";"):
        cookie = cookie.strip()
        if "=" in cookie:
            name, value = cookie.split("=", 1)
            cookies[name.strip()] = value.strip()

    return cookies.get(cookie_name)


async def get_current_user_id(
    cookie: Optional[str] = Header(None, alias="Cookie"),
    db: AsyncSession = Depends(get_session),
) -> str:
    """Extract user_id from Better Auth session cookie."""
    # Debug logging
    print(f"DEBUG: Cookie header received: {cookie}")

    # Parse the session token from Cookie header
    session_token = parse_cookie_header(cookie, "better-auth.session_token")

    print(f"DEBUG: Parsed session token: {session_token}")

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated - no session cookie",
        )

    # Parse the session token (Better Auth format: token.signature)
    try:
        token_value = session_token.split(".")[0]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session token format",
        )

    print(f"DEBUG: Looking for token in DB: {token_value}")

    # First, let's see what tokens are in the database
    all_tokens = await db.execute(text("SELECT token FROM session LIMIT 5"))
    print(f"DEBUG: All tokens in DB: {[row[0] for row in all_tokens.fetchall()]}")

    # Query the session table using raw SQL
    result = await db.execute(
        text('SELECT "userId", "expiresAt", token FROM session WHERE token = :token'),
        {"token": token_value},
    )
    session_data = result.first()

    print(f"DEBUG: Session found: {session_data}")

    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found",
        )

    # Extract data (userId, expiresAt, token)
    user_id = session_data[0]
    expires_at = session_data[1]

    print(f"DEBUG: user_id={user_id}, expires_at={expires_at}")

    # Check if session is expired
    if expires_at:
        # Make expires_at timezone-aware if it's naive
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)
        print(f"DEBUG: Checking expiry - expires_at={expires_at}, current_time={current_time}")
        if expires_at < current_time:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired",
            )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user ID in session",
        )

    print(f"DEBUG: Returning user_id: {user_id}")

    # Better Auth uses custom string IDs, not UUIDs
    return user_id


def verify_user_authorization(
    url_user_id: str, token_user_id: str = Depends(get_current_user_id)
) -> str:
    """Verify that URL user_id matches authenticated user_id."""
    if url_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )
    return token_user_id
