from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction_schema import TransactionType


class FinanceService:
    def __init__(self, transaction_repo: TransactionRepository):
        self.transaction_repo = transaction_repo

    def get_total_income(self) -> float:
        return self.transaction_repo.get_by_type(TransactionType.income)

    def get_total_expense(self) -> float:
        return self.transaction_repo.get_by_type(TransactionType.expense)

    def calculate_profit(self) -> float:
        return self.get_total_income() - self.get_total_expense()
