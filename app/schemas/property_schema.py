from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def normalize_name(value: str) -> str:

    value = value.strip().title()

    if not value:
        raise ValueError("Nome é obrigatório")

    return value


class PropertyCreate(BaseModel):
    name: str = Field(min_length=1)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if value is None:
            return value

        clean_value: str = value

        return normalize_name(clean_value)


class PropertyUpdate(BaseModel):
    name: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        clean_value: str = value

        return normalize_name(clean_value)


class PropertyResponse(BaseModel):
    id: int
    name: str


model_config = ConfigDict(from_attributes=True)
