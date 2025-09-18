from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.booking import BookingStatus


class BookingBase(BaseModel):
    start_time: datetime
    duration_minutes: int = Field(default=60, ge=15, le=480, description="Duration in minutes (15 min to 8 hours)")
    notes: Optional[str] = None


class BookingCreate(BookingBase):
    specialist_id: int


class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=15, le=480)
    notes: Optional[str] = None
    status: Optional[BookingStatus] = None
    cancellation_reason: Optional[str] = None


class BookingOut(BookingBase):
    id: int
    patient_id: int
    specialist_id: int
    status: BookingStatus
    cancellation_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BookingWithDetails(BookingOut):
    """Booking with patient and specialist details"""
    patient_email: Optional[str] = None
    specialist_bio: Optional[str] = None
    specialist_license_number: Optional[str] = None