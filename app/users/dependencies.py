import datetime

from fastapi import Depends, Request, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.testing.pickleable import User

from app.config import settings
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    expire: str = payload.get("exp")
    print("==========================")
    print("==========================")
    print("expire =", expire)
    print("timestamp =", datetime.datetime.now(datetime.UTC).timestamp())
    print("==========================")
    print("==========================")
    if not expire or int(expire) < int(datetime.datetime.now(datetime.UTC).timestamp()):
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
