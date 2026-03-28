from app.models.property import Property
from app.repositories.property_repo import PropertyRepository
from app.schemas.property_schema import PropertyCreate, PropertyUpdate


class ExistingNameError(Exception):
    pass


class PropertyNoFoundError(Exception):
    pass


class PropertyService:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository

    def create_property(self, new_property: PropertyCreate) -> Property:

        if new_property.name is not None:
            existing_name = self.repository.get_by_name(new_property.name)

        if existing_name:
            raise ExistingNameError("Já existe um imóvel com esse nome")

        return self.repository.create(new_property)

    def list_properties(self) -> list[Property]:
        return self.repository.get_all()

    def update_property(
        self, property_id: int, property_update: PropertyUpdate
    ) -> Property:
        property = self.repository.get_by_id(property_id)

        if property is None:
            raise PropertyNoFoundError("Imóvel não encontrado")

        if property_update.name is not None:
            existing_name = self.repository.get_by_name(property_update.name)

            if existing_name and existing_name.id != property_id:
                raise ExistingNameError("Já existe um imóvel com esse nome")

        return self.repository.update(property, property_update)

    def delete_property(self, property_id: int) -> Property | None:
        property = self.repository.get_by_id(property_id)

        if not property:
            raise PropertyNoFoundError("Imóvel não encontrado")

        return self.repository.delete(property_id)
