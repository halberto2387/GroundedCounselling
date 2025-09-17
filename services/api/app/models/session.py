from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class SessionStatus(str, Enum):
    """Session status options."""
    
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Session(Base):
    """Session model for tracking actual counselling sessions."""
    
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), unique=True, nullable=False)
    
    # Session details
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.SCHEDULED, nullable=False)
    
    # Session notes and outcomes
    counsellor_notes = Column(Text, nullable=True)
    client_feedback = Column(Text, nullable=True)
    session_summary = Column(Text, nullable=True)
    
    # Video/Recording details
    video_room_id = Column(String(255), nullable=True)  # Jitsi room ID
    recording_url = Column(String(500), nullable=True)
    recording_consent = Column(Boolean, default=False, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    booking = relationship("Booking", back_populates="session")
    
    def __repr__(self) -> str:
        return f"<Session(id={self.id}, booking_id={self.booking_id}, status={self.status})>"
    
    @property
    def duration_minutes(self) -> int | None:
        """Calculate session duration in minutes."""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() // 60)
        return None