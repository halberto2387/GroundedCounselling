"""
Booking API endpoints.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.user import User
from app.models.specialist import Specialist
from app.models.booking import BookingStatus
from app.schemas.booking import BookingCreate, BookingUpdate, BookingOut
from app.services.booking import BookingService
from app.security.auth import get_current_user, get_current_specialist


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Create a new booking as a patient."""
    try:
        booking = await BookingService.create_booking(
            session, booking_data, current_user.id
        )
        return booking
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/my-bookings", response_model=List[BookingOut])
async def get_my_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status_filter: Optional[BookingStatus] = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get current user's bookings as a patient."""
    bookings = await BookingService.get_bookings_for_patient(
        session, current_user.id, skip=skip, limit=limit, status=status_filter
    )
    return bookings


@router.get("/specialist-bookings", response_model=List[BookingOut])
async def get_specialist_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status_filter: Optional[BookingStatus] = Query(None, alias="status"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Get bookings for the current specialist."""
    bookings = await BookingService.get_bookings_for_specialist(
        session, current_specialist.id, skip=skip, limit=limit,
        status=status_filter, start_date=start_date, end_date=end_date
    )
    return bookings


@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(
    booking_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get booking by ID (only if user is patient or specialist for this booking)."""
    booking = await BookingService.get_booking(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check if user has access to this booking
    if (booking.patient_id != current_user.id and 
        booking.specialist.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return booking


@router.put("/{booking_id}", response_model=BookingOut)
async def update_booking(
    booking_id: UUID,
    booking_data: BookingUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Update booking (only by patient who created it)."""
    booking = await BookingService.get_booking(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Only patient can update booking details
    if booking.patient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the patient can update booking details"
        )
    
    try:
        updated_booking = await BookingService.update_booking(
            session, booking_id, booking_data
        )
        return updated_booking
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{booking_id}/cancel", response_model=BookingOut)
async def cancel_booking(
    booking_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Cancel a booking (by patient or specialist)."""
    booking = await BookingService.get_booking(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check if user has permission to cancel
    if (booking.patient_id != current_user.id and 
        booking.specialist.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        cancelled_booking = await BookingService.cancel_booking(session, booking_id)
        return cancelled_booking
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{booking_id}/confirm", response_model=BookingOut)
async def confirm_booking(
    booking_id: UUID,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Confirm a pending booking (only by specialist)."""
    booking = await BookingService.get_booking(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Only the specialist for this booking can confirm
    if booking.specialist_id != current_specialist.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the specialist can confirm this booking"
        )
    
    try:
        confirmed_booking = await BookingService.confirm_booking(session, booking_id)
        return confirmed_booking
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{booking_id}/complete", response_model=BookingOut)
async def complete_booking(
    booking_id: UUID,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Mark a booking as completed (only by specialist)."""
    booking = await BookingService.get_booking(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Only the specialist for this booking can complete
    if booking.specialist_id != current_specialist.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the specialist can complete this booking"
        )
    
    try:
        completed_booking = await BookingService.complete_booking(session, booking_id)
        return completed_booking
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))