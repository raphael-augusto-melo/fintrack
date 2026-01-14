from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.transactions import router as transactions_router
from app.api.routes.reports import router as reports_router

from fastapi import APIRouter

router = APIRouter()
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(transactions_router)
router.include_router(reports_router)