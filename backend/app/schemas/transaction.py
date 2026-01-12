from decimal import Decimal
from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel,field_validator
from app.models.transaction import TransactionCategory, TransactionType
from pydantic import ConfigDict


class TransactionCreate(BaseModel):
    type: TransactionType
    amount: Decimal
    description: Optional[str] = None
    occurred_at: datetime
    category: TransactionCategory

    @field_validator('amount', mode='after')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("amount_deve_ser_maior_que_zero")

        return v

class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    occurred_at: Optional[datetime] = None
    category: Optional[TransactionCategory] = None
    @field_validator('amount', mode='after')
    @classmethod
    def validate_amount(cls, v):
        if v is None:
            return v
        if v <= 0:
            raise ValueError("amount_deve_ser_maior_que_zero")

        return v

class TransactionResponse(BaseModel):
    id: UUID
    user_id: UUID
    type: TransactionType
    amount: Decimal
    description: Optional[str]
    created_at: datetime
    occurred_at: datetime
    category: TransactionCategory
    
    model_config = ConfigDict(from_attributes=True)