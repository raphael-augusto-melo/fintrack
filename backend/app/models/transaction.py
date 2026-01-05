from datetime import datetime
import uuid
import enum
from decimal import Decimal
from typing import Optional

from sqlalchemy import UUID, DateTime, Numeric, String, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, CheckConstraint

from app.core.db import Base

class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionCategory(enum.Enum):
    ALIMENTACAO = "alimentacao"
    ASSINATURA = "assinatura"
    TRANSPORTE = "transporte"
    LAZER = "lazer"
    SAUDE = "saude"
    OUTROS = "outros"

class Transaction(Base):
    __tablename__ = "transactions"

    __table_args__ = (
    CheckConstraint("amount > 0", name="ck_transactions_amount_positive"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), index=True, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    category: Mapped[Optional[TransactionCategory]] = mapped_column(Enum(TransactionCategory), nullable=True, index=True)