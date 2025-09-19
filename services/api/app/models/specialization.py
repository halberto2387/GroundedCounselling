from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Specialization(Base):
    __tablename__ = 'specializations'

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SpecialistSpecialization(Base):
    __tablename__ = 'specialist_specializations'

    specialist_id: Mapped[int] = mapped_column(primary_key=True)
    specialization_id: Mapped[int] = mapped_column(primary_key=True)
    # Composite PK gives implicit index; add separate index if query patterns expand.