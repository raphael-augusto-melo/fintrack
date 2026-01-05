from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(health_router)
router.include_router(auth_router)