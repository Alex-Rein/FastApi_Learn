from datetime import date

from sqlalchemy import select, func, and_, or_

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def search_for_hotels(
            cls,
            location: str,
            date_from: date | None,
            date_to: date | None,
    ):
        async with async_session_maker() as session:
            stmt = select(Hotels).where(Hotels.location.ilike(f'%{location}%'))

        # Если даты не переданы
            if date_from is None or date_to is None:
                result = await session.execute(stmt)
                return result.scalars().all()

        # Подзапрос: для каждого Room считаем, сколько броней пересекается с диапазоном
        overlapping_bookings = (
            select(
                Bookings.room_id,
                func.count(Bookings.id).label('booked'),
            )
            .where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from
                    )
                )
            )
            .group_by(Bookings.room_id)
            .subquery()
        )

        # Условие: существует Room этого отеля, у которого booked < quantity
        available_room_exists = (
            select(Rooms.id)
            .outerjoin(
                overlapping_bookings,
                overlapping_bookings.c.room_id == Rooms.id
            )
            .where(
                and_(
                    Rooms.hotel_id == Hotels.id,
                    func.coalesce(overlapping_bookings.c.booked, 0) < Rooms.quantity
                )
            )
            .exists()
        )

        stmt = stmt.where(available_room_exists)
        result = await session.execute(stmt)
        return result.scalars().all()