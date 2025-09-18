"""
Specialist API endpoints.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.user import User
from app.models.specialist import Specialist
from app.schemas.specialist import SpecialistCreate, SpecialistUpdate, SpecialistOut
from app.services.specialist import SpecialistService
from app.security.auth import get_current_user, get_current_specialist


router = APIRouter(prefix="/specialists", tags=["specialists"])


@router.post("", response_model=SpecialistOut, status_code=status.HTTP_201_CREATED)
async def create_specialist_profile(
    specialist_data: SpecialistCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Create a specialist profile for the current user."""
    try:
        specialist = await SpecialistService.create_specialist(
            session, specialist_data, current_user.id
        )
        return specialist
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[SpecialistOut])
async def list_specialists(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_available: Optional[bool] = Query(None),
    specializations: Optional[List[str]] = Query(None),
    session: AsyncSession = Depends(get_session),
):
    """Get list of specialists with optional filtering."""
    specialists = await SpecialistService.get_specialists(
        session, skip=skip, limit=limit, 
        is_available=is_available, specializations=specializations
    )
    return specialists


@router.get("/me", response_model=SpecialistOut)
async def get_my_specialist_profile(
    current_specialist: Specialist = Depends(get_current_specialist),
):
    """Get current user's specialist profile."""
    return current_specialist


@router.get("/{specialist_id}", response_model=SpecialistOut)
async def get_specialist(
    specialist_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Get specialist by ID."""
    specialist = await SpecialistService.get_specialist(session, specialist_id)
    if not specialist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specialist not found"
        )
    return specialist


@router.put("/me", response_model=SpecialistOut)
async def update_my_specialist_profile(
    specialist_data: SpecialistUpdate,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Update current user's specialist profile."""
    try:
        specialist = await SpecialistService.update_specialist(
            session, current_specialist.id, specialist_data
        )
        return specialist
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{specialist_id}", response_model=SpecialistOut)
async def update_specialist(
    specialist_id: UUID,
    specialist_data: SpecialistUpdate,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Update specialist profile (only by the specialist themselves)."""
    if current_specialist.id != specialist_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only update your own profile"
        )
    
    try:
        specialist = await SpecialistService.update_specialist(
            session, specialist_id, specialist_data
        )
        if not specialist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specialist not found"
            )
        return specialist
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_specialist_profile(
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Delete current user's specialist profile."""
    await SpecialistService.delete_specialist(session, current_specialist.id)


@router.patch("/me/availability", response_model=SpecialistOut)
async def toggle_my_availability(
    is_available: bool,
    current_specialist: Specialist = Depends(get_current_specialist),
    session: AsyncSession = Depends(get_session),
):
    """Toggle current specialist's availability status."""
    specialist = await SpecialistService.toggle_availability(
        session, current_specialist.id, is_available
    )
    return specialist