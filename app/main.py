from fastapi import FastAPI

from app.api import property_routes, test_router
from app.core.database import Base, engine
from app.models.property import Property  # noqa: F401
from app.models.test_table import TestTable  # noqa: F401

app = FastAPI()

app.include_router(test_router.router)
app.include_router(property_routes.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> dict:
    return {"message": "Rota de teste"}
