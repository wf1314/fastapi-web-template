from typing import Any

from tortoise import fields

from common.db import DBBaseModel
from common.utils import get_password_hash, verify_password


class User(DBBaseModel):
    """用户表"""

    id = fields.BigIntField(pk=True, description="主键id")
    name = fields.CharField(max_length=255, description="用户姓名", default="")
    username = fields.CharField(max_length=255, description="用户名")
    password = fields.CharField(max_length=255, description="密码hash值")
    phone = fields.CharField(max_length=255, description="手机号", default="")
    disabled = fields.BooleanField(description="是否禁用", default=False)

    class Meta:
        table = "user"
        table_description = "用户表"

    @classmethod
    async def create_user(
        cls: type["User"], username: str, password: str, **kwargs: Any
    ) -> "User":
        """存储hash密码"""
        hash_password = get_password_hash(password)
        user = await cls.create(username=username, password=hash_password, **kwargs)
        return user

    async def verify_password(self, password: str) -> bool:
        """验证密码是否正确"""
        return verify_password(password, self.password)

    async def change_password(self, password: str) -> None:
        """修改密码"""
        hash_password = get_password_hash(password)
        self.password = hash_password
        await self.save()
