
from decimal import Decimal
from pydantic import BaseModel

from app.models.transaction import TransactionCategory


class MonthSummaryResponse(BaseModel):
    month: str
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal

class CategoryTotalItem(BaseModel):
    category: TransactionCategory
    total: Decimal