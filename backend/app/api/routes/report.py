from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.transaction import TransactionType
from app.models.user import User
from app.schemas.report import CategoryTotalItem, MonthSummaryResponse
from app.services.exceptions import InvalidMonthFormatError
from app.services.report_service import by_category_totals, month_summary


router = APIRouter(prefix='/reports', tags=['reports'])

@router.get('/month-summary', response_model=MonthSummaryResponse)
def get_month_summary_route(month: Optional[str] = Query(None), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        month_summary_response = month_summary(db, user, month)
        return month_summary_response
    except InvalidMonthFormatError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.detail
        )

@router.get("/by-category", response_model=List[CategoryTotalItem])
def get_by_category_route(
    month: Optional[str] = Query(None),
    transaction_type: TransactionType = Query(
        TransactionType.EXPENSE,
        description="Tipo de transação a considerar"
    ),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        totals = by_category_totals(db, user, month, transaction_type)
        return totals
    except InvalidMonthFormatError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.detail
        )