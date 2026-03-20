from typing import List, Optional
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import UUID, Date, DateTime, Numeric, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.budget_domain import BudgetBucket, BudgetMethodology
from app.core.db import Base
from app.models.transaction import TransactionCategory

class BudgetTemplate(Base):
    __tablename__ = "budget_templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    methodology: Mapped[BudgetMethodology] = mapped_column(Enum(BudgetMethodology))
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
    methodology_used: Mapped[BudgetMethodology] = mapped_column(Enum(BudgetMethodology))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    categories: Mapped[List["MonthlyBudgetCategory"]] = relationship(back_populates="budget")

    __table_args__ = (
        UniqueConstraint("user_id", "month", name="uq_only_one_budget_per_user_in_a_month"),
        )


class MonthlyBudgetCategory(Base):
    __tablename__ = "monthly_budget_categories"
    

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    monthly_budget_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("monthly_budgets.id"), )
    category: Mapped[TransactionCategory] = mapped_column(Enum(TransactionCategory))
    budget_limit: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    bucket: Mapped[BudgetBucket] = mapped_column(Enum(BudgetBucket))
    budget: Mapped[MonthlyBudget] = relationship(back_populates="categories")
