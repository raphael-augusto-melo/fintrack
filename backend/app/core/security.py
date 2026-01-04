from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.settings import get_settings
import bcrypt



def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    plain_bytes = plain.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode["exp"] = expire

    settings = get_settings()

    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

    return token


def decode_access_token(token: str) -> dict:
    try:
        settings = get_settings()
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise ValueError("token_expirado")
    except JWTError:
        raise ValueError("token_invalido")