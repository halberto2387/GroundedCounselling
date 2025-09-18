"""
Session service for CRUD operations.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.session import Session
from app.models.booking import Booking, BookingStatus
from app.schemas.session import SessionCreate, SessionUpdate


class SessionService:
    """Service class for session CRUD operations."""

    @staticmethod
    async def create_session(
        db: AsyncSession, session_data: SessionCreate, booking_id: UUID
    ) -> Session:
        """Create a new session for a booking."""
        # Validate booking exists and is confirmed
        booking = await db.get(Booking, booking_id)
        if not booking:
            raise ValueError("Booking not found")

        if booking.status != BookingStatus.CONFIRMED:
            raise ValueError("Can only create sessions for confirmed bookings")

        # Check if session already exists for this booking
        existing = await SessionService.get_session_by_booking_id(db, booking_id)
        if existing:
            raise ValueError("Session already exists for this booking")

        session = Session(
            booking_id=booking_id,
            notes=session_data.notes,
            recording_url=session_data.recording_url,
            summary=session_data.summary,
            action_items=session_data.action_items,
            next_steps=session_data.next_steps,
        )
        
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def get_session(db: AsyncSession, session_id: UUID) -> Optional[Session]:
        """Get session by ID with related data."""
        result = await db.execute(
            select(Session)
            .options(
                selectinload(Session.booking)
                .selectinload(Booking.patient),
                selectinload(Session.booking)
                .selectinload(Booking.specialist)
                .selectinload(Booking.specialist.user)
            )
            .where(Session.id == session_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_session_by_booking_id(
        db: AsyncSession, booking_id: UUID
    ) -> Optional[Session]:
        """Get session by booking ID."""
        result = await db.execute(
            select(Session)
            .options(
                selectinload(Session.booking)
                .selectinload(Booking.patient),
                selectinload(Session.booking)
                .selectinload(Booking.specialist)
                .selectinload(Booking.specialist.user)
            )
            .where(Session.booking_id == booking_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_sessions_for_patient(
        db: AsyncSession,
        patient_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Session]:
        """Get sessions for a specific patient."""
        result = await db.execute(
            select(Session)
            .join(Booking)
            .options(
                selectinload(Session.booking)
                .selectinload(Booking.specialist)
                .selectinload(Booking.specialist.user)
            )
            .where(Booking.patient_id == patient_id)
            .offset(skip)
            .limit(limit)
            .order_by(Session.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_sessions_for_specialist(
        db: AsyncSession,
        specialist_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Session]:
        """Get sessions for a specific specialist."""
        result = await db.execute(
            select(Session)
            .join(Booking)
            .options(
                selectinload(Session.booking)
                .selectinload(Booking.patient)
            )
            .where(Booking.specialist_id == specialist_id)
            .offset(skip)
            .limit(limit)
            .order_by(Session.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def update_session(
        db: AsyncSession, session_id: UUID, session_data: SessionUpdate
    ) -> Optional[Session]:
        """Update session information."""
        session = await SessionService.get_session(db, session_id)
        if not session:
            return None

        update_data = session_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(session, field, value)

        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def delete_session(db: AsyncSession, session_id: UUID) -> bool:
        """Delete session record."""
        session = await SessionService.get_session(db, session_id)
        if not session:
            return False

        await db.delete(session)
        await db.commit()
        return True

    @staticmethod
    async def add_session_notes(
        db: AsyncSession, session_id: UUID, notes: str
    ) -> Optional[Session]:
        """Add or update session notes."""
        session = await SessionService.get_session(db, session_id)
        if not session:
            return None

        session.notes = notes
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def set_recording_url(
        db: AsyncSession, session_id: UUID, recording_url: str
    ) -> Optional[Session]:
        """Set the recording URL for a session."""
        session = await SessionService.get_session(db, session_id)
        if not session:
            return None

        session.recording_url = recording_url
        await db.commit()
        await db.refresh(session)
        return session