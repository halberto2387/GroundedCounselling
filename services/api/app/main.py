"""
Minimal FastAPI application for GroundedCounselling API.
This is a placeholder implementation for Docker testing.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import get_session
from app.routers import auth as auth_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="GroundedCounselling API",
    description="A secure, HIPAA-compliant platform for counselling practice management",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "GroundedCounselling API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {"status": "healthy", "service": "api", "version": "0.1.0"}

@app.get("/api/v1/health")
async def api_health(session: AsyncSession = Depends(get_session)):
    """API health check"""
    # Verify DB connectivity
    await session.execute(text("SELECT 1"))
    return {
        "status": "healthy",
        "api_version": "v1",
        "environment": os.getenv("NODE_ENV", "development"),
    }

app.include_router(auth_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)