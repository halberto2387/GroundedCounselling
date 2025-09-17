import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from app.core.config import settings


def init_sentry() -> None:
    """Initialize Sentry for error tracking."""
    if not settings.SENTRY_DSN:
        return
    
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENV,
        integrations=[
            FastApiIntegration(auto_enabling_integrations=False),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=0.1 if settings.ENVIRONMENT == "production" else 1.0,
        debug=settings.DEBUG,
    )