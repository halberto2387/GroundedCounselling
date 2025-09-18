from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class SpecialistBase(BaseModel):
    bio: Optional[str] = None
    specializations: List[str] = Field(default_factory=list)
    hourly_rate: Optional[float] = Field(None, ge=0, description="Hourly rate in USD")
    is_available: bool = True
    years_experience: Optional[int] = Field(None, ge=0)
    education: Optional[str] = None
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)


class SpecialistCreate(SpecialistBase):
    pass  # user_id is passed separately to the service method


class SpecialistUpdate(BaseModel):
    bio: Optional[str] = None
    specializations: Optional[List[str]] = None
    hourly_rate: Optional[float] = Field(None, ge=0)
    is_available: Optional[bool] = None
    years_experience: Optional[int] = Field(None, ge=0)
    education: Optional[str] = None
    certifications: Optional[List[str]] = None
    languages: Optional[List[str]] = None


class SpecialistOut(SpecialistBase):
    id: int
    user_id: int
    license_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SpecialistProfile(SpecialistOut):
    """Extended specialist profile with user info"""
    user_email: Optional[str] = None
    user_role: Optional[str] = None