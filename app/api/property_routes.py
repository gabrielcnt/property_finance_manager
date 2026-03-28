from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.property_repo import PropertyRepository
from app.schemas.property_schema import PropertyCreate, PropertyResponse, PropertyUpdate
from app.services.property_service import (
    ExistingNameError,
    PropertyNoFoundError,
    PropertyService,
)

router = APIRouter(prefix="/properties", tags=["properties"])


@router.post("/", response_model=PropertyResponse, status_code=201)
def create_property(
    new_property: PropertyCreate, db: Session = Depends(get_db)
) -> PropertyResponse:
    try:
        property_repo = PropertyRepository(db)
        property_service = PropertyService(property_repo)

        return property_service.create_property(new_property)

    except ExistingNameError as err:
        raise HTTPException(
            status_code=409, detail="Já existe um imóvel com esse nome"
        ) from err

    except PropertyNoFoundError as err:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado") from err


@router.get("/", response_model=list[PropertyResponse], status_code=200)
def list_properties(db: Session = Depends(get_db)) -> list:

    property_repo = PropertyRepository(db)
    property_service = PropertyService(property_repo)

    return property_service.list_properties()


@router.put("/{property_id}", response_model=PropertyResponse, status_code=200)
def update_property(
    property_id: int, property_update: PropertyUpdate, db: Session = Depends(get_db)
) -> PropertyResponse:
    try:
        property_repo = PropertyRepository(db)
        property_service = PropertyService(property_repo)

        return property_service.update_property(property_id, property_update)

    except PropertyNoFoundError as err:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado") from err

    except ExistingNameError as err:
        raise HTTPException(
            status_code=409, detail="Já existe um imóvel com esse nome"
        ) from err


@router.delete("/{property_id}", status_code=200)
def delete_property(property_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        property_repo = PropertyRepository(db)
        property_service = PropertyService(property_repo)

        property_service.delete_property(property_id)

        return {"message": "Imóvel deletado com sucesso"}
    except PropertyNoFoundError as err:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado") from err
