from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, create_refresh_token, verify_password, get_password_hash
from app.db.session import get_async_session
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RefreshTokenRequest,
    ChangePasswordRequest,
)
from app.schemas.user import User, UserCreate

router = APIRouter()
security = HTTPBearer()


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """Login endpoint."""
    # TODO: Implement user authentication
    # This is a placeholder implementation
    
    # For now, return a mock response
    if login_data.email == "admin@groundedcounselling.com" and login_data.password == "admin":
        mock_user = User(
            id="mock-user-id",
            email=login_data.email,
            first_name="Admin",
            last_name="User",
            role="admin",
            phone=None,
            is_active=True,
            is_verified=True,
            is_2fa_enabled=False,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
            last_login_at=None,
        )
        
        access_token = create_access_token({"sub": mock_user.id, "email": mock_user.email})
        refresh_token = create_refresh_token({"sub": mock_user.id, "email": mock_user.email})
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=mock_user,
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )


@router.post("/register", response_model=User)
async def register(
    user_data: RegisterRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """Registration endpoint."""
    # TODO: Implement user registration
    # This is a placeholder implementation
    
    # Mock user creation
    mock_user = User(
        id="mock-new-user-id",
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role="patient",
        phone=user_data.phone,
        is_active=True,
        is_verified=False,
        is_2fa_enabled=False,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        last_login_at=None,
    )
    
    return mock_user


@router.post("/refresh")
async def refresh_token(
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """Refresh token endpoint."""
    # TODO: Implement token refresh
    # This is a placeholder implementation
    
    # Mock token refresh
    new_access_token = create_access_token({"sub": "mock-user-id", "email": "user@example.com"})
    new_refresh_token = create_refresh_token({"sub": "mock-user-id", "email": "user@example.com"})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Logout endpoint."""
    # TODO: Implement token blacklisting
    # This is a placeholder implementation
    
    return {"message": "Successfully logged out"}


@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Change password endpoint."""
    # TODO: Implement password change
    # This is a placeholder implementation
    
    return {"message": "Password changed successfully"}