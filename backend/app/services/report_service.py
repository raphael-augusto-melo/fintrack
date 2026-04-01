from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Tuple
import re
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.services.exceptions import InvalidMonthFormatError
from app.models.user import User
from app.models.transaction import Transaction, TransactionType
from app.schemas.report import CategoryTotalItem, MonthSummaryResponse


def get_default_month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")

def get_month_range(month: str | None = None) -> Tuple[datetime, datetime]:
    if month is None:
        month = get_default_month()
    pattern = r"^\d{4}-(0[1-9]|1[0-2])$"
    if not re.match(pattern, month):
        raise InvalidMonthFormatError()
    parsed_month_range = month.split('-')
    parsed_year = int(parsed_month_range[0])
    parsed_month = int(parsed_month_range[1])

    start_dt = datetime(parsed_year, parsed_month, 1, tzinfo=timezone.utc)
    
    if parsed_month == 12:
        end_dt_exclusive = datetime(parsed_year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end_dt_exclusive = datetime(parsed_year, parsed_month + 1, 1, tzinfo=timezone.utc)
    
    return start_dt, end_dt_exclusive


def month_summary(db: Session, user: User, month: str | None = None) -> MonthSummaryResponse:
    start_dt, end_dt_exclusive = get_month_range(month)
    
    incomes = (
        db.query(func.sum(Transaction.amount))
        .filter(
            Transaction.user_id == user.id,
            Transaction.occurred_at >= start_dt,
            Transaction.occurred_at < end_dt_exclusive,
            Transaction.type == TransactionType.INCOME
        )
        .scalar()
        
    )

    if incomes is None:
        incomes = Decimal("0")

    expenses = (
        db.query(func.sum(Transaction.amount))
        .filter(
            Transaction.user_id == user.id,
            Transaction.occurred_at >= start_dt,
            Transaction.occurred_at < end_dt_exclusive,
            Transaction.type == TransactionType.EXPENSE
        )
        .scalar()
        
    )

    if expenses is None:
        expenses = Decimal("0")

    balance = incomes - expenses

    response = MonthSummaryResponse(
        month=month,
        total_income=incomes,
        total_expense=expenses,
        balance=balance
    )

    return response

def by_category_totals(db: Session, user: User, month: str, transaction_type: TransactionType = TransactionType.EXPENSE) -> List[CategoryTotalItem]:
    start_dt, end_dt_exclusive = get_month_range(month)
    q = (db.query(Transaction.category, func.sum(Transaction.amount))
         .filter(
            Transaction.user_id == user.id, 
            Transaction.type == transaction_type,
            Transaction.occurred_at >= start_dt, 
            Transaction.occurred_at < end_dt_exclusive
         )
         .group_by(Transaction.category)
         .order_by(func.sum(Transaction.amount).desc())
         .all()
        
        )
    if not q:
        return []
    result = []
    
    for line in q:
        category, total = line
        if total is None:
            total = Decimal("0")
        result.append(CategoryTotalItem(category=category, total=total))
    
    return result
