from pydantic import BaseModel


class UserInDB(BaseModel):
    email           : str
    name            : str
    id_token        : str
    access_token    : str
    refresh_token   : str
    picture         : str
    locale          : str


class UserOutDB(BaseModel):
    email   : str
    name    : str
    picture : str
    locale  : str
