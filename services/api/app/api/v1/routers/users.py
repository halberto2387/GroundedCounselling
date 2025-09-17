from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.schemas.user import User, UserUpdate, UserProfile

router = APIRouter()
security = HTTPBearer()


@router.get("/me", response_model=UserProfile)
async def get_current_user(
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Get current user profile."""
    # TODO: Implement user retrieval from token
    # This is a placeholder implementation
    
    mock_user = UserProfile(
        id="mock-user-id",
        email="user@example.com",
        first_name="John",
        last_name="Doe",
        role="patient",
        phone="+1234567890",
        is_active=True,
        is_verified=True,
        is_2fa_enabled=False,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        last_login_at="2024-01-01T12:00:00Z",
        full_name="John Doe",
        is_specialist=False,
        is_admin=False,
    )
    
    return mock_user


@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Update current user profile."""
    # TODO: Implement user update
    # This is a placeholder implementation
    
    mock_user = User(
        id="mock-user-id",
        email="user@example.com",
        first_name=user_update.first_name or "John",
        last_name=user_update.last_name or "Doe",
        role="patient",
        phone=user_update.phone,
        is_active=True,
        is_verified=True,
        is_2fa_enabled=False,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        last_login_at="2024-01-01T12:00:00Z",
    )
    
    return mock_user


@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 20,
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Get users (admin only)."""
    # TODO: Implement user listing with permissions check
    # This is a placeholder implementation
    
    mock_users = [
        User(
            id=f"user-{i}",
            email=f"user{i}@example.com",
            first_name=f"User",
            last_name=f"{i}",
            role="patient",
            phone=None,
            is_active=True,
            is_verified=True,
            is_2fa_enabled=False,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
            last_login_at=None,
        )
        for i in range(skip, skip + min(limit, 10))
    ]
    
    return mock_users


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Get user by ID (admin only)."""
    # TODO: Implement user retrieval with permissions check
    # This is a placeholder implementation
    
    mock_user = User(
        id=user_id,
        email="user@example.com",
        first_name="John",
        last_name="Doe",
        role="patient",
        phone=None,
        is_active=True,
        is_verified=True,
        is_2fa_enabled=False,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        last_login_at=None,
    )
    
    return mock_user