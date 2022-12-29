from pydantic import BaseModel


class Login(BaseModel):
    user_name: str
    password: str


class Logout(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_name: str


class Auth(BaseModel):
    auth: bool
