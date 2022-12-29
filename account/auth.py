from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .connection import ConnectToKeycloak
from account import types


openid = ConnectToKeycloak().keycloak_openid
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def user(access_token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        userinfo = openid.userinfo(access_token)
        auth_status = openid.has_uma_access(access_token, "Default Resource")
        if not auth_status.is_logged_in:
            raise credentials_exception
        return userinfo['preferred_username']
    except Exception as ex:
        raise credentials_exception


def login(username: str, password: str):
    try:
        token = openid.token(username, password)
        formatted_token = types.Token(access_token=token['access_token'], refresh_token=token['refresh_token'], token_type=token['token_type'], user_name=username)
        return formatted_token
    except Exception as ex:
        raise HTTPException(status_code=401, detail="Logged in Failed")


def logout(logout: types.Logout):
    try:
        openid.logout(logout.refresh_token)
        return "Logged out successfully"
    except:
        raise HTTPException(status_code=401, detail="Logged out abnormally")


def get_user_info(token: types.Token):
    try:
        userinfo = openid.userinfo(token.access_token)
        return userinfo
    except:
        raise HTTPException(status_code=401, detail="XXXXX")
