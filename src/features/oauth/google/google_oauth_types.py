import os
from pydantic import BaseModel

class GoogleClientParams(BaseModel):
    code: str
    client_id       : str | None = os.getenv("GOOGLE_CLIENT_ID")
    client_secret   : str | None = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri    : str | None = os.getenv("GOOGLE_REDIRECT_URI")
    grant_type      : str        = "authorization_code"
    
class GoogleUserInfoResponse(BaseModel):
    email   : str
    name    : str
    picture : str
    locale  : str

class GoogleOauthCode(BaseModel):
    code: str   