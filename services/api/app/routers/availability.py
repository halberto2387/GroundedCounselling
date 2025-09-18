"""
Availability API endpoints.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.specialist import Specialist
from app.models.availability import DayOfWeek
from app.schemas.availability import (
    AvailabilityCreate, AvailabilityUpdate, AvailabilityOut,
    BulkAvailabilityCreate, AvailableSlot
)
from app.services.availability import AvailabilityService
from app.security.auth import get_current_specialist


router = APIRouter(prefix="/availability", tags=["availability"])


@router.post("", response_model=AvailabilityOut, status_code=status.HTTP_201_CREATED)
async def create_availability(
    availability_data: AvailabilityCreate,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Create an availability slot for the current specialist."""
    try:
        availability = await AvailabilityService.create_availability(
            session, availability_data, current_specialist.id
        )
        return availability
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/bulk", response_model=List[AvailabilityOut], status_code=status.HTTP_201_CREATED)
async def create_bulk_availability(
    bulk_data: BulkAvailabilityCreate,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Create multiple availability slots at once."""
    try:
        availabilities = await AvailabilityService.bulk_create_availability(
            session, current_specialist.id, bulk_data.availabilities
        )
        return availabilities
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me", response_model=List[AvailabilityOut])
async def get_my_availability(
    day_of_week: Optional[DayOfWeek] = Query(None),
    is_available: Optional[bool] = Query(None),
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Get availability slots for the current specialist."""
    availabilities = await AvailabilityService.get_specialist_availability(
        session, current_specialist.id, day_of_week=day_of_week, is_available=is_available
    )
    return availabilities


@router.get("/specialist/{specialist_id}", response_model=List[AvailabilityOut])
async def get_specialist_availability(
    specialist_id: UUID,
    day_of_week: Optional[DayOfWeek] = Query(None),
    is_available: Optional[bool] = Query(None),
    session: AsyncSession = Depends(get_session),
):
    """Get availability slots for a specific specialist (public endpoint)."""
    availabilities = await AvailabilityService.get_specialist_availability(
        session, specialist_id, day_of_week=day_of_week, is_available=is_available
    )
    return availabilities


@router.get("/specialist/{specialist_id}/slots", response_model=List[AvailableSlot])
async def get_available_slots(
    specialist_id: UUID,
    target_date: date = Query(...),
    duration_minutes: int = Query(60, ge=15, le=480),
    session: AsyncSession = Depends(get_session),
):
    """Get available time slots for a specific specialist and date."""
    try:
        slots = await AvailabilityService.get_available_slots(
            session, specialist_id, target_date, duration_minutes
        )
        
        # Convert datetime objects to AvailableSlot schema
        available_slots = [
            AvailableSlot(
                start_time=slot,
                end_time=slot + timedelta(minutes=duration_minutes),
                duration_minutes=duration_minutes
            )
            for slot in slots
        ]
        
        return available_slots
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching available slots: {str(e)}"
        )


@router.get("/{availability_id}", response_model=AvailabilityOut)
async def get_availability(
    availability_id: UUID,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Get availability slot by ID (only for current specialist)."""
    availability = await AvailabilityService.get_availability(session, availability_id)
    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found"
        )
    
    if availability.specialist_id != current_specialist.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return availability


@router.put("/{availability_id}", response_model=AvailabilityOut)
async def update_availability(
    availability_id: UUID,
    availability_data: AvailabilityUpdate,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Update availability slot (only for current specialist)."""
    availability = await AvailabilityService.get_availability(session, availability_id)
    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found"
        )
    
    if availability.specialist_id != current_specialist.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        updated_availability = await AvailabilityService.update_availability(
            session, availability_id, availability_data
        )
        return updated_availability
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_availability(
    availability_id: UUID,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Delete availability slot (only for current specialist)."""
    availability = await AvailabilityService.get_availability(session, availability_id)
    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found"
        )
    
    if availability.specialist_id != current_specialist.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    await AvailabilityService.delete_availability(session, availability_id)


@router.delete("/me/all", status_code=status.HTTP_204_NO_CONTENT)
async def clear_my_availability(
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Clear all availability slots for the current specialist."""
    await AvailabilityService.clear_specialist_availability(
        session, current_specialist.id
    )