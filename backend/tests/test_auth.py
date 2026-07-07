import pytest

from app.services.auth_service import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hashing():
    hashed = hash_password("test123")
    assert verify_password("test123", hashed)
    assert not verify_password("wrong", hashed)


def test_token_roundtrip():
    token = create_access_token("user-1", "operator")
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "user-1"
    assert payload["role"] == "operator"


def test_expired_token():
    from datetime import timedelta
    from app.config import settings

    original = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    settings.ACCESS_TOKEN_EXPIRE_MINUTES = 0
    token = create_access_token("user-1", "operator")
    payload = decode_access_token(token)
    assert payload is None
    settings.ACCESS_TOKEN_EXPIRE_MINUTES = original
