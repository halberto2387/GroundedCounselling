"""
Minimal FastAPI application for GroundedCounselling API.
This is a placeholder implementation for Docker testing.
"""

from fastapi import FastAPI
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
    return {
        "status": "healthy",
        "service": "api",
        "version": "0.1.0"
    }

@app.get("/api/v1/health")
async def api_health():
    """API health check"""
    return {
        "status": "healthy",
        "api_version": "v1",
        "environment": os.getenv("NODE_ENV", "development")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)