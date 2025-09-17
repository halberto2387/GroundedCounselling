import logging
import sys
from typing import Any

import structlog
from structlog.contextvars import clear_contextvars

from app.core.config import settings


def setup_logging() -> None:
    """Setup structured logging."""
    
    # Clear any existing context
    clear_contextvars()
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if settings.DEBUG else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if settings.DEBUG else logging.INFO,
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=False,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
    )
    
    # Suppress noisy loggers in production
    if not settings.DEBUG:
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> Any:
    """Get a structured logger."""
    return structlog.get_logger(name)