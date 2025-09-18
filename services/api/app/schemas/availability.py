from datetime import datetime, time
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from app.models.availability import DayOfWeek


class AvailabilityBase(BaseModel):
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    is_available: bool = True


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityUpdate(BaseModel):
    day_of_week: DayOfWeek | None = None
    start_time: time | None = None
    end_time: time | None = None
    is_available: bool | None = None


class AvailabilityOut(AvailabilityBase):
    id: UUID
    specialist_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BulkAvailabilityCreate(BaseModel):
    """Create multiple availability slots for a specialist"""
    availabilities: List[AvailabilityCreate]


class AvailableSlot(BaseModel):
    """Available time slot for booking"""
    start_time: datetime
    end_time: datetime
    duration_minutes: int


class WeeklySchedule(BaseModel):
    """Weekly schedule for a specialist"""
    specialist_id: UUID
    monday: List[AvailabilityOut] = Field(default_factory=list)
    tuesday: List[AvailabilityOut] = Field(default_factory=list)
    wednesday: List[AvailabilityOut] = Field(default_factory=list)
    thursday: List[AvailabilityOut] = Field(default_factory=list)
    friday: List[AvailabilityOut] = Field(default_factory=list)
    saturday: List[AvailabilityOut] = Field(default_factory=list)
    sunday: List[AvailabilityOut] = Field(default_factory=list)