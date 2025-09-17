from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.rbac import UserRole
from app.db.session import Base


class User(Base):
    """User model for authentication and basic profile."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    
    # Role and permissions
    role = Column(Enum(UserRole), default=UserRole.PATIENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # 2FA
    is_2fa_enabled = Column(Boolean, default=False, nullable=False)
    totp_secret = Column(String(32), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    specialist_profile = relationship("Specialist", back_populates="user", uselist=False)
    bookings_as_client = relationship("Booking", foreign_keys="[Booking.client_id]", back_populates="client")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
    
    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property 
    def is_specialist(self) -> bool:
        """Check if user is a specialist."""
        return self.role in (UserRole.COUNSELLOR, UserRole.ADMIN, UserRole.SUPER_ADMIN)
    
    @property
    def is_admin(self) -> bool:
        """Check if user is an admin.""" 
        return self.role in (UserRole.ADMIN, UserRole.SUPER_ADMIN)