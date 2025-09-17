from datetime import datetime
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.booking import BookingStatus
from app.schemas.user import User
from app.schemas.specialist import Specialist


class BookingBase(BaseModel):
    """Base booking schema."""
    
    specialist_id: str
    start_time: datetime
    duration_minutes: int = 60
    client_notes: Optional[str] = None


class BookingCreate(BookingBase):
    """Schema for creating a booking."""
    
    pass


class BookingUpdate(BaseModel):
    """Schema for updating a booking."""
    
    start_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    client_notes: Optional[str] = None
    specialist_notes: Optional[str] = None
    status: Optional[BookingStatus] = None
    cancellation_reason: Optional[str] = None


class BookingInDB(BookingBase):
    """Booking schema with database fields."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    client_id: str
    status: BookingStatus
    specialist_notes: Optional[str] = None
    cancellation_reason: Optional[str] = None
    hourly_rate: Decimal
    total_cost: Decimal
    payment_intent_id: Optional[str] = None
    is_paid: bool
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    confirmed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None


class Booking(BookingInDB):
    """Public booking schema."""
    
    client: Optional[User] = None
    specialist: Optional[Specialist] = None
    end_time: datetime
    is_active: bool
    can_be_cancelled: bool


class BookingList(BaseModel):
    """Schema for listing bookings."""
    
    id: str
    start_time: datetime
    duration_minutes: int
    status: BookingStatus
    total_cost: Decimal
    is_paid: bool
    specialist_name: str
    client_name: Optional[str] = None