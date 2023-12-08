from datetime import datetime

import pytz
from passlib.context import CryptContext

from conf.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
global_timezone = pytz.timezone(settings.TIMEZONE)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否正确"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码hash值"""
    return pwd_context.hash(password)


def get_current_time() -> datetime:
    """获取当前时间"""
    return datetime.now(global_timezone)
