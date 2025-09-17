from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import sentry_sdk

from app.api.v1.routers import auth, users, specialists, bookings
from app.core.config import settings
from app.observability.sentry import init_sentry
from app.observability.logging import setup_logging


def get_limiter_key(request: Request) -> str:
    """Get rate limiting key from request."""
    return get_remote_address(request)


# Initialize rate limiter
limiter = Limiter(key_func=get_limiter_key, default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_logging()
    if settings.SENTRY_DSN:
        init_sentry()
    
    yield
    
    # Shutdown
    pass


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    # Rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.groundedcounselling.com"],
    )
    
    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
        }
    
    # Root endpoint
    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint."""
        return {
            "message": "GroundedCounselling API",
            "version": settings.VERSION,
            "docs": "/docs",
            "health": "/health",
        }
    
    # Include routers
    app.include_router(
        auth.router,
        prefix=f"{settings.API_V1_STR}/auth",
        tags=["authentication"],
    )
    app.include_router(
        users.router,
        prefix=f"{settings.API_V1_STR}/users",
        tags=["users"],
    )
    app.include_router(
        specialists.router,
        prefix=f"{settings.API_V1_STR}/specialists",
        tags=["specialists"],
    )
    app.include_router(
        bookings.router,
        prefix=f"{settings.API_V1_STR}/bookings",
        tags=["bookings"],
    )
    
    # Custom exception handlers
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Any) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Resource not found"},
        )
    
    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc: Any) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
    
    return app


# Create the application instance
app = create_app()