"""
API router initialization.
"""

from fastapi import APIRouter

from .auth import router as auth_router

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Add a simple test endpoint
@api_router.get("/", tags=["API"])
async def api_root() -> dict:
    """API root endpoint."""
    return {"message": "GroundedCounselling API v1"}