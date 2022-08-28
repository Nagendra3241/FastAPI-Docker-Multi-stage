import os
import traceback
from typing import Any, NamedTuple

from pydantic import BaseModel
from config.logger import logger
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import requests
from features.users import users_controller, users_service
from features.users.users_service import UserInDB
from features.oauth.google import google_oauth_service
from jose import JWTError, jwt

class GoogleClientParams(NamedTuple):
    code: str
    client_id       : str | None = os.getenv("GOOGLE_CLIENT_ID")
    client_secret   : str | None = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri    : str | None = os.getenv("GOOGLE_REDIRECT_URI")
    grant_type      : str        = "authorization_code"
    
class GoogleUserInfoResponse(NamedTuple):
    email: str
    name: str
    picture: str
    locale: str

class GoogleOauthCode(BaseModel):
    code: str    


async def get_google_oauth_url():
    base = os.getenv("GOOGLE_AUTH_URL")  # https://accounts.google.com/o/oauth2/v2/auth

    url = f"""{base}?\
    redirect_uri={os.getenv("GOOGLE_REDIRECT_URI")}\
    &client_id={os.getenv("GOOGLE_CLIENT_ID")}\
    &access_type=offline\
    &response_type=code\
    &prompt=consent\
    &scope=https://www.googleapis.com/auth/userinfo.profile\
        +https://www.googleapis.com/auth/userinfo.email\
    """.strip().replace(" ", "")

    return {"oauth_url": str(url)}


async def get_google_session(body: GoogleOauthCode):

    access_code = body.code
    # Exchange CODE for TOKENS
    access_token, refresh_token, id_token = google_oauth_service.get_google_tokens(access_code=access_code)

    # Exchange TOKENS for USER_INFO
    try:
        user_info = await google_oauth_service.get_google_user(id_token, access_token)
        # Update or Insert User to DB
        new_user_db_info = UserInDB(
            **user_info.dict(),
            id_token = id_token,
            access_token = access_token,
            refresh_token = refresh_token
        )
        new_user = await users_controller.update_or_create_user(new_user_db_info)

        # Encode COOKIE
        jwt_token = jwt.encode(
            {
                "user_email": new_user.email,
                "id_token": new_user.id_token
            },
            str(os.getenv("JWT_SECRET")),
            algorithm="HS256"
        )

        # Set session COOKIE
        """  res.set_cookie(
                key="Authorization",
                value=f"Bearer NIGGA",
                httponly=True,
                secure=True,
                samesite="none",
                domain="https://now-me.herokuapp.com/",
                # max_age=user_tokens.get("expires_in"),
                # expires=user_tokens.get("expires_in"),
            ) """

        res = JSONResponse(content={"message": "OK"}, status_code=200)
        res.headers["Authorization"] = f"Bearer {jwt_token}"        
        return res


    except Exception:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Expand")