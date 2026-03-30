from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.property import Property
from app.schemas.property_schema import PropertyCreate, PropertyUpdate


class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, new_property: PropertyCreate) -> Property:
        try:
            property_obj = Property(name=new_property.name)

            self.db.add(property_obj)
            self.db.commit()
            self.db.refresh(property_obj)

            return property_obj

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_all(self) -> list[Property]:
        return self.db.query(Property).all()

    def get_by_id(self, property_id: int) -> Property | None:

        property_obj = (
            self.db.query(Property).filter(Property.id == property_id).first()
        )

        return property_obj

    def get_by_name(self, property_name: str) -> Property | None:
        return self.db.query(Property).filter(Property.name == property_name).first()

    def update(self, property: Property, property_update: PropertyUpdate) -> Property:
        try:
            update_data = property_update.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(property, key, value)

            self.db.commit()
            self.db.refresh(property)

            return property

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, property_id: int) -> Property | None:
        try:
            property_obj = (
                self.db.query(Property).filter(Property.id == property_id).first()
            )

            self.db.delete(property_obj)
            self.db.commit()

            return property_obj
        except SQLAlchemyError:
            self.db.rollback()
            raise
