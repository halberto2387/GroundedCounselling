"""
Booking service for CRUD operations.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.booking import Booking, BookingStatus
from app.models.specialist import Specialist
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingUpdate


class BookingService:
    """Service class for booking CRUD operations."""

    @staticmethod
    async def create_booking(
        db: AsyncSession, booking_data: BookingCreate, patient_id: UUID
    ) -> Booking:
        """Create a new booking."""
        # Validate specialist exists
        specialist = await db.get(Specialist, booking_data.specialist_id)
        if not specialist:
            raise ValueError("Specialist not found")

        if not specialist.is_available:
            raise ValueError("Specialist is not currently available")

        # Check for conflicting bookings
        end_time = booking_data.start_time + timedelta(minutes=booking_data.duration_minutes)
        
        conflicts = await BookingService._check_booking_conflicts(
            db, booking_data.specialist_id, booking_data.start_time, end_time
        )
        if conflicts:
            raise ValueError("Time slot is not available")

        booking = Booking(
            patient_id=patient_id,
            specialist_id=booking_data.specialist_id,
            start_time=booking_data.start_time,
            duration_minutes=booking_data.duration_minutes,
            notes=booking_data.notes,
            status=BookingStatus.PENDING,
        )
        
        db.add(booking)
        await db.commit()
        await db.refresh(booking)
        return booking

    @staticmethod
    async def get_booking(db: AsyncSession, booking_id: UUID) -> Optional[Booking]:
        """Get booking by ID with related data."""
        result = await db.execute(
            select(Booking)
            .options(
                selectinload(Booking.patient),
                selectinload(Booking.specialist).selectinload(Specialist.user),
                selectinload(Booking.session)
            )
            .where(Booking.id == booking_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_bookings_for_patient(
        db: AsyncSession,
        patient_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[BookingStatus] = None,
    ) -> List[Booking]:
        """Get bookings for a specific patient."""
        query = (
            select(Booking)
            .options(
                selectinload(Booking.specialist).selectinload(Specialist.user),
                selectinload(Booking.session)
            )
            .where(Booking.patient_id == patient_id)
        )
        
        if status:
            query = query.where(Booking.status == status)
        
        query = query.offset(skip).limit(limit).order_by(Booking.start_time.desc())
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_bookings_for_specialist(
        db: AsyncSession,
        specialist_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[BookingStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Booking]:
        """Get bookings for a specific specialist."""
        query = (
            select(Booking)
            .options(
                selectinload(Booking.patient),
                selectinload(Booking.session)
            )
            .where(Booking.specialist_id == specialist_id)
        )
        
        conditions = []
        if status:
            conditions.append(Booking.status == status)
        if start_date:
            conditions.append(Booking.start_time >= start_date)
        if end_date:
            conditions.append(Booking.start_time <= end_date)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.offset(skip).limit(limit).order_by(Booking.start_time.asc())
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_booking(
        db: AsyncSession, booking_id: UUID, booking_data: BookingUpdate
    ) -> Optional[Booking]:
        """Update booking information."""
        booking = await BookingService.get_booking(db, booking_id)
        if not booking:
            return None

        # If updating time, check for conflicts
        if booking_data.start_time or booking_data.duration_minutes:
            new_start = booking_data.start_time or booking.start_time
            new_duration = booking_data.duration_minutes or booking.duration_minutes
            new_end = new_start + timedelta(minutes=new_duration)
            
            conflicts = await BookingService._check_booking_conflicts(
                db, booking.specialist_id, new_start, new_end, exclude_booking_id=booking_id
            )
            if conflicts:
                raise ValueError("New time slot is not available")

        update_data = booking_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(booking, field, value)

        await db.commit()
        await db.refresh(booking)
        return booking

    @staticmethod
    async def cancel_booking(db: AsyncSession, booking_id: UUID) -> Optional[Booking]:
        """Cancel a booking."""
        booking = await BookingService.get_booking(db, booking_id)
        if not booking:
            return None

        if booking.status in [BookingStatus.CANCELLED, BookingStatus.COMPLETED]:
            raise ValueError(f"Cannot cancel booking with status: {booking.status}")

        booking.status = BookingStatus.CANCELLED
        await db.commit()
        await db.refresh(booking)
        return booking

    @staticmethod
    async def confirm_booking(db: AsyncSession, booking_id: UUID) -> Optional[Booking]:
        """Confirm a pending booking."""
        booking = await BookingService.get_booking(db, booking_id)
        if not booking:
            return None

        if booking.status != BookingStatus.PENDING:
            raise ValueError(f"Can only confirm pending bookings, current status: {booking.status}")

        booking.status = BookingStatus.CONFIRMED
        await db.commit()
        await db.refresh(booking)
        return booking

    @staticmethod
    async def complete_booking(db: AsyncSession, booking_id: UUID) -> Optional[Booking]:
        """Mark a booking as completed."""
        booking = await BookingService.get_booking(db, booking_id)
        if not booking:
            return None

        if booking.status != BookingStatus.CONFIRMED:
            raise ValueError(f"Can only complete confirmed bookings, current status: {booking.status}")

        booking.status = BookingStatus.COMPLETED
        await db.commit()
        await db.refresh(booking)
        return booking

    @staticmethod
    async def _check_booking_conflicts(
        db: AsyncSession,
        specialist_id: UUID,
        start_time: datetime,
        end_time: datetime,
        exclude_booking_id: Optional[UUID] = None,
    ) -> List[Booking]:
        """Check for conflicting bookings in the given time range."""
        query = (
            select(Booking)
            .where(
                and_(
                    Booking.specialist_id == specialist_id,
                    Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
                    or_(
                        # New booking starts during existing booking
                        and_(
                            Booking.start_time <= start_time,
                            start_time < Booking.start_time + timedelta(minutes=Booking.duration_minutes)
                        ),
                        # New booking ends during existing booking
                        and_(
                            Booking.start_time < end_time,
                            end_time <= Booking.start_time + timedelta(minutes=Booking.duration_minutes)
                        ),
                        # New booking encompasses existing booking
                        and_(
                            start_time <= Booking.start_time,
                            Booking.start_time + timedelta(minutes=Booking.duration_minutes) <= end_time
                        )
                    )
                )
            )
        )
        
        if exclude_booking_id:
            query = query.where(Booking.id != exclude_booking_id)
        
        result = await db.execute(query)
        return result.scalars().all()