"""
Authentication dependencies and utilities.
"""

from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.user import User
from app.models.specialist import Specialist


async def get_current_user(
    x_user_id: Optional[str] = Header(None),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Get current user from X-User-ID header.
    This is a simplified auth system for demo purposes.
    """
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-ID header required"
        )
    
    try:
        user_id = UUID(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format"
        )
    
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


async def get_current_specialist(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Specialist:
    """Get current user's specialist profile."""
    result = await session.execute(
        select(Specialist).where(Specialist.user_id == current_user.id)
    )
    specialist = result.scalar_one_or_none()
    
    if not specialist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a specialist"
        )
    
    return specialist


def require_specialist_ownership(
    specialist_id: UUID,
    current_specialist: Specialist = Depends(get_current_specialist)
) -> None:
    """Ensure current specialist owns the resource."""
    if current_specialist.id != specialist_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )


def require_user_ownership(
    user_id: UUID,
    current_user: User = Depends(get_current_user)
) -> None:
    """Ensure current user owns the resource."""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )