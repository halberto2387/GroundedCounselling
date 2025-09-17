"""
Database configuration and session management.
"""

from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from .config import get_settings

settings = get_settings()

# Database engine
engine = create_async_engine(
    str(settings.DATABASE_URL) if settings.DATABASE_URL else "sqlite+aiosqlite:///./test.db",
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    poolclass=NullPool if "sqlite" in str(settings.DATABASE_URL or "") else None,
    echo=settings.DEBUG,
    future=True,
)

# Session factory
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base model with naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_database() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_database() -> None:
    """Close database connections."""
    await engine.dispose()