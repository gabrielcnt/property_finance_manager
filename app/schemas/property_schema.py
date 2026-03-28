from pydantic import BaseModel, ConfigDict


class PropertyCreate(BaseModel):
    name: str


class PropertyResponse(BaseModel):
    id: int
    name: str


model_config = ConfigDict(from_attributes=True)
