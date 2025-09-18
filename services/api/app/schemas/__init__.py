from .user import UserCreate, UserOut
from .specialist import (
    SpecialistCreate,
    SpecialistUpdate,
    SpecialistOut,
    SpecialistProfile,
)
from .booking import (
    BookingCreate,
    BookingUpdate,
    BookingOut,
    BookingWithDetails,
)
from .session import (
    SessionCreate,
    SessionUpdate,
    SessionOut,
    SessionWithBooking,
)
from .availability import (
    AvailabilityCreate,
    AvailabilityUpdate,
    AvailabilityOut,
    AvailabilityBulkCreate,
    WeeklySchedule,
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserOut",
    # Specialist schemas
    "SpecialistCreate",
    "SpecialistUpdate",
    "SpecialistOut",
    "SpecialistProfile",
    # Booking schemas
    "BookingCreate",
    "BookingUpdate",
    "BookingOut",
    "BookingWithDetails",
    # Session schemas
    "SessionCreate",
    "SessionUpdate",
    "SessionOut",
    "SessionWithBooking",
    # Availability schemas
    "AvailabilityCreate",
    "AvailabilityUpdate",
    "AvailabilityOut",
    "AvailabilityBulkCreate",
    "WeeklySchedule",
]