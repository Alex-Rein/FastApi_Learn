from fastapi import HTTPException, status


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь с таким именем уже существует"
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Указаны неправильная почта или пароль'
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Срок действия токена истек"
)

TokenIsAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = 'Токен отсутствует'
)

TokenIncorrectFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неправильный формат токена"
)

UserIncorrectException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token"
)