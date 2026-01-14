
from decimal import Decimal
from pydantic import BaseModel


class MonthSummaryResponse(BaseModel):
    month: str
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal

