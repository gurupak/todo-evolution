"""Async database engine and session factory."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .config import settings

# Import all models to ensure they are registered with SQLModel's metadata
from .models import Task, Conversation, Message  # noqa: F401

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycle connections every hour
    pool_size=5,
    max_overflow=10,
    connect_args={
        "prepared_statement_cache_size": 0,  # Disable prepared statement cache
        "statement_cache_size": 0,  # Disable statement cache
    },
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        yield session


async def create_db_and_tables() -> None:
    """Create database tables (for testing only)."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
