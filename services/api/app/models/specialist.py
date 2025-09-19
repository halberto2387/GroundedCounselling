from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, Integer, Text, Boolean, ForeignKey, DECIMAL, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.booking import Booking
    from app.models.availability import Availability


class Specialist(Base):
    __tablename__ = "specialists"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    hourly_rate: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    license_number: Mapped[str] = mapped_column(String(100), nullable=True)
    years_experience: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="specialist")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="specialist")
    availabilities: Mapped[List["Availability"]] = relationship("Availability", back_populates="specialist")

    # Dynamic access to specialization slugs via association table; returns list[str]
    @hybrid_property
    def specializations(self):  # type: ignore
        # This property is for runtime attribute-style access (not used in queries now)
        if not hasattr(self, '_specialization_slugs_cache'):
            # Lazy load via relationship if defined later; placeholder empty list
            return []
        return getattr(self, '_specialization_slugs_cache')