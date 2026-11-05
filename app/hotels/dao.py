from app.dao.base import BaseDAO
from app.hotels.models import Hotels


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    def get_by_hotel_id(cls, hotel_id: int):
        pass

    @classmethod
    def find_all(cls):
        pass