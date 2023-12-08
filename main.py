from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger
from tortoise import Tortoise, connections

from common.exceptions.handler import register_custom_exception
from common.logger import init_logging
from common.middleware import register_middleware
from common.response import CustomJSONResponse
from conf.routers import register_router
from conf.settings import AERICH_TORTOISE_ORM_CONFIG, settings


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        """
        新版本fastapi使用该方式替代startup 和shutdown 事件
        https://fastapi.tiangolo.com/advanced/events/
        如果需要初始化模型等操作应该在此方法的yield前进行并在yield后释放
        """
        # startup
        init_logging()
        logger.info("项启动信号接收成功!")
        if settings.DB_URL:
            # 初始化tortoise-orm
            await Tortoise.init(config=AERICH_TORTOISE_ORM_CONFIG)
        yield
        # shutdown
        logger.info("项目终止信号接收成功!")
        if settings.DB_URL:
            # 关闭所有tortoise-orm连接
            await connections.close_all()

    _app = FastAPI(
        default_response_class=CustomJSONResponse,  # 修改默认响应类, 响应中增加code, msg
        lifespan=lifespan,
    )
    # 注册中间件
    register_middleware(_app)
    # 注册路由
    register_router(_app)
    # 注册自定义异常处理
    register_custom_exception(_app)
    # https://github.com/uriyyo/fastapi-pagination 分页器用法
    # 开启静态目录
    if settings.STATIC_FILE:
        from fastapi.staticfiles import StaticFiles

        _app.mount(
            settings.STATIC_PATH,
            StaticFiles(directory=settings.STATIC_DIR),
            name="static",
        )
    return _app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
