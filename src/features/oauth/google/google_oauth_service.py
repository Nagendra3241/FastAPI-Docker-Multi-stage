import os
import traceback
from typing import Any
from pydantic import BaseModel
from config.logger import logger
from fastapi.exceptions import HTTPException
import requests


class GoogleClientParams(BaseModel):
    code: str
    client_id: str | None = os.getenv("GOOGLE_CLIENT_ID")
    client_secret: str | None = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri: str | None = os.getenv("GOOGLE_REDIRECT_URI")
    grant_type: str = "authorization_code"


class GoogleUserInfoResponse(BaseModel):
    email: str
    name: str
    picture: str
    locale: str


def get_google_tokens(access_code: str):
    token_url = os.getenv("GOOGLE_TOKEN_URL")  # https://oauth2.googleapis.com/token
    params = GoogleClientParams(
        code=access_code
        # ... defaults
    )
    response = requests.post(str(token_url),
                             params=params.dict(),
                             headers={"Content-Type": "application/x-www-form-url-encoded"})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error while trying to request exchange of code for tokens")

    user_tokens = response.json()

    return user_tokens.get("access_token"), user_tokens.get("refresh_token"), user_tokens.get("id_token"),


async def get_google_user(id_token: str, access_token: str) -> GoogleUserInfoResponse:

    url = os.getenv("GOOGLE_USER_INFO_URL")  # https://www.googleapis.com/oauth2/v1/userinfo
    params = {
        "alt": "json",
        "access_token": access_token
    }
    headers = {
        "Authorization": f"Bearer {id_token}"
    }

    response = requests.get(str(url), headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Expand")

    try:
        user_info = response.json()
        return GoogleUserInfoResponse(
            email=user_info.get("email"),
            name=user_info.get("name"),
            picture=user_info.get("picture"),
            locale=user_info.get("locale")
        )

    except requests.JSONDecodeError:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Json decoded error")
