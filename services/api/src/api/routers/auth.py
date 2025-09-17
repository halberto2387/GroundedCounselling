"""
Authentication router - placeholder implementation.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Authentication"])
async def auth_root() -> dict:
    """Authentication endpoint placeholder."""
    return {"message": "Authentication endpoints will be implemented here"}