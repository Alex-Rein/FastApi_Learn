from typing import Optional

from pydantic import BaseModel, ConfigDict, Json


class SHotelsBase(BaseModel):
    name: str
    location: str
    services: Optional[Json] = None
    rooms_quantity: int
    image_id: Optional[int] = None


class SHotelsCreate(SHotelsBase):
    pass


class SHotelsUpdate(SHotelsBase):
    name: Optional[str] = None
    location: Optional[str] = None
    services: Optional[Json] = None
    rooms_quantity: Optional[int] = None
    image_id: Optional[int] = None


class SHotels(SHotelsBase):
    id: int

    model_config = ConfigDict(from_attributes=True)