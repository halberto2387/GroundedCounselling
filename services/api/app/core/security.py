from datetime import datetime, timedelta
from typing import Any

import bcrypt
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MIN)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.REFRESH_TOKEN_EXPIRES_HR)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str, secret: str) -> dict[str, Any] | None:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_access_token(token: str) -> dict[str, Any] | None:
    """Verify an access token."""
    payload = verify_token(token, settings.JWT_SECRET)
    if payload and payload.get("type") == "access":
        return payload
    return None


def verify_refresh_token(token: str) -> dict[str, Any] | None:
    """Verify a refresh token."""
    payload = verify_token(token, settings.JWT_REFRESH_SECRET)
    if payload and payload.get("type") == "refresh":
        return payload
    return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def generate_totp_secret() -> str:
    """Generate a TOTP secret for 2FA."""
    # TODO: Implement TOTP secret generation
    # For now, return a placeholder
    return "TOTP_SECRET_PLACEHOLDER"


def verify_totp_token(secret: str, token: str) -> bool:
    """Verify a TOTP token for 2FA."""
    # TODO: Implement TOTP verification
    # For now, return True for development
    return True