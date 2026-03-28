from sqlalchemy import Column, Integer, String

from app.core.database import Base


class TestTable(Base):
    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_name = Column(String, nullable=True)
