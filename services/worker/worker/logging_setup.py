import logging
import sys
from typing import Any

import structlog
import sentry_sdk

from worker.config import settings


def setup_logging() -> None:
    """Setup structured logging."""
    
    # Initialize Sentry if DSN is provided
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.SENTRY_ENV,
            traces_sample_rate=0.1 if settings.ENVIRONMENT == "production" else 1.0,
            debug=settings.DEBUG,
        )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if settings.DEBUG else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=False,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    )


def get_logger(name: str) -> Any:
    """Get a structured logger."""
    return structlog.get_logger(name)