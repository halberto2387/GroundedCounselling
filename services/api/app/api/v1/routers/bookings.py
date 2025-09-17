from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.models.booking import BookingStatus
from app.schemas.booking import Booking, BookingList, BookingCreate, BookingUpdate

router = APIRouter()
security = HTTPBearer()


@router.get("/", response_model=List[BookingList])
async def get_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: BookingStatus = Query(None, alias="status"),
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Get user's bookings."""
    # TODO: Implement booking listing with filtering
    # This is a placeholder implementation
    
    mock_bookings = [
        BookingList(
            id=f"booking-{i}",
            start_time="2024-01-15T10:00:00Z",
            duration_minutes=60,
            status=BookingStatus.CONFIRMED,
            total_cost=150.00,
            is_paid=True,
            specialist_name="Dr. Jane Smith",
            client_name="John Doe",
        )
        for i in range(skip, skip + min(limit, 5))
    ]
    
    return mock_bookings


@router.get("/{booking_id}", response_model=Booking)
async def get_booking(
    booking_id: str,
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Get booking by ID."""
    # TODO: Implement booking retrieval
    # This is a placeholder implementation
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Booking retrieval not yet implemented",
    )


@router.post("/", response_model=Booking)
async def create_booking(
    booking_data: BookingCreate,
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Create a new booking."""
    # TODO: Implement booking creation
    # This is a placeholder implementation
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Booking creation not yet implemented",
    )


@router.put("/{booking_id}", response_model=Booking)
async def update_booking(
    booking_id: str,
    booking_update: BookingUpdate,
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Update booking."""
    # TODO: Implement booking update
    # This is a placeholder implementation
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Booking update not yet implemented",
    )


@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: str,
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Cancel booking."""
    # TODO: Implement booking cancellation
    # This is a placeholder implementation
    
    return {"message": "Booking cancelled successfully"}