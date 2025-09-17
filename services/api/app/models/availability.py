from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class Availability(Base):
    """Specialist availability model."""
    
    __tablename__ = "availability"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    specialist_id = Column(UUID(as_uuid=True), ForeignKey("specialists.id"), nullable=False)
    
    # Schedule details
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Settings
    is_active = Column(Boolean, default=True, nullable=False)
    is_recurring = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    specialist = relationship("Specialist", back_populates="availability_slots")
    
    def __repr__(self) -> str:
        return f"<Availability(specialist_id={self.specialist_id}, day={self.day_of_week}, time={self.start_time}-{self.end_time})>"