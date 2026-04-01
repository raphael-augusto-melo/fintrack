import enum
import math
from typing import List, Optional
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import UUID, Date, DateTime, Numeric, Enum as SAEnum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.transaction import TransactionCategory


class BudgetMethodology(enum.Enum):
    FIFTY_THIRTY_TWENTY = "FIFTY_THIRTY_TWENTY"
    SIXTY_TWENTY_TWENTY = "SIXTY_TWENTY_TWENTY"
    SIXTY_THIRTY_TEN = "SIXTY_THIRTY_TEN"

class BudgetBucket(enum.Enum):
    NEEDS = enum.auto()
    WANTS = enum.auto()
    SAVINGS = enum.auto()

METHODOLOGY_VALUES: dict[BudgetMethodology, dict[BudgetBucket, float]] = {
    BudgetMethodology.FIFTY_THIRTY_TWENTY: {
        BudgetBucket.NEEDS: 0.5,
        BudgetBucket.WANTS: 0.3,
        BudgetBucket.SAVINGS: 0.2
    },
    BudgetMethodology.SIXTY_TWENTY_TWENTY: {
        BudgetBucket.NEEDS: 0.6,
        BudgetBucket.WANTS: 0.2,
        BudgetBucket.SAVINGS: 0.2
    },
    BudgetMethodology.SIXTY_THIRTY_TEN: {
        BudgetBucket.NEEDS: 0.6,
        BudgetBucket.WANTS: 0.3,
        BudgetBucket.SAVINGS: 0.1
    }
}

CATEGORY_MAPPINGS: dict[TransactionCategory, BudgetBucket] = {
    TransactionCategory.ALIMENTACAO: BudgetBucket.NEEDS,
    TransactionCategory.ASSINATURA: BudgetBucket.NEEDS,
    TransactionCategory.INVESTIMENTOS: BudgetBucket.SAVINGS,
    TransactionCategory.LAZER: BudgetBucket.WANTS,
    TransactionCategory.OUTROS: BudgetBucket.WANTS,
    TransactionCategory.SAUDE: BudgetBucket.NEEDS,
    TransactionCategory.TRANSPORTE: BudgetBucket.NEEDS
}

for mtd, buckets in METHODOLOGY_VALUES.items():
    if not math.isclose(sum(buckets.values()), 1.0):
        raise ValueError("Soma dos valores dos buckets passou o limite de 100%")

class BudgetTemplate(Base):
    __tablename__ = "budget_templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    methodology: Mapped[BudgetMethodology] = mapped_column(SAEnum(BudgetMethodology))
    default_income: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class MonthlyBudget(Base):
    __tablename__ = "monthly_budgets"


    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    template_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("budget_templates.id", ondelete="SET NULL"), nullable=True)
    month: Mapped[date] = mapped_column(Date())
    income_used: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    methodology_used: Mapped[BudgetMethodology] = mapped_column(SAEnum(BudgetMethodology))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    categories: Mapped[List["MonthlyBudgetCategory"]] = relationship(back_populates="budget")

    __table_args__ = (
        UniqueConstraint("user_id", "month", name="uq_only_one_budget_per_user_in_a_month"),
        )


class MonthlyBudgetCategory(Base):
    __tablename__ = "monthly_budget_categories"
    

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    monthly_budget_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("monthly_budgets.id"), )
    category: Mapped[TransactionCategory] = mapped_column(SAEnum(TransactionCategory))
    budget_limit: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    bucket: Mapped[BudgetBucket] = mapped_column(SAEnum(BudgetBucket))
    budget: Mapped[MonthlyBudget] = relationship(back_populates="categories")
