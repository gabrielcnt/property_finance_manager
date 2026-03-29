from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.transactions import Transaction


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    modified_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now)

    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="property", cascade="all, delete-orphan"
    )
