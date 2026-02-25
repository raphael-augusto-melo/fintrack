import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import UUID, DateTime, Numeric, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.budget_domain import BudgetMethodology
from app.core.db import Base

class BudgetTemplate(Base):
    __tablename__ = "budget_templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    methodology: Mapped[BudgetMethodology] = mapped_column(Enum(BudgetMethodology))
    default_income: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
