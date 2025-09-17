"""
Sentry configuration for error monitoring.
"""

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from ..config import get_settings

settings = get_settings()


def setup_sentry() -> None:
    """
    Configure Sentry for error monitoring.
    """
    if not settings.ENABLE_SENTRY or not settings.SENTRY_DSN:
        return

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENVIRONMENT or settings.ENVIRONMENT,
        integrations=[
            FastApiIntegration(auto_enable=True),
            SqlalchemyIntegration(),
        ],
        # Performance monitoring
        traces_sample_rate=0.1 if settings.ENVIRONMENT == "production" else 1.0,
        # Error filtering
        before_send=filter_sensitive_data,
        # Release tracking
        release=settings.VERSION,
    )


def filter_sensitive_data(event: dict, hint: dict) -> dict:
    """
    Filter sensitive data from Sentry events.
    
    Args:
        event: Sentry event data
        hint: Additional context
        
    Returns:
        dict: Filtered event data
    """
    # Remove sensitive headers
    if "request" in event and "headers" in event["request"]:
        headers = event["request"]["headers"]
        sensitive_headers = ["authorization", "cookie", "x-api-key"]
        
        for header in sensitive_headers:
            if header in headers:
                headers[header] = "[Filtered]"
    
    # Remove sensitive form data
    if "request" in event and "data" in event["request"]:
        data = event["request"]["data"]
        if isinstance(data, dict):
            sensitive_fields = ["password", "token", "secret", "key"]
            for field in sensitive_fields:
                if field in data:
                    data[field] = "[Filtered]"
    
    return event