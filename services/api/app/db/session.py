from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator
import os

from app.core.config import settings


def get_database_url() -> str:
    # Check for runtime environment variables first (for testing)
    if "ASYNC_DATABASE_URL" in os.environ:
        return os.environ["ASYNC_DATABASE_URL"]
    if "DATABASE_URL" in os.environ:
        # Convert PostgreSQL to async if needed
        db_url = os.environ["DATABASE_URL"]
        if db_url.startswith("postgresql://"):
            return db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif db_url.startswith("sqlite://"):
            return db_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
        return db_url
    # Fall back to settings
    return settings.database_url


def get_engine():
    return create_async_engine(get_database_url(), pool_pre_ping=True)


def get_session_maker():
    return async_sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = get_session_maker()
    async with SessionLocal() as session:
        yield session
