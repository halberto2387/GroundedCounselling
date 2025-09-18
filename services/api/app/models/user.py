from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.specialist import Specialist
    from app.models.booking import Booking


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="patient")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    specialist: Mapped[Optional["Specialist"]] = relationship("Specialist", back_populates="user", uselist=False)
    patient_bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="patient", foreign_keys="Booking.patient_id")
