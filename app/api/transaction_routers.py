from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.property_repo import PropertyRepository
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction_schema import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from app.services.transaction_service import (
    AmountZeroError,
    DateInconsistencyError,
    PropertyNotFoundError,
    TransactionNotFoundError,
    TransactionService,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    new_transaction: TransactionCreate, db: Session = Depends(get_db)
) -> TransactionResponse:
    try:
        property_repo = PropertyRepository(db)
        transaction_repo = TransactionRepository(db)
        transaction_service = TransactionService(transaction_repo, property_repo)

        return transaction_service.create(new_transaction)

    except AmountZeroError as err:
        raise HTTPException(
            status_code=400, detail="O valor não pode ser menor que zero"
        ) from err

    except DateInconsistencyError as err:
        raise HTTPException(
            status_code=400, detail="A data de inicio deve ser menor que a final"
        ) from err

    except PropertyNotFoundError as err:
        raise HTTPException(
            status_code=404, detail="O imóvel não foi encontrado"
        ) from err

    except TransactionNotFoundError as err:
        raise HTTPException(status_code=404, detail="Transação não encontrada") from err


@router.patch("/{transaction_id}", response_model=TransactionResponse, status_code=200)
def update_transaction(
    transaction_id: int, update: TransactionUpdate, db: Session = Depends(get_db)
) -> TransactionResponse:
    try:
        property_repo = PropertyRepository(db)
        transaction_repo = TransactionRepository(db)
        transaction_service = TransactionService(transaction_repo, property_repo)

        return transaction_service.update(transaction_id, update)

    except AmountZeroError as err:
        raise HTTPException(
            status_code=400, detail="O valor não pode ser menor que zero"
        ) from err

    except DateInconsistencyError as err:
        raise HTTPException(
            status_code=400, detail="A data de inicio deve ser menor que a final"
        ) from err

    except PropertyNotFoundError as err:
        raise HTTPException(
            status_code=404, detail="O imóvel não foi encontrado"
        ) from err

    except TransactionNotFoundError as err:
        raise HTTPException(status_code=404, detail="Transação não encontrada") from err


@router.delete("/{transaction_id}", status_code=200)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        property_repo = PropertyRepository(db)
        transaction_repo = TransactionRepository(db)
        transaction_service = TransactionService(transaction_repo, property_repo)
        transaction_service.delete(transaction_id)

        return {"message": "Transação excluida com sucesso"}

    except TransactionNotFoundError as err:
        raise HTTPException(status_code=404, detail="Transação não encontrada") from err


@router.get("/", response_model=list[TransactionResponse], status_code=200)
def list_filter_transactions(
    property_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
) -> list:
    property_repo = PropertyRepository(db)
    transaction_repo = TransactionRepository(db)
    transaction_service = TransactionService(transaction_repo, property_repo)
    transactions = transaction_service.list_transactions(
        property_id, start_date, end_date
    )
    return [TransactionResponse.model_validate(tx) for tx in transactions]


@router.get("/{transaction_id}", response_model=TransactionResponse, status_code=200)
def list_transaction_by_id(
    transaction_id: int, db: Session = Depends(get_db)
) -> TransactionResponse:
    property_repo = PropertyRepository(db)
    transaction_repo = TransactionRepository(db)
    transaction_service = TransactionService(transaction_repo, property_repo)

    return transaction_service.get_transaction_by_id(transaction_id)
