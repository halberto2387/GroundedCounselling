from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking


class SessionStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class Session(Base):
    __tablename__ = "sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), unique=True)
    actual_start_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[SessionStatus] = mapped_column(String(20), default=SessionStatus.SCHEDULED)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recording_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    session_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    booking: Mapped["Booking"] = relationship("Booking", back_populates="session")