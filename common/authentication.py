"""
https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/
官方文档中推荐的jwt认证方式
"""
from datetime import timedelta
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from tortoise.exceptions import DoesNotExist

from apps.account.models.db import User
from common.exceptions import JWTTokenError
from common.utils import get_current_time
from conf.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES
TOKEN_URL = settings.TOKEN_URL

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL, auto_error=False)
AUTH_USER_MODEL = User


async def get_user(user_id: str) -> AUTH_USER_MODEL | None:
    try:
        user = await AUTH_USER_MODEL.get(id=user_id)
    except DoesNotExist:
        return None
    else:
        return user


async def authenticate_user(username: str, password: str) -> AUTH_USER_MODEL:
    user = await AUTH_USER_MODEL.get(username=username)
    if not user:
        raise JWTTokenError.InvalidUserError
    verify_result = await user.verify_password(password)
    if not verify_result:
        raise JWTTokenError.InvalidPasswordError
    return user


def create_token(
    data: dict[str, Any],
    access_token_expires_delta: timedelta | None = None,
    refresh_token_expires_delta: timedelta | None = None,
) -> dict[str, Any]:
    to_encode = data.copy()
    current_time = get_current_time()
    if access_token_expires_delta:
        access_token_expire = current_time + access_token_expires_delta
    else:
        access_token_expire = current_time + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    # 设置访问token过期时间
    to_encode.update({"exp": access_token_expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    if refresh_token_expires_delta:
        refresh_token_expire = current_time + refresh_token_expires_delta
    else:
        refresh_token_expire = current_time + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )
    # 设置刷新token过期时间
    to_encode.update({"exp": refresh_token_expire})
    to_encode.update({"grant_type": "refresh_token"})
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    output = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": access_token_expire,
    }
    return output


def refresh_token_to_access_token(refresh_token: str) -> dict[str, Any]:
    """刷新token换取access_token"""
    try:
        current_time = get_current_time()
        # 从刷新token中提取信息转换为访问token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        grant_type = payload.pop("grant_type", None)
        if grant_type != "refresh_token":
            raise JWTTokenError.InvalidRefreshTokenError
        else:
            expires_in = payload["exp"] = current_time + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
            access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": access_token, "expires_in": expires_in}
    except JWTError:
        raise JWTTokenError.InvalidRefreshTokenError from None


async def need_access_token(
    token: str = Depends(oauth2_scheme),  # noqa: B008
) -> AUTH_USER_MODEL:
    if not token:
        raise JWTTokenError.InvalidAccessTokenError
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if payload.get("grant_type") == "refresh_token":
            raise JWTTokenError.InvalidAccessTokenError
        if user_id is None:
            raise JWTTokenError.InvalidAccessTokenError
    except JWTError:
        raise JWTTokenError.InvalidAccessTokenError from None
    user = await get_user(user_id)
    if not user:
        raise JWTTokenError.InvalidAccessTokenError
    elif isinstance(user, AUTH_USER_MODEL) and user.disabled:
        raise JWTTokenError.InvalidUserError
    return user


async def selectable_access_token(
    token: str = Depends(oauth2_scheme),  # noqa: B008
) -> AUTH_USER_MODEL | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if payload.get("grant_type") == "refresh_token":
            raise JWTTokenError.InvalidAccessTokenError
        if user_id is None:
            raise JWTTokenError.InvalidAccessTokenError
    except JWTError:
        raise JWTTokenError.InvalidAccessTokenError from None
    user = await get_user(user_id)
    if not user:
        raise JWTTokenError.InvalidAccessTokenError
    elif isinstance(user, AUTH_USER_MODEL) and user.disabled:
        raise JWTTokenError.InvalidUserError
    return user
