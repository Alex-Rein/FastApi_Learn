from fastapi import APIRouter
from app.hotels.rooms.dao import RoomsDAO


router = APIRouter(prefix='/hotels', tags=['Отели и номера'])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    return await RoomsDAO.find_all(hotel_id=hotel_id)
