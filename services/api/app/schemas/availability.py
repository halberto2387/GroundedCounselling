from datetime import datetime, time
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from app.models.availability import DayOfWeek


class AvailabilityBase(BaseModel):
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    is_active: bool = True


class AvailabilityCreate(AvailabilityBase):
    specialist_id: int


class AvailabilityUpdate(BaseModel):
    start_time: time | None = None
    end_time: time | None = None
    is_active: bool | None = None


class AvailabilityOut(AvailabilityBase):
    id: int
    specialist_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AvailabilityBulkCreate(BaseModel):
    """Create multiple availability slots for a specialist"""
    specialist_id: int
    availabilities: List[AvailabilityBase]


class WeeklySchedule(BaseModel):
    """Weekly schedule for a specialist"""
    specialist_id: int
    monday: List[AvailabilityOut] = Field(default_factory=list)
    tuesday: List[AvailabilityOut] = Field(default_factory=list)
    wednesday: List[AvailabilityOut] = Field(default_factory=list)
    thursday: List[AvailabilityOut] = Field(default_factory=list)
    friday: List[AvailabilityOut] = Field(default_factory=list)
    saturday: List[AvailabilityOut] = Field(default_factory=list)
    sunday: List[AvailabilityOut] = Field(default_factory=list)