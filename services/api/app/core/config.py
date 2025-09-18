from pydantic_settings import BaseSettings
from pydantic import Field


def _derive_async_url(db_url: str) -> str:
    # If already async, return as-is
    if db_url.startswith("postgresql+asyncpg://"):
        return db_url
    # Convert common sync form to asyncpg driver for SQLAlchemy async engine
    if db_url.startswith("postgresql://"):
        return db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return db_url


class Settings(BaseSettings):
    app_name: str = "GroundedCounselling API"
    # Sync URL for Alembic; Async URL for application use
    database_url_sync: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/grounded_counselling",
        alias="DATABASE_URL",
    )
    async_database_url: str | None = Field(default=None, alias="ASYNC_DATABASE_URL")
    jwt_secret: str = Field(default="dev-secret-change-in-production", alias="JWT_SECRET")
    access_token_expires_min: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRES_MIN")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        # Prefer explicit async URL; otherwise derive from sync
        if self.async_database_url:
            return self.async_database_url
        return _derive_async_url(self.database_url_sync)


settings = Settings()
