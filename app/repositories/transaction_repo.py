from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.transactions import Transaction
from app.schemas.transaction_schema import TransactionCreate, TransactionUpdate


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, new_transaction: TransactionCreate) -> Transaction:
        try:
            transaction = Transaction(new_transaction.model_dump())

            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)

            return transaction

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        return (
            self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
        )

    def get_all(self) -> list[Transaction]:
        return self.db.query(Transaction).all()

    def update(
        self, transaction: Transaction, update: TransactionUpdate
    ) -> Transaction:
        try:
            update_data = update.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(transaction, key, value)

            self.db.commit()
            self.db.refresh(transaction)

            return transaction

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, transaction_id: int) -> Transaction | None:
        try:
            transaction = (
                self.db.query(Transaction)
                .filter(Transaction.id == transaction_id)
                .first()
            )

            self.db.delete(transaction)
            self.db.commit()

            return transaction

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_by_filtered(
        self,
        property_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[Transaction]:

        query = self.db.query(Transaction)

        if property_id is not None:
            query = query.filter(Transaction.property_id == property_id)

        if start_date is not None and end_date is not None:
            query = query.filter(Transaction.date.between(start_date, end_date))

        return query.all()
