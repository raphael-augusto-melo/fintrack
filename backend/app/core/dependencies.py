from fastapi import Depends

from app.api.routes.auth import oauth2_scheme
from app.core.security import decode_access_token
from app.core.db import get_db
from app.models.user import User
from fastapi import HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        user_uuid = UUID(user_id)
        user = db.query(User).filter(User.id == user_uuid).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"}
        )
