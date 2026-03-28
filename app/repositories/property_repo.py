from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.property import Property
from app.schemas.property_schema import PropertyCreate, PropertyUpdate


class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, new_property: PropertyCreate) -> Property:
        try:
            property = Property(name=new_property.name)

            self.db.add(property)
            self.db.commit()
            self.db.refresh(property)

            return property

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_all(self) -> list[Property]:
        return self.db.query(Property).all()

    def get_by_id(self, property_id: int) -> Property | None:

        property = self.db.query(Property).filter(Property.id == property_id).first()
        if not property:
            return None

        return property

    def update(
        self, property_id: int, property_update: PropertyUpdate
    ) -> Property | None:
        try:
            property = (
                self.db.query(Property).filter(Property.id == property_id).first()
            )
            if not property:
                return None

            if property_update.name is not None:
                property.name = property_update.name

            self.db.commit()
            self.db.refresh(property)

            return property

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, property_id: int) -> Property | None:
        try:
            property = (
                self.db.query(Property).filter(Property.id == property_id).first()
            )
            if not property:
                return None

            self.db.delete(property)
            self.db.commit()

            return property
        except SQLAlchemyError:
            self.db.rollback()
            raise
