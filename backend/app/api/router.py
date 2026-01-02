from app.api.routes import health_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(health_router)