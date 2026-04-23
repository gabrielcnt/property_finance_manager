from app.models.transactions import Transaction
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

    def calculate_tax(self, amount: float, fee: float | None) -> float:

        if fee is None:
            return 0.0

        return amount * (fee / 100)

    def calculate_net_amount(self, transaction: Transaction) -> float:
        rate = self.calculate_tax(transaction.amount, transaction.platform_fee_percent)
        net_amount = transaction.amount - rate
        return net_amount

    def get_total_net_income(self) -> float:
        return self.transaction_repo.get_total_net_income()

    def calculate_net_profit(self) -> float:
        return self.get_total_net_income() - self.get_total_expense()
