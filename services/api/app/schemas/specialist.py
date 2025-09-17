from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.schemas.user import User


class SpecialistBase(BaseModel):
    """Base specialist schema."""
    
    bio: Optional[str] = None
    specializations: List[str] = []
    credentials: List[str] = []
    languages: List[str] = ["English"]
    hourly_rate: Decimal
    is_available: bool = True
    is_accepting_new_clients: bool = True
    years_experience: Optional[int] = None
    license_number: Optional[str] = None
    license_state: Optional[str] = None
    education: Optional[str] = None


class SpecialistCreate(SpecialistBase):
    """Schema for creating a specialist profile."""
    
    pass


class SpecialistUpdate(BaseModel):
    """Schema for updating a specialist profile."""
    
    bio: Optional[str] = None
    specializations: Optional[List[str]] = None
    credentials: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    hourly_rate: Optional[Decimal] = None
    is_available: Optional[bool] = None
    is_accepting_new_clients: Optional[bool] = None
    years_experience: Optional[int] = None
    license_number: Optional[str] = None
    license_state: Optional[str] = None
    education: Optional[str] = None


class SpecialistInDB(SpecialistBase):
    """Specialist schema with database fields."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    user_id: str
    total_sessions: int
    average_rating: Optional[Decimal] = None
    total_reviews: int
    created_at: datetime
    updated_at: datetime


class Specialist(SpecialistInDB):
    """Public specialist schema."""
    
    user: User
    display_name: str


class SpecialistList(BaseModel):
    """Schema for listing specialists."""
    
    id: str
    display_name: str
    bio: Optional[str] = None
    specializations: List[str]
    hourly_rate: Decimal
    years_experience: Optional[int] = None
    average_rating: Optional[Decimal] = None
    total_reviews: int
    is_available: bool
    is_accepting_new_clients: bool