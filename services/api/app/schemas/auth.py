from pydantic import BaseModel

from app.schemas.user import User


class Token(BaseModel):
    """Token response schema."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    
    sub: str  # user ID
    email: str
    role: str


class LoginRequest(BaseModel):
    """Login request schema."""
    
    email: str
    password: str


class LoginResponse(BaseModel):
    """Login response schema."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: User


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    
    refresh_token: str


class RegisterRequest(BaseModel):
    """Registration request schema."""
    
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str | None = None


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""
    
    email: str


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema."""
    
    token: str
    new_password: str


class ChangePasswordRequest(BaseModel):
    """Change password request schema."""
    
    current_password: str
    new_password: str


class Enable2FAResponse(BaseModel):
    """Enable 2FA response schema."""
    
    secret: str
    qr_code_url: str


class Verify2FARequest(BaseModel):
    """Verify 2FA request schema."""
    
    token: str