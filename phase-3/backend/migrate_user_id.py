"""Migration script to change task.user_id from UUID to VARCHAR."""

import asyncio
import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def migrate():
    # Get database URL from environment or use default
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_cZKLhPn1Bg4D@ep-hidden-queen-a4ld5opf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require",
    )

    # Remove sslmode from URL and convert to async URL
    database_url = database_url.replace("?sslmode=require", "").replace("&sslmode=require", "")
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

    # Add SSL parameter for asyncpg
    engine = create_async_engine(database_url, connect_args={"ssl": "require"})

    async with engine.begin() as conn:
        # Drop existing task table (development only!)
        print("Dropping task table...")
        await conn.execute(text("DROP TABLE IF EXISTS task CASCADE"))

        # Drop and create the priority enum type
        print("Creating PriorityEnum type...")
        await conn.execute(text("DROP TYPE IF EXISTS priorityenum CASCADE"))
        await conn.execute(text("CREATE TYPE priorityenum AS ENUM ('LOW', 'MEDIUM', 'HIGH')"))

        # Create new task table with VARCHAR user_id
        print("Creating task table with VARCHAR user_id...")
        await conn.execute(
            text("""
            CREATE TABLE task (
                id UUID PRIMARY KEY,
                user_id VARCHAR NOT NULL,
                title VARCHAR(200) NOT NULL,
                description VARCHAR(1000) DEFAULT '',
                priority priorityenum NOT NULL,
                is_completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                completed_at TIMESTAMP
            )
        """)
        )

        # Create index on user_id
        await conn.execute(text("CREATE INDEX ix_task_user_id ON task(user_id)"))

        print("✅ Migration complete!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(migrate())
