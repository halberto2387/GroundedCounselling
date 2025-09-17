from sqlalchemy import Column, DateTime, ForeignKey, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class AuditLog(Base):
    """Audit log model for tracking system actions."""
    
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Action details
    action = Column(String(100), nullable=False)  # e.g., "user.login", "booking.create"
    resource_type = Column(String(50), nullable=False)  # e.g., "User", "Booking"
    resource_id = Column(String(100), nullable=True)
    
    # Request details
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    
    # Data
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action={self.action}, user_id={self.user_id})>"