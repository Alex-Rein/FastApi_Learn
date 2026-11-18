from fastapi import APIRouter, Depends
from starlette import status

from app.exceptions import UserIncorrectException, NoNeededFieldsException, FailedToAddException, \
    DeletionErrorException, RoomIsNotFoundException, FailedToUpdateException
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoomsCreate, SRoomsUpdate
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix='/hotels', tags=['Отели и номера'])


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: int):
    return await RoomsDAO.find_all_hotel_rooms(hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def add_hotel_room(
        data: SRoomsCreate,
        user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIncorrectException

    payload = data.model_dump(exclude_unset=True)
    if not payload:
        raise NoNeededFieldsException

    result = await RoomsDAO.add(
        **payload
    )

    if not result.status_code == (status.HTTP_201_CREATED or status.HTTP_200_OK):
        raise FailedToAddException

    return result


@router.delete("/{hotel_id}/rooms/{room_id}")
async def remove_hotel_room(
        hotel_id: int,
        room_id: int,
        user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIncorrectException

    hotel_room = RoomsDAO.find_by_id(room_id)
    if not hotel_room or hotel_room.hotel_id == hotel_id:
        raise RoomIsNotFoundException

    deleted =  await RoomsDAO.delete(room_id)
    if not deleted:
        raise DeletionErrorException


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_hotel_room(
        hotel_id: int,
        room_id: int,
        data: SRoomsUpdate,
        user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIncorrectException

    hotel_room = RoomsDAO.find_by_id(room_id)
    if not hotel_room or hotel_room.hotel_id == hotel_id:
        raise RoomIsNotFoundException

    payload = data.model_dump(exclude_unset=True)
    if not payload:
        raise NoNeededFieldsException

    updated = await RoomsDAO.update(
        room_id,
        **payload
    )

    if not updated:
        raise FailedToUpdateException

    return updated