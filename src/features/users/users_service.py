from typing import Any
from .users_types import UserInDB, UserOutDB
from features.users.users_schema import User
from config.logger import logger


async def create_user(user: UserInDB) -> User:
    return await User.create(**user.dict())


async def update_user(user: UserInDB, user_in_db: User) -> User:
    await user_in_db.save()  # Triggers update_at TS field when on auto_now=True
    return user_in_db.update_from_dict({**user.dict()})


async def get_user(decoded_user: dict[str, Any]):  # USerInDB

    user = await User.filter(email=decoded_user.get("user_email")).first()

    if user:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "picture": user.picture,
            "locale": user.locale
        }


async def get_user_by_id(id: str) -> UserOutDB | None:

    user = await User.filter(id=id).first()

    if user:
        return UserOutDB(**{
            "name": user.name,
            "email": user.email,
            "picture": user.picture,
            "locale": user.locale
        })
