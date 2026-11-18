from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.exceptions import UserIncorrectException, NoNeededFieldsException, HotelIsNotFoundException, \
    FailedToAddException, FailedToUpdateException, WrongDateException
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels, SHotelsCreate, SHotelsUpdate
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix='/hotels', tags=['Отели и номера'])


@router.get("")
async def get_hotels_by_location_and_time(
        location: str = Query(None, description='Введите город или часть названия'),
        date_from: date = Query(None, description=f'Например, {datetime.now().date()}'),
        date_to: date = Query(None, description=f'Например, {datetime.now().date()}')
):
    if date_from and date_to and date_from >= date_to:
        raise WrongDateException

    hotels = await HotelsDAO.search_for_hotels(location, date_from, date_to)
    return hotels


@router.post("")
async def add_hotel(
        data: SHotelsCreate,
        user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIncorrectException

    payload = data.model_dump(exclude_unset=True)
    if not payload:
        raise NoNeededFieldsException

    result = await HotelsDAO.add(
        **payload
    )

    if not result.status_code == (status.HTTP_201_CREATED or status.HTTP_200_OK):
        raise FailedToAddException

    return result


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int,
        user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIncorrectException

    if not await HotelsDAO.delete(hotel_id):
        raise HotelIsNotFoundException


@router.patch("/{hotel_id}")
async def update_hotel(
        hotel_id: int,
        data: SHotelsUpdate,
        user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIncorrectException

    payload = data.model_dump(exclude_unset=True)
    if not payload:
        raise NoNeededFieldsException

    updated = await HotelsDAO.update(
        hotel_id,
        **payload
    )

    if not updated:
        raise FailedToUpdateException

    return updated