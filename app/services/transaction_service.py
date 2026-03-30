from datetime import datetime
from typing import Optional

from app.models.transactions import Transaction
from app.repositories.property_repo import PropertyRepository
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction_schema import TransactionCreate, TransactionUpdate


class AmountZeroError(Exception):
    pass


class PropertyNotFoundError(Exception):
    pass


class TransactionNotFoundError(Exception):
    pass


class DateInconsistencyError(Exception):
    pass


class TransactionService:
    def __init__(
        self, transaction_repo: TransactionRepository, property_repo: PropertyRepository
    ):
        self.transaction_repo = transaction_repo
        self.property_repo = property_repo

    def create(self, new_transaction: TransactionCreate) -> Transaction:

        if new_transaction.amount <= 0:
            raise AmountZeroError("O valor não pode ser menor que zero")

        property_obj = self.property_repo.get_by_id(new_transaction.property_id)

        if property_obj is None:
            raise PropertyNotFoundError("O imóvel não foi encontrado")

        return self.transaction_repo.create(new_transaction)

    def update(self, transaction_id: int, update: TransactionUpdate) -> Transaction:

        transaction = self.transaction_repo.get_by_id(transaction_id)

        if transaction is None:
            raise TransactionNotFoundError("Transação não encontrada")

        if update.amount is not None and update.amount <= 0:
            raise AmountZeroError("O valor não pode ser menor que zero")

        return self.transaction_repo.update(transaction, update)

    def delete(self, transaction_id: int) -> Transaction:

        transaction = self.transaction_repo.get_by_id(transaction_id)

        if transaction is None:
            raise TransactionNotFoundError("Transação não encontrada")

        return self.transaction_repo.delete(transaction)

    def list_transactions(
        self,
        property_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> list[Transaction]:

        if property_id is not None:
            property_obj = self.property_repo.get_by_id(property_id)

            if property_obj is None:
                raise PropertyNotFoundError("O imóvel não foi encontrado")

        if start_date is not None and end_date is not None:
            if start_date > end_date:
                raise DateInconsistencyError(
                    "A data de inicio deve ser menor que a final"
                )

        transactions = self.transaction_repo.get_by_filtered(
            property_id=property_id, start_date=start_date, end_date=end_date
        )

        return transactions
