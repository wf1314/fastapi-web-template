import asyncio
from typing import Annotated

import typer
from tortoise import Tortoise

from apps.account.models.db import User
from conf.settings import AERICH_TORTOISE_ORM_CONFIG

app = typer.Typer()


async def init_tortoise():
    await Tortoise.init(config=AERICH_TORTOISE_ORM_CONFIG)


async def _add_user(username: str, password: str) -> None:
    await init_tortoise()
    await User.create_user(username=username, password=password)
    typer.echo("User added!")


@app.command()
def add_user(
    username: Annotated[str, typer.Argument(help="用户名")],
    password: Annotated[
        str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)
    ],  # 隐藏式密码输入
) -> None:
    """创建新用户"""
    asyncio.run(_add_user(username, password))


if __name__ == "__main__":
    app()
