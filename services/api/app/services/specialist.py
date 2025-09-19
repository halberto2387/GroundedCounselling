"""
Specialist service for CRUD operations.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, and_, or_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.specialist import Specialist
from app.models.user import User
from app.schemas.specialist import SpecialistCreate, SpecialistUpdate


class SpecialistService:
    """Service class for specialist CRUD operations."""

    @staticmethod
    async def create_specialist(
        db: AsyncSession, specialist_data: SpecialistCreate, user_id: UUID
    ) -> Specialist:
        """Create a new specialist profile for a user."""
        # Check if user already has a specialist profile
        existing = await SpecialistService.get_specialist_by_user_id(db, user_id)
        if existing:
            raise ValueError("User already has a specialist profile")

        specialist = Specialist(
            user_id=user_id,
            bio=specialist_data.bio,
            specializations=specialist_data.specializations,
            hourly_rate=specialist_data.hourly_rate,
            is_available=specialist_data.is_available,
            years_experience=specialist_data.years_experience,
            license_number=getattr(specialist_data, 'license_number', None),
        )
        
        db.add(specialist)
        await db.commit()
        await db.refresh(specialist)
        return specialist

    @staticmethod
    async def get_specialist(db: AsyncSession, specialist_id: UUID) -> Optional[Specialist]:
        """Get specialist by ID with user details."""
        result = await db.execute(
            select(Specialist)
            .options(selectinload(Specialist.user))
            .where(Specialist.id == specialist_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_specialist_by_user_id(db: AsyncSession, user_id: UUID) -> Optional[Specialist]:
        """Get specialist by user ID."""
        result = await db.execute(
            select(Specialist)
            .options(selectinload(Specialist.user))
            .where(Specialist.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_specialists(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        is_available: Optional[bool] = None,
        specializations: Optional[List[str]] = None,
    ) -> List[Specialist]:
        """Get list of specialists with optional filtering."""
        query = select(Specialist).options(selectinload(Specialist.user))
        
        conditions = []
        if is_available is not None:
            conditions.append(Specialist.is_available == is_available)
        
        if specializations:
            # Portable filtering for list/JSON stored specializations.
            # Strategy:
            # 1. Try Postgres ARRAY overlap operator if available (dialect name check at runtime).
            # 2. Fallback: OR group of LIKE matches on JSON/text representation for SQLite and others.
            dialect_name = getattr(db.bind.dialect, 'name', '') if db.bind else ''
            if dialect_name == 'postgresql':
                # Use native overlap for efficiency
                conditions.append(Specialist.specializations.op('&&')(specializations))
            else:
                like_clauses = []
                # JSON/text serialization of list typically like: ["anxiety", "stress"]
                # We wrap with quotes to reduce false positives (e.g., "art" in "heart").
                for spec in specializations:
                    pattern = f'%"{spec}"%'
                    like_clauses.append(Specialist.specializations.cast(text('TEXT')).like(pattern))
                if like_clauses:
                    conditions.append(or_(*like_clauses))
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.offset(skip).limit(limit).order_by(Specialist.created_at.desc())
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_specialist(
        db: AsyncSession, specialist_id: UUID, specialist_data: SpecialistUpdate
    ) -> Optional[Specialist]:
        """Update specialist information."""
        specialist = await SpecialistService.get_specialist(db, specialist_id)
        if not specialist:
            return None

        update_data = specialist_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(specialist, field, value)

        await db.commit()
        await db.refresh(specialist)
        return specialist

    @staticmethod
    async def delete_specialist(db: AsyncSession, specialist_id: UUID) -> bool:
        """Delete specialist profile."""
        specialist = await SpecialistService.get_specialist(db, specialist_id)
        if not specialist:
            return False

        await db.delete(specialist)
        await db.commit()
        return True

    @staticmethod
    async def toggle_availability(
        db: AsyncSession, specialist_id: UUID, is_available: bool
    ) -> Optional[Specialist]:
        """Toggle specialist availability status."""
        specialist = await SpecialistService.get_specialist(db, specialist_id)
        if not specialist:
            return None

        specialist.is_available = is_available
        await db.commit()
        await db.refresh(specialist)
        return specialist