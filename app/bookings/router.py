from typing import List

from fastapi import APIRouter, Request, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("/")
async def get_bookings(user: Users = Depends(get_current_user)): #-> List[SBooking]:  # Переделать валидацию после перехода на v2 pydantic с orm_mode на model_config
    return await BookingDAO.find_all(user_id=user.id)


# @router.get("/{booking_id}")
# def get_booking(booking_id: int):
#     pass