from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.database_url_async,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Create declarative base
Base = declarative_base()


async def get_async_session() -> AsyncSession:
    """Get async database session."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()