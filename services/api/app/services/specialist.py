"""
Specialist service for CRUD operations.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, and_, or_, text, func, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.specialist import Specialist
from app.models.specialization import Specialization, SpecialistSpecialization
from app.services.cache.specialization_cache import bulk_normalize
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
            specializations=specialist_data.specializations,  # legacy mirror
            hourly_rate=specialist_data.hourly_rate,
            is_available=specialist_data.is_available,
            years_experience=specialist_data.years_experience,
            license_number=getattr(specialist_data, 'license_number', None),
        )
        db.add(specialist)
        await db.flush()
        # Associate specializations via normalized slugs
        await SpecialistService._sync_specializations(db, specialist, specialist_data.specializations)
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
            # Prefer association join if tables exist
            assoc_exists = await SpecialistService._association_tables_present(db)
            if assoc_exists:
                norm_specs = bulk_normalize(specializations)
                query = query.join(
                    SpecialistSpecialization,
                    SpecialistSpecialization.specialist_id == Specialist.id,
                ).join(
                    Specialization,
                    Specialization.id == SpecialistSpecialization.specialization_id,
                ).where(Specialization.slug.in_(norm_specs))
            else:
                # Fallback to existing JSON-based strategy
                dialect_name = getattr(db.bind.dialect, 'name', '') if db.bind else ''
                if dialect_name == 'postgresql':
                    conditions.append(Specialist.specializations.op('&&')(specializations))
                else:
                    like_clauses = []
                    for spec in specializations:
                        lowered_column = func.lower(Specialist.specializations.cast(text('TEXT')))
                        pattern = f'%"{spec.lower()}"%'
                        like_clauses.append(lowered_column.like(pattern))
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

        # Sync associations if specializations provided
        if 'specializations' in update_data:
            await SpecialistService._sync_specializations(db, specialist, update_data['specializations'])
            # Mirror legacy JSON field
            specialist.specializations = update_data['specializations']

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

    # ---- Internal helpers ----
    @staticmethod
    async def _association_tables_present(db: AsyncSession) -> bool:
        inspector = db.bind.dialect.get_inspector(db.bind)
        tables = inspector.get_table_names()
        return 'specializations' in tables and 'specialist_specializations' in tables

    @staticmethod
    async def _sync_specializations(db: AsyncSession, specialist: Specialist, specs: Optional[List[str]]):
        if specs is None:
            return
        norm_specs = bulk_normalize(specs)
        # Fetch existing specializations
        existing_rows = (await db.execute(select(Specialization).where(Specialization.slug.in_(norm_specs)))).scalars().all()
        existing_by_slug = {r.slug: r for r in existing_rows}
        to_create = [s for s in norm_specs if s not in existing_by_slug]
        for slug in to_create:
            db.add(Specialization(slug=slug, display_name=slug.title()))
        if to_create:
            await db.flush()
            new_rows = (await db.execute(select(Specialization).where(Specialization.slug.in_(to_create)))).scalars().all()
            for r in new_rows:
                existing_by_slug[r.slug] = r

        # Current associations
        current_assoc = (await db.execute(select(SpecialistSpecialization).where(SpecialistSpecialization.specialist_id == specialist.id))).scalars().all()
        current_ids = {a.specialization_id for a in current_assoc}
        desired_ids = {existing_by_slug[s].id for s in norm_specs}
        add_ids = desired_ids - current_ids
        remove_ids = current_ids - desired_ids

        for sid in add_ids:
            db.add(SpecialistSpecialization(specialist_id=specialist.id, specialization_id=sid))
        if remove_ids:
            await db.execute(
                delete(SpecialistSpecialization).where(
                    SpecialistSpecialization.specialist_id == specialist.id,
                    SpecialistSpecialization.specialization_id.in_(remove_ids)
                )
            )