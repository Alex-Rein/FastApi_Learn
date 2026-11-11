from fastapi import Query, FastAPI
from typing import Optional
from datetime import date
from pydantic import BaseModel


from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
from app.hotels.router import router as hotels_router
from app.hotels.rooms.router import router as rooms_router


app = FastAPI()

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)


# class SHotel(BaseModel):
#     address: str
#     name: str
#     stars: int


# @app.get("/hotels")
# def get_hotels(
#         location: str,
#         date_from: date,
#         date_to: date,
#         has_spa: Optional[bool] = False,
#         stars: Optional[int] = Query(None, ge=1, le=5),
#
# ):
#     pass