from fastapi import FastAPI

from app.api import finance_routes, property_routes, test_router, transaction_routers
from app.core.database import Base, engine
from app.models.property import Property  # noqa: F401
from app.models.test_table import TestTable  # noqa: F401
from app.models.transactions import Transaction  # noqa: F401

app = FastAPI()

app.include_router(test_router.router)
app.include_router(property_routes.router)
app.include_router(transaction_routers.router)
app.include_router(finance_routes.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> dict:
    return {"message": "Rota de teste"}
