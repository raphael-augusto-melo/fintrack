from fastapi import APIRouter, Depends
from sqlalchemy import text
from app.core.db import get_db

router = APIRouter()

@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}

@router.get("/db-check")
def check_db_conn(db=Depends(get_db)) -> dict:
    try:
        db.execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception as e:
        return {"db": "disconnected", "error": str(e)}