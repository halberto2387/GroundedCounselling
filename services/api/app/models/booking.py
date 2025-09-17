from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class BookingStatus(str, Enum):
    """Booking status options."""
    
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class Booking(Base):
    """Booking model for counselling sessions."""
    
    __tablename__ = "bookings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Relationships
    client_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    specialist_id = Column(UUID(as_uuid=True), ForeignKey("specialists.id"), nullable=False)
    
    # Scheduling
    start_time = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=60, nullable=False)
    
    # Status and notes
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING, nullable=False)
    client_notes = Column(Text, nullable=True)
    specialist_notes = Column(Text, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    
    # Pricing
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    total_cost = Column(Numeric(10, 2), nullable=False)
    
    # Payment tracking
    payment_intent_id = Column(String(255), nullable=True)  # Stripe payment intent
    is_paid = Column(Boolean, default=False, nullable=False)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    confirmed_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    client = relationship("User", foreign_keys=[client_id], back_populates="bookings_as_client")
    specialist = relationship("Specialist", back_populates="bookings")
    session = relationship("Session", back_populates="booking", uselist=False)
    
    def __repr__(self) -> str:
        return f"<Booking(id={self.id}, status={self.status}, start_time={self.start_time})>"
    
    @property
    def end_time(self) -> datetime:
        """Calculate the end time of the booking."""
        from datetime import timedelta
        return self.start_time + timedelta(minutes=self.duration_minutes)
    
    @property
    def is_active(self) -> bool:
        """Check if the booking is active (confirmed and not completed/cancelled)."""
        return self.status == BookingStatus.CONFIRMED
    
    @property 
    def can_be_cancelled(self) -> bool:
        """Check if the booking can be cancelled."""
        return self.status in (BookingStatus.PENDING, BookingStatus.CONFIRMED)