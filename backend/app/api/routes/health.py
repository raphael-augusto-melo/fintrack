from fastapi import APIRouter
from sqlalchemy import text, create_engine
from app.core.db import get_db

router = APIRouter()
db = next(get_db())

@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}

@router.get("/db-check")
def check_db_conn() -> dict:
    try:
        db.execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception as e:
        return {"db": "disconnected", "error": str(e)}