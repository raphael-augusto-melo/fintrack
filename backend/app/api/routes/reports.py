from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.reports import MonthSummaryResponse
from app.services.exceptions import InvalidMonthFormatError
from app.services.report_service import month_summary


router = APIRouter(prefix='/reports', tags=['reports'])

@router.get('/month-summary', response_model=MonthSummaryResponse)
def get_month_summary_route(month: Optional[str] = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        if month is None:
            month = datetime.now(timezone.utc).strftime("%Y-%m")
        response = month_summary(db, user, month)
        return response
    
    except InvalidMonthFormatError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Mês no formato errado."
        )