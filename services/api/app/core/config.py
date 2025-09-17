from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    # Database
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/grounded_counselling"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    JWT_SECRET: str = "your-super-secret-jwt-key-change-this-in-production"
    JWT_REFRESH_SECRET: str = "your-super-secret-refresh-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRES_MIN: int = 15
    REFRESH_TOKEN_EXPIRES_HR: int = 168  # 1 week
    JWT_ALGORITHM: str = "HS256"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GroundedCounselling API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "FastAPI backend for GroundedCounselling"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://localhost:3000",
    ]
    
    # Email (Resend)
    RESEND_API_KEY: str | None = None
    
    # SMS (Twilio)
    TWILIO_ACCOUNT_SID: str | None = None
    TWILIO_AUTH_TOKEN: str | None = None
    TWILIO_PHONE_NUMBER: str | None = None
    
    # Payments (Stripe)
    STRIPE_PUBLISHABLE_KEY: str | None = None
    STRIPE_SECRET_KEY: str | None = None
    STRIPE_WEBHOOK_SECRET: str | None = None
    
    # Sentry
    SENTRY_DSN: str | None = None
    SENTRY_ENV: str = "development"
    
    # Admin
    FIRST_SUPERUSER_EMAIL: str = "admin@groundedcounselling.com"
    FIRST_SUPERUSER_PASSWORD: str = "change-this-password"
    
    # Security
    SECRET_KEY: str = "your-secret-key-for-encryption"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: list[str] = [
        "image/jpeg",
        "image/png", 
        "image/gif",
        "application/pdf"
    ]
    
    # Calendar Integration
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    OUTLOOK_CLIENT_ID: str | None = None
    OUTLOOK_CLIENT_SECRET: str | None = None
    
    # Search (Meilisearch)
    MEILISEARCH_URL: str | None = None
    MEILISEARCH_API_KEY: str | None = None
    
    @property
    def database_url_async(self) -> str:
        """Convert psycopg2 URL to asyncpg URL."""
        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.DATABASE_URL


settings = Settings()