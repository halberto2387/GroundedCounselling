from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
    verify_password,
    get_password_hash,
)


def test_password_hashing():
    """Test password hashing and verification."""
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_access_token_creation_and_verification():
    """Test access token creation and verification."""
    data = {"sub": "user123", "email": "test@example.com"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    
    payload = verify_access_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["email"] == "test@example.com"
    assert payload["type"] == "access"


def test_refresh_token_creation_and_verification():
    """Test refresh token creation and verification."""
    data = {"sub": "user123", "email": "test@example.com"}
    token = create_refresh_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    
    payload = verify_refresh_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["email"] == "test@example.com"
    assert payload["type"] == "refresh"


def test_invalid_token_verification():
    """Test verification of invalid tokens."""
    invalid_token = "invalid.token.here"
    
    assert verify_access_token(invalid_token) is None
    assert verify_refresh_token(invalid_token) is None