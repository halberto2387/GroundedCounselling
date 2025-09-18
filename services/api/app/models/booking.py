from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.specialist import Specialist
    from app.models.session import Session


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    specialist_id: Mapped[int] = mapped_column(ForeignKey("specialists.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    status: Mapped[BookingStatus] = mapped_column(String(20), default=BookingStatus.PENDING)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    patient: Mapped["User"] = relationship("User", back_populates="patient_bookings", foreign_keys=[patient_id])
    specialist: Mapped["Specialist"] = relationship("Specialist", back_populates="bookings")
    session: Mapped[Optional["Session"]] = relationship("Session", back_populates="booking", uselist=False)