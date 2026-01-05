from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.auth import RegisterRequest, UserResponse
from app.core.security import hash_password, verify_password
from app.services.exceptions import EmailAlreadyExistsError

def register_user(db: Session, data: RegisterRequest) -> UserResponse:
    user_exists = db.query(User).filter(User.email == data.email).first()
    if user_exists:
        raise EmailAlreadyExistsError("Email já cadastrado.")
    hashed_password = hash_password(data.password)
    new_user = User(
        name=data.name,
        email=data.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise EmailAlreadyExistsError("Email já cadastrado.")
    except Exception:
        db.rollback()
        raise
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: EmailStr, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user