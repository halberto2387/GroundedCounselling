"""
Availability service for CRUD operations.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime, date, time, timedelta
from sqlalchemy import select, and_, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.availability import Availability, DayOfWeek
from app.models.specialist import Specialist
from app.schemas.availability import AvailabilityCreate, AvailabilityUpdate


class AvailabilityService:
    """Service class for availability CRUD operations."""

    @staticmethod
    async def create_availability(
        db: AsyncSession, availability_data: AvailabilityCreate, specialist_id: UUID
    ) -> Availability:
        """Create a new availability slot."""
        # Validate specialist exists
        specialist = await db.get(Specialist, specialist_id)
        if not specialist:
            raise ValueError("Specialist not found")

        # Check for overlapping availability
        conflicts = await AvailabilityService._check_availability_conflicts(
            db, specialist_id, availability_data.day_of_week, 
            availability_data.start_time, availability_data.end_time
        )
        if conflicts:
            raise ValueError("Availability slot conflicts with existing availability")

        availability = Availability(
            specialist_id=specialist_id,
            day_of_week=availability_data.day_of_week,
            start_time=availability_data.start_time,
            end_time=availability_data.end_time,
            is_available=availability_data.is_available,
        )
        
        db.add(availability)
        await db.commit()
        await db.refresh(availability)
        return availability

    @staticmethod
    async def get_availability(
        db: AsyncSession, availability_id: UUID
    ) -> Optional[Availability]:
        """Get availability by ID."""
        return await db.get(Availability, availability_id)

    @staticmethod
    async def get_specialist_availability(
        db: AsyncSession,
        specialist_id: UUID,
        day_of_week: Optional[DayOfWeek] = None,
        is_available: Optional[bool] = None,
    ) -> List[Availability]:
        """Get availability slots for a specialist."""
        query = select(Availability).where(Availability.specialist_id == specialist_id)
        
        conditions = []
        if day_of_week is not None:
            conditions.append(Availability.day_of_week == day_of_week)
        if is_available is not None:
            conditions.append(Availability.is_available == is_available)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.order_by(Availability.day_of_week, Availability.start_time)
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_available_slots(
        db: AsyncSession,
        specialist_id: UUID,
        target_date: date,
        duration_minutes: int = 60,
    ) -> List[datetime]:
        """Get available time slots for a specific date."""
        day_of_week = DayOfWeek(target_date.weekday())
        
        # Get availability for the day
        availabilities = await AvailabilityService.get_specialist_availability(
            db, specialist_id, day_of_week, is_available=True
        )
        
        if not availabilities:
            return []

        # Import here to avoid circular imports
        from app.models.booking import Booking, BookingStatus
        
        # Get existing bookings for the date
        start_of_day = datetime.combine(target_date, time.min)
        end_of_day = datetime.combine(target_date, time.max)
        
        bookings = await db.execute(
            select(Booking)
            .where(
                and_(
                    Booking.specialist_id == specialist_id,
                    Booking.start_time >= start_of_day,
                    Booking.start_time <= end_of_day,
                    Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
                )
            )
        )
        existing_bookings = bookings.scalars().all()

        available_slots = []
        
        for availability in availabilities:
            # Generate time slots within availability window
            slot_start = datetime.combine(target_date, availability.start_time)
            slot_end = datetime.combine(target_date, availability.end_time)
            
            current_slot = slot_start
            while current_slot + timedelta(minutes=duration_minutes) <= slot_end:
                slot_finish = current_slot + timedelta(minutes=duration_minutes)
                
                # Check if this slot conflicts with existing bookings
                is_conflicted = any(
                    AvailabilityService._times_overlap(
                        current_slot, slot_finish,
                        booking.start_time, 
                        booking.start_time + timedelta(minutes=booking.duration_minutes)
                    )
                    for booking in existing_bookings
                )
                
                if not is_conflicted:
                    available_slots.append(current_slot)
                
                # Move to next slot (15-minute intervals)
                current_slot += timedelta(minutes=15)
        
        return sorted(available_slots)

    @staticmethod
    async def update_availability(
        db: AsyncSession, availability_id: UUID, availability_data: AvailabilityUpdate
    ) -> Optional[Availability]:
        """Update availability information."""
        availability = await AvailabilityService.get_availability(db, availability_id)
        if not availability:
            return None

        # Check for conflicts if time is being updated
        if (availability_data.day_of_week is not None or 
            availability_data.start_time is not None or 
            availability_data.end_time is not None):
            
            new_day = availability_data.day_of_week or availability.day_of_week
            new_start = availability_data.start_time or availability.start_time
            new_end = availability_data.end_time or availability.end_time
            
            conflicts = await AvailabilityService._check_availability_conflicts(
                db, availability.specialist_id, new_day, new_start, new_end,
                exclude_availability_id=availability_id
            )
            if conflicts:
                raise ValueError("Updated availability conflicts with existing availability")

        update_data = availability_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(availability, field, value)

        await db.commit()
        await db.refresh(availability)
        return availability

    @staticmethod
    async def delete_availability(db: AsyncSession, availability_id: UUID) -> bool:
        """Delete availability slot."""
        availability = await AvailabilityService.get_availability(db, availability_id)
        if not availability:
            return False

        await db.delete(availability)
        await db.commit()
        return True

    @staticmethod
    async def bulk_create_availability(
        db: AsyncSession, 
        specialist_id: UUID, 
        availabilities: List[AvailabilityCreate]
    ) -> List[Availability]:
        """Create multiple availability slots at once."""
        # Validate specialist exists
        specialist = await db.get(Specialist, specialist_id)
        if not specialist:
            raise ValueError("Specialist not found")

        created_availabilities = []
        for availability_data in availabilities:
            # Check for conflicts
            conflicts = await AvailabilityService._check_availability_conflicts(
                db, specialist_id, availability_data.day_of_week,
                availability_data.start_time, availability_data.end_time
            )
            if conflicts:
                raise ValueError(
                    f"Availability slot for {availability_data.day_of_week} "
                    f"{availability_data.start_time}-{availability_data.end_time} conflicts"
                )

            availability = Availability(
                specialist_id=specialist_id,
                day_of_week=availability_data.day_of_week,
                start_time=availability_data.start_time,
                end_time=availability_data.end_time,
                is_available=availability_data.is_available,
            )
            db.add(availability)
            created_availabilities.append(availability)

        await db.commit()
        for availability in created_availabilities:
            await db.refresh(availability)
        
        return created_availabilities

    @staticmethod
    async def clear_specialist_availability(
        db: AsyncSession, specialist_id: UUID
    ) -> int:
        """Clear all availability for a specialist."""
        result = await db.execute(
            delete(Availability).where(Availability.specialist_id == specialist_id)
        )
        await db.commit()
        return result.rowcount

    @staticmethod
    async def _check_availability_conflicts(
        db: AsyncSession,
        specialist_id: UUID,
        day_of_week: DayOfWeek,
        start_time: time,
        end_time: time,
        exclude_availability_id: Optional[UUID] = None,
    ) -> List[Availability]:
        """Check for conflicting availability slots."""
        query = (
            select(Availability)
            .where(
                and_(
                    Availability.specialist_id == specialist_id,
                    Availability.day_of_week == day_of_week,
                    or_(
                        # New slot starts during existing slot
                        and_(
                            Availability.start_time <= start_time,
                            start_time < Availability.end_time
                        ),
                        # New slot ends during existing slot
                        and_(
                            Availability.start_time < end_time,
                            end_time <= Availability.end_time
                        ),
                        # New slot encompasses existing slot
                        and_(
                            start_time <= Availability.start_time,
                            Availability.end_time <= end_time
                        )
                    )
                )
            )
        )
        
        if exclude_availability_id:
            query = query.where(Availability.id != exclude_availability_id)
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    def _times_overlap(
        start1: datetime, end1: datetime, start2: datetime, end2: datetime
    ) -> bool:
        """Check if two time ranges overlap."""
        return start1 < end2 and start2 < end1