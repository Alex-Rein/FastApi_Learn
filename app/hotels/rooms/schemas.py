from typing import Optional

from pydantic import BaseModel, ConfigDict, Json


class SRoomsBase(BaseModel):
    hotel_id: int
    name: str
    description: str
    price: int
    services: Json
    quantity: int
    image_id: int = None


class SRoomsCreate(SRoomsBase):
    pass


class SRoomsUpdate(SRoomsBase):
    hotel_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    services: Optional[Json] = None
    quantity: Optional[int] = None
    image_id: Optional[int] = None



class SRooms(SRoomsBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
