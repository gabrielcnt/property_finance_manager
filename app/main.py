from fastapi import FastAPI

from app.api import test_router
from app.core.database import Base, engine
from app.models.test_table import TestTable


app = FastAPI()

app.include_router(test_router.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Rota de teste"}
