from datetime import date
from typing import Optional, Dict

from fastapi import APIRouter, Depends, Query
from pydantic import Json

from app.exceptions import UserIncorrectException, NoNeededFieldsException, HotelIsNotFoundException
from app.hotels.dao import HotelsDAO
from app.hotels.models import Hotels
from app.hotels.schemas import SHotels, SHotelsCreate, SHotelsUpdate
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix='/hotels', tags=['Отели и номера'])


@router.get("")
async def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Optional[bool] = False,
        stars: Optional[int] = Query(None, ge=1, le=5)
):

    return await HotelsDAO.find_all(
        location=location,
        date_from=date_from,
        date_to=date_to,
        has_spa=has_spa,
        stars=stars
    )


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

    hotel = await HotelsDAO.add(
        **payload
    )

    return hotel


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int,
        user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIncorrectException

    result = await HotelsDAO.delete(hotel_id)
    if not result:
        raise HotelIsNotFoundException

    return result


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
        raise HotelIsNotFoundException

    return updated