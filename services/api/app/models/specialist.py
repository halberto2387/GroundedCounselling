from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class Specialist(Base):
    """Specialist/Counsellor profile model."""
    
    __tablename__ = "specialists"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    
    # Professional information
    bio = Column(Text, nullable=True)
    specializations = Column(ARRAY(String), default=[], nullable=False)
    credentials = Column(ARRAY(String), default=[], nullable=False)
    languages = Column(ARRAY(String), default=["English"], nullable=False)
    
    # Pricing and availability
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    is_accepting_new_clients = Column(Boolean, default=True, nullable=False)
    
    # Experience and ratings
    years_experience = Column(Integer, nullable=True)
    total_sessions = Column(Integer, default=0, nullable=False)
    average_rating = Column(Numeric(3, 2), nullable=True)
    total_reviews = Column(Integer, default=0, nullable=False)
    
    # Professional details
    license_number = Column(String(100), nullable=True)
    license_state = Column(String(50), nullable=True)
    education = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="specialist_profile")
    bookings = relationship("Booking", back_populates="specialist")
    availability_slots = relationship("Availability", back_populates="specialist")
    
    def __repr__(self) -> str:
        return f"<Specialist(id={self.id}, user_id={self.user_id})>"
    
    @property
    def display_name(self) -> str:
        """Get the specialist's display name."""
        if self.user:
            return self.user.full_name
        return "Unknown Specialist"