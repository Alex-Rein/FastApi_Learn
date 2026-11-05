from fastapi import APIRouter


router = APIRouter(prefix='/hotels', tags=['Отели и номера'])

@router.get("")
def get_hotels():
    pass