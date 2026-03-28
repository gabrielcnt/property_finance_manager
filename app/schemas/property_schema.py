from typing import Optional

from pydantic import BaseModel, ConfigDict


class PropertyCreate(BaseModel):
    name: str


class PropertyUpdate(BaseModel):
    name: Optional[str] = None


class PropertyResponse(BaseModel):
    id: int
    name: str


model_config = ConfigDict(from_attributes=True)
