# Import all models here to ensure they are registered with SQLAlchemy
from app.db.session import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.specialist import Specialist  # noqa: F401
from app.models.booking import Booking  # noqa: F401
from app.models.session import Session  # noqa: F401
from app.models.availability import Availability  # noqa: F401
from app.models.audit_log import AuditLog  # noqa: F401

# Export Base for Alembic
__all__ = ["Base"]