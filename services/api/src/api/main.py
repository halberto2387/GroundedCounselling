"""
FastAPI application factory for GroundedCounselling API.
"""

import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .config import get_settings
from .db import close_database, init_database

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    await init_database()
    
    yield
    
    # Shutdown
    await close_database()


def create_app() -> FastAPI:
    """
    FastAPI application factory.
    
    Returns:
        FastAPI: Configured FastAPI application
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Security middleware - Trusted Host (should be first)
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*.groundedcounselling.com", "localhost"]
        )

    # CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
            allow_headers=["*"],
        )

    # Security headers middleware
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next) -> Response:
        """Add security headers to all responses."""
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=(), payment=(), usb=()"
        )
        
        # Content Security Policy
        if not settings.DEBUG:
            csp = (
                "default-src 'self'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "style-src 'self' 'unsafe-inline'; "
                "script-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "object-src 'none';"
            )
            response.headers["Content-Security-Policy"] = csp
        
        # HSTS in production
        if not settings.DEBUG and request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        
        return response

    # Request ID and timing middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next) -> Response:
        """Add process time and request ID headers."""
        start_time = time.time()
        
        # Add request ID if not present
        request_id = request.headers.get("X-Request-ID", f"req_{int(time.time())}")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id
        
        return response

    # Health check endpoints
    @app.get("/health", tags=["Health"])
    async def health_check() -> dict:
        """Health check endpoint for Docker and load balancers."""
        return {
            "status": "healthy",
            "service": "api",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
        }

    @app.get("/", tags=["Root"])
    async def root() -> dict:
        """Root endpoint."""
        return {
            "message": f"{settings.PROJECT_NAME} is running",
            "version": settings.VERSION,
            "docs_url": "/docs" if settings.DEBUG else None,
        }

    @app.get("/api/v1/health", tags=["Health"])
    async def api_v1_health() -> dict:
        """API v1 health check."""
        return {
            "status": "healthy",
            "api_version": "v1",
            "environment": settings.ENVIRONMENT,
        }

    return app


# Create app instance
app = create_app()


def run() -> None:
    """Run the application with uvicorn."""
    import uvicorn
    
    uvicorn.run(
        "api.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    run()