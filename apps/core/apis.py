from fastapi import APIRouter, Depends

from apps.account.models.db import User
from common.authentication import need_access_token, selectable_access_token
from common.exceptions import ExampleError

router = APIRouter(
    prefix="/core",
    tags=["业务核心"],
    responses={404: {"description": "Not found"}},
)


@router.get("/index", summary="index")
async def index():
    """index"""
    return "hello world"


@router.get("/auth-index", summary="需要认证访问")
async def auth_index(user: User = Depends(need_access_token)):
    """需要携带Authorization头"""
    return "authed"


@router.get("/selectable-auth-index", summary="认证与不认证都可访问访问")
async def selectable_auth_index(user: User | None = Depends(selectable_access_token)):
    """认证与不认证都可获得相应"""
    if user:
        return "authed"
    return "no auth"


@router.get("/error-example", summary="报错示例")
async def error_example():
    """返回状态码400"""
    raise ExampleError.OnPurposeError
