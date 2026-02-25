import enum
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
    if round(sum(buckets.values()), 10) != 1.0:
        raise ValueError("Soma dos valores dos buckets passou o limite de 100%")