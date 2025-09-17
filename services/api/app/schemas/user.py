from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict

from app.core.rbac import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.PATIENT


class UserCreate(UserBase):
    """Schema for creating a user."""
    
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserInDB(UserBase):
    """User schema with database fields."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    is_active: bool
    is_verified: bool
    is_2fa_enabled: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None


class User(UserInDB):
    """Public user schema."""
    
    pass


class UserProfile(User):
    """Extended user profile schema."""
    
    # Computed fields
    full_name: str
    is_specialist: bool
    is_admin: bool