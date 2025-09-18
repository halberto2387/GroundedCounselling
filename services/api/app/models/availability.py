from datetime import datetime, time
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, Time, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.specialist import Specialist


class DayOfWeek(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class Availability(Base):
    __tablename__ = "availabilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    specialist_id: Mapped[int] = mapped_column(ForeignKey("specialists.id"))
    day_of_week: Mapped[DayOfWeek] = mapped_column(String(10))
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    specialist: Mapped["Specialist"] = relationship("Specialist", back_populates="availabilities")