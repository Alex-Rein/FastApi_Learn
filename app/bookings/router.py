from typing import List

from fastapi import APIRouter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("/")
async def get_bookings() -> List[SBooking]:  # Переделать валидацию после перехода на v2 pydantic с orm_mode на model_config
    return await BookingDAO.find_all()


# @router.get("/{booking_id}")
# def get_booking(booking_id: int):
#     pass