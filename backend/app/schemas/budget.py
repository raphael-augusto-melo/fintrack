from decimal import Decimal

from pydantic import BaseModel, field_validator

from app.models.budget import BudgetMethodology

class BudgetTemplateRequest(BaseModel):
    methodology: BudgetMethodology
    default_income: Decimal
    @field_validator('default_income', mode='before')
    @classmethod
    def validate_default_income(cls, di):
        if not di > 0:
            raise ValueError('default_income_must_be_bigger_than_zero')

class BudgetTemplateResponse:
    pass
