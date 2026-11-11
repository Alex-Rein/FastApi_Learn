from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import JSON

from app.exceptions import UserIncorrectException
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels
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
        name: str,
        location: str,
        services: Optional[JSON],
        rooms_quantity: int,
        image_id: Optional[int],
        user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIncorrectException

    hotel = HotelsDAO.add(
        name=name,
        location=location,
        services=services,
        rooms_quantity=rooms_quantity,
        image_id=image_id,
    )

    return hotel


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int,
        user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIncorrectException

    return await HotelsDAO.delete(hotel_id)


@router.put("/{hotel_id}")
async def update_hotel(         # TODO проверить и если нужно доделать распаковку данных для update
        hotel_id: int,
        name: Optional[str],
        location: Optional[str],
        services: Optional[JSON],
        rooms_quantity: Optional[int],
        image_id: Optional[int],
        user: Users = Depends(get_current_user)
):
    if not user:
        raise UserIncorrectException

    hotel = await HotelsDAO.update(
        hotel_id,
        name=name,
        location=location,
        services=services,
        rooms_quantity=rooms_quantity,
        image_id=image_id
    )

    return hotel