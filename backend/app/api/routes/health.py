from fastapi import APIRouter
from sqlalchemy import text, create_engine
from app.core.settings import settings

router = APIRouter()
engine = create_engine(settings.DATABASE_URL, echo=True)

@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}

@router.get("/db-check")
def check_db_conn() -> dict:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception as e:
        return {"db": "disconnected", "error": str(e)}