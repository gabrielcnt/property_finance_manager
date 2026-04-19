from app.models.property import Property
from app.repositories.property_repo import PropertyRepository
from app.schemas.property_schema import PropertyCreate, PropertyUpdate


class ExistingNameError(Exception):
    pass


class PropertyNotFoundError(Exception):
    pass


class PropertyService:
    def __init__(self, repository: PropertyRepository):
        self.property_repo = repository

    def create_property(self, new_property: PropertyCreate) -> Property:

        if new_property.name is not None:
            existing_name = self.property_repo.get_by_name(new_property.name)

        if existing_name:
            raise ExistingNameError("Já existe um imóvel com esse nome")

        return self.property_repo.create(new_property)

    def list_properties(self) -> list[Property]:
        return self.property_repo.get_all()

    def get_property_by_id(self, property_id: int) -> Property:
        property_obj = self.property_repo.get_by_id(property_id)

        if property_obj is None:
            raise PropertyNotFoundError("Imóvel não encontrado")

        return property_obj

    def update_property(
        self, property_id: int, property_update: PropertyUpdate
    ) -> Property:
        property_obj = self.property_repo.get_by_id(property_id)

        if property_obj is None:
            raise PropertyNotFoundError("Imóvel não encontrado")

        if property_update.name is not None:
            existing_name = self.property_repo.get_by_name(property_update.name)

            if existing_name and existing_name.id != property_id:
                raise ExistingNameError("Já existe um imóvel com esse nome")

        return self.property_repo.update(property_obj, property_update)

    def delete_property(self, property_id: int) -> Property | None:
        property_obj = self.property_repo.get_by_id(property_id)

        if not property_obj:
            raise PropertyNotFoundError("Imóvel não encontrado")

        return self.property_repo.delete(property_id)
