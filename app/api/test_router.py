from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db


router = APIRouter()

@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {'message': "DB conectado com sucesso"}