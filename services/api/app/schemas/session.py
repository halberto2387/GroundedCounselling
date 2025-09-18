from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.models.session import SessionStatus


class SessionBase(BaseModel):
    notes: Optional[str] = None
    recording_url: Optional[str] = None
    is_recorded: bool = False
    session_summary: Optional[str] = None


class SessionCreate(SessionBase):
    booking_id: UUID


class SessionUpdate(BaseModel):
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None
    status: Optional[SessionStatus] = None
    notes: Optional[str] = None
    recording_url: Optional[str] = None
    is_recorded: Optional[bool] = None
    session_summary: Optional[str] = None


class SessionOut(SessionBase):
    id: UUID
    booking_id: UUID
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SessionWithBooking(SessionOut):
    """Session with booking details"""
    booking_start_time: Optional[datetime] = None
    booking_duration_minutes: Optional[int] = None
    patient_id: Optional[UUID] = None
    specialist_id: Optional[UUID] = None