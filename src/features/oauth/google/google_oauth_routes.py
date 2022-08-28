from fastapi import APIRouter
from features.oauth.google import google_oauth_controller
from typing import Any
from pydantic import BaseModel


GOOGLE_OAUTH_ROUTER = APIRouter()

class GoogleOauthURLResponse(BaseModel):
    oauth_url: str

class GoogleOauthSessionResponse(BaseModel):
    message: str = "OK"  

GOOGLE_OAUTH_ROUTER.add_api_route(path="/google/url",
                            methods=["GET"],
                            endpoint=google_oauth_controller.get_google_oauth_url,
                            tags=["Google Oauth"],
                            response_model=GoogleOauthURLResponse
                        )                        
GOOGLE_OAUTH_ROUTER.add_api_route(path="/google/session",
                            methods=["POST"],
                            endpoint=google_oauth_controller.get_google_session,
                            tags=["Google Oauth"],
                            response_model=GoogleOauthSessionResponse,
                        )                