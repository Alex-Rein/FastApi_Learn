import datetime

from fastapi import Depends, Request
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import TokenExpiredException, TokenIsAbsentException, TokenIncorrectFormatException, \
    UserIncorrectException
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenIsAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise TokenIncorrectFormatException

    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.datetime.now(datetime.UTC).timestamp():
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIncorrectException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIncorrectException

    return user
