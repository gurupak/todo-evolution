"""Add target_completion_date column to task table."""

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

from src.todo_api.config import settings


async def add_target_completion_date():
    """Add target_completion_date column to task table."""
    engine = create_async_engine(settings.database_url, echo=True)

    async with engine.begin() as conn:
        # Add target_completion_date column
        await conn.execute(
            text(
                """
            ALTER TABLE task
            ADD COLUMN IF NOT EXISTS target_completion_date TIMESTAMP
            """
            )
        )
        print("✅ Added target_completion_date column to task table")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(add_target_completion_date())
