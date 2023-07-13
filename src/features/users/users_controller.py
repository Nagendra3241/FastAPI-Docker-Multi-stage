import os
from fastapi import Request, HTTPException, status
from features.users.users_schema import User
from features.users import users_service
from features.users.users_types import UserInDB
from app_config.logger import logger
from database.config import TORTOISE_ORM
from jose import JWTError, jwt


async def get_current_user(req: Request):

    jwt_token = req.headers.get("Authorization")

    if not jwt_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        decoded_user = jwt.decode(jwt_token.split("Bearer ")[1], str(os.getenv('JWT_SECRET')))
        return await users_service.get_user(decoded_user)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def update_or_create_user(user: UserInDB) -> User:

    user_in_db = await User.filter(email=user.email).first()
    if not user_in_db:
        return await users_service.create_user(user=user)
    return await users_service.update_user(user=user, user_in_db=user_in_db)


async def get_user_by_id(id: str):

    logger.debug(f" loggin in controller!!! {id} ")

    return await users_service.get_user_by_id(id)
