from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


def validate_amount(value: float) -> float:
    if value < 0:
        raise ValueError("Valor deve ser maior que zero")
    return value


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class TransactionCreate(BaseModel):
    property_id: int
    type: TransactionType
    amount: float
    category: Optional[str] = None
    platform: Optional[str] = None
    platform_fee_percent: Optional[float] = None
    description: Optional[str] = None
    date: datetime

    @field_validator("amount")
    @classmethod
    def validate_amount_field(cls, value: float) -> float:
        return validate_amount(value)


class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    platform: Optional[str] = None
    platform_fee_percent: Optional[float] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

    @field_validator("amount")
    @classmethod
    def validate_amount_field(cls, value: Optional[float]) -> Optional[float]:
        if value is None:
            return value
        return validate_amount(value)


class TransactionResponse(BaseModel):
    id: int
    property_id: int
    type: TransactionType
    amount: float
    category: Optional[str]
    platform: Optional[str]
    platform_fee_percent: Optional[float]
    description: Optional[str]
    date: datetime
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True)
