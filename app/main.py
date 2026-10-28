from fastapi import Query, FastAPI
from typing import Optional
from datetime import date
from pydantic import BaseModel



app = FastAPI()

from app.bookings.router import router as bookings_router
from app.users.router import router as users_router

app.include_router(users_router)
app.include_router(bookings_router)


class SHotel(BaseModel):
    adress: str
    name: str
    stars: int


@app.get("/hotels")
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Optional[bool] = False,
        stars: Optional[int] = Query(None, ge=1, le=5),

):
    pass