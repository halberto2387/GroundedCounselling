"""
Session API endpoints.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.user import User
from app.models.specialist import Specialist
from app.schemas.session import SessionCreate, SessionUpdate, SessionOut
from app.services.session import SessionService
from app.services.booking import BookingService
from app.security.auth import get_current_user, get_current_specialist


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    booking_id: UUID,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Create a session for a booking (only by specialist)."""
    # Verify specialist owns the booking
    booking = await BookingService.get_booking(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.specialist_id != current_specialist.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the specialist can create sessions for their bookings"
        )
    
    try:
        session_record = await SessionService.create_session(
            session, session_data, booking_id
        )
        return session_record
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/my-sessions", response_model=List[SessionOut])
async def get_my_sessions_as_patient(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get sessions for current user as a patient."""
    sessions = await SessionService.get_sessions_for_patient(
        session, current_user.id, skip=skip, limit=limit
    )
    return sessions


@router.get("/specialist-sessions", response_model=List[SessionOut])
async def get_my_sessions_as_specialist(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Get sessions for current specialist."""
    sessions = await SessionService.get_sessions_for_specialist(
        session, current_specialist.id, skip=skip, limit=limit
    )
    return sessions


@router.get("/{session_id}", response_model=SessionOut)
async def get_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session),
):
    """Get session by ID (only if user is patient or specialist for this session)."""
    session_record = await SessionService.get_session(db_session, session_id)
    if not session_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Check if user has access to this session
    if (session_record.booking.patient_id != current_user.id and 
        session_record.booking.specialist.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return session_record


@router.get("/booking/{booking_id}", response_model=SessionOut)
async def get_session_by_booking(
    booking_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get session for a specific booking."""
    # First verify user has access to the booking
    booking = await BookingService.get_booking(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if (booking.patient_id != current_user.id and 
        booking.specialist.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    session_record = await SessionService.get_session_by_booking_id(session, booking_id)
    if not session_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found for this booking"
        )
    
    return session_record


@router.put("/{session_id}", response_model=SessionOut)
async def update_session(
    session_id: UUID,
    session_data: SessionUpdate,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Update session (only by specialist who created it)."""
    session_record = await SessionService.get_session(session, session_id)
    if not session_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Only the specialist can update session details
    if session_record.booking.specialist_id != current_specialist.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the specialist can update session details"
        )
    
    updated_session = await SessionService.update_session(
        session, session_id, session_data
    )
    return updated_session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: UUID,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Delete session (only by specialist who created it)."""
    session_record = await SessionService.get_session(session, session_id)
    if not session_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Only the specialist can delete session
    if session_record.booking.specialist_id != current_specialist.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the specialist can delete sessions"
        )
    
    await SessionService.delete_session(session, session_id)


@router.patch("/{session_id}/notes", response_model=SessionOut)
async def update_session_notes(
    session_id: UUID,
    notes: str,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Update session notes (only by specialist)."""
    session_record = await SessionService.get_session(session, session_id)
    if not session_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session_record.booking.specialist_id != current_specialist.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the specialist can update session notes"
        )
    
    updated_session = await SessionService.add_session_notes(session, session_id, notes)
    return updated_session


@router.patch("/{session_id}/recording", response_model=SessionOut)
async def set_recording_url(
    session_id: UUID,
    recording_url: str,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Set recording URL for session (only by specialist)."""
    session_record = await SessionService.get_session(session, session_id)
    if not session_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session_record.booking.specialist_id != current_specialist.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the specialist can set recording URL"
        )
    
    updated_session = await SessionService.set_recording_url(
        session, session_id, recording_url
    )
    return updated_session