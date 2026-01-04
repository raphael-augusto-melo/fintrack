import pytest
from app.core.settings import get_settings


from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


@pytest.fixture(autouse=True)
def clean_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def set_auth_env(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    monkeypatch.setenv("DATABASE_URL", "postgresql://x:y@localhost:5434/fintrack")
    yield


def test_password_hash_and_verify():
    hashed = hash_password("abc")
    assert hashed != "abc"
    assert verify_password("abc", hashed) is True
    assert verify_password("wrong", hashed) is False


def test_jwt_encode_decode(set_auth_env):
    token = create_access_token({"sub": "user-123"})
    payload = decode_access_token(token)
    assert payload["sub"] == "user-123"


def test_jwt_tampered_is_invalid(set_auth_env):
    token = create_access_token({"sub": "user-123"})
    tampered = token[:-1] + ("a" if token[-1] != "a" else "b")
    with pytest.raises(ValueError) as exc:
        decode_access_token(tampered)
    assert str(exc.value) == "token_invalido"


def test_jwt_expired_raises(set_auth_env, monkeypatch):
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "-1")
    get_settings.cache_clear()

    token = create_access_token({"sub": "user-123"})
    with pytest.raises(ValueError) as exc:
        decode_access_token(token)

    assert str(exc.value) == "token_expirado"
