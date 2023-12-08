from fastapi import FastAPI

from apps.account.apis import router as account_router
from apps.core.apis import router as core_router


def register_router(app: FastAPI) -> None:
    # 添加路由蓝图
    app.include_router(account_router)
    app.include_router(core_router)
