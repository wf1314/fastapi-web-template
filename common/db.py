"""
DB 基类
"""
from tortoise import fields
from tortoise.models import Model


class DBBaseModel(Model):

    id = fields.BigIntField(pk=True, description="主键id")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_removed = fields.BooleanField(description="是否删除", default=False)

    class Meta:
        abstract = True
