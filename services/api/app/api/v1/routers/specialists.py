from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.schemas.specialist import Specialist, SpecialistList, SpecialistCreate, SpecialistUpdate

router = APIRouter()
security = HTTPBearer()


@router.get("/", response_model=List[SpecialistList])
async def get_specialists(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    specialization: str = Query(None),
    db: AsyncSession = Depends(get_async_session),
):
    """Get list of specialists."""
    # TODO: Implement specialist listing with filtering
    # This is a placeholder implementation
    
    mock_specialists = [
        SpecialistList(
            id=f"specialist-{i}",
            display_name=f"Dr. Specialist {i}",
            bio=f"Experienced counsellor specializing in therapy {i}",
            specializations=["Anxiety", "Depression"],
            hourly_rate=100.00 + (i * 10),
            years_experience=5 + i,
            average_rating=4.5,
            total_reviews=20 + i,
            is_available=True,
            is_accepting_new_clients=True,
        )
        for i in range(skip, skip + min(limit, 10))
    ]
    
    return mock_specialists


@router.get("/{specialist_id}", response_model=Specialist)
async def get_specialist(
    specialist_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    """Get specialist by ID."""
    # TODO: Implement specialist retrieval
    # This is a placeholder implementation
    
    from app.schemas.user import User
    
    mock_user = User(
        id="user-1",
        email="specialist@example.com",
        first_name="Dr. Jane",
        last_name="Smith",
        role="counsellor",
        phone="+1234567890",
        is_active=True,
        is_verified=True,
        is_2fa_enabled=False,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        last_login_at="2024-01-01T12:00:00Z",
    )
    
    mock_specialist = Specialist(
        id=specialist_id,
        user_id="user-1",
        bio="Experienced clinical psychologist with 10+ years of experience",
        specializations=["Anxiety", "Depression", "PTSD"],
        credentials=["PhD Psychology", "Licensed Clinical Psychologist"],
        languages=["English", "Spanish"],
        hourly_rate=150.00,
        is_available=True,
        is_accepting_new_clients=True,
        years_experience=10,
        total_sessions=500,
        average_rating=4.8,
        total_reviews=45,
        license_number="PSY12345",
        license_state="CA",
        education="PhD in Clinical Psychology, UCLA",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        user=mock_user,
        display_name="Dr. Jane Smith",
    )
    
    return mock_specialist


@router.post("/", response_model=Specialist)
async def create_specialist_profile(
    specialist_data: SpecialistCreate,
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Create specialist profile (counsellor only)."""
    # TODO: Implement specialist profile creation
    # This is a placeholder implementation
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Specialist profile creation not yet implemented",
    )


@router.put("/{specialist_id}", response_model=Specialist)
async def update_specialist_profile(
    specialist_id: str,
    specialist_update: SpecialistUpdate,
    token: str = Depends(security),
    db: AsyncSession = Depends(get_async_session),
):
    """Update specialist profile (own profile only)."""
    # TODO: Implement specialist profile update
    # This is a placeholder implementation
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Specialist profile update not yet implemented",
    )