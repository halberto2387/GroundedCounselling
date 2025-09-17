from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Worker settings."""
    
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Email (Resend)
    RESEND_API_KEY: str | None = None
    
    # SMS (Twilio)
    TWILIO_ACCOUNT_SID: str | None = None
    TWILIO_AUTH_TOKEN: str | None = None
    TWILIO_PHONE_NUMBER: str | None = None
    
    # Sentry
    SENTRY_DSN: str | None = None
    SENTRY_ENV: str = "development"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Worker Configuration
    WORKER_NAME: str = "grounded-counselling-worker"
    WORKER_QUEUES: list[str] = ["default", "email", "sms", "notifications", "reports"]
    
    # Logging
    LOG_LEVEL: str = "INFO"


settings = Settings()