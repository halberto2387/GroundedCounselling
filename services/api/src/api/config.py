"""
Configuration management using Pydantic Settings.
"""

import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    field_validator,
)


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "GroundedCounselling API"
    PROJECT_DESCRIPTION: str = "A secure, HIPAA-compliant platform for counselling practice management"
    VERSION: str = "0.1.0"
    
    # Server Configuration
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database Configuration
    DATABASE_URL: Optional[PostgresDsn] = None
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis Configuration
    REDIS_URL: Optional[RedisDsn] = None
    REDIS_POOL_SIZE: int = 10
    
    # Authentication Configuration
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_REFRESH_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Security Configuration
    PASSWORD_MIN_LENGTH: int = 8
    BCRYPT_ROUNDS: int = 12
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Email Configuration (Resend)
    RESEND_API_KEY: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # SMS Configuration (Twilio)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_FROM_NUMBER: Optional[str] = None
    
    # Payment Configuration (Stripe)
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: Optional[str] = None
    
    # Video Configuration
    VIDEO_PROVIDER: str = "jitsi"  # jitsi, livekit
    JITSI_DOMAIN: str = "meet.jit.si"
    LIVEKIT_API_KEY: Optional[str] = None
    LIVEKIT_API_SECRET: Optional[str] = None
    LIVEKIT_WS_URL: Optional[str] = None
    
    # OAuth Configuration
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    MICROSOFT_CLIENT_ID: Optional[str] = None
    MICROSOFT_CLIENT_SECRET: Optional[str] = None
    
    # Search Configuration (Meilisearch)
    MEILISEARCH_URL: Optional[str] = None
    MEILISEARCH_MASTER_KEY: Optional[str] = None
    
    # Monitoring Configuration
    SENTRY_DSN: Optional[str] = None
    SENTRY_ENVIRONMENT: Optional[str] = None
    ENABLE_SENTRY: bool = False
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json, text
    
    # Background Tasks
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    RQ_REDIS_URL: Optional[str] = None
    
    # File Upload Configuration
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "application/pdf",
        "text/plain",
    ]
    
    # Encryption Configuration
    ENCRYPTION_KEY: Optional[str] = None
    
    # Compliance Configuration
    AUDIT_LOG_ENABLED: bool = True
    DATA_RETENTION_DAYS: int = 2555  # 7 years for HIPAA
    
    class Config:
        """Pydantic configuration."""
        
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings