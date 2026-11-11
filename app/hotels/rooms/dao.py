from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int):
        async with async_session_maker() as session:
            query = select(Rooms).where(Rooms.hotel_id == hotel_id)
            result = await session.execute(query)
            return result.scalars().all()