from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键id',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_removed` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0,
    `name` VARCHAR(255) NOT NULL  COMMENT '用户姓名' DEFAULT '',
    `username` VARCHAR(255) NOT NULL  COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL  COMMENT '密码hash值',
    `phone` VARCHAR(255) NOT NULL  COMMENT '手机号' DEFAULT '',
    `disabled` BOOL NOT NULL  COMMENT '是否禁用' DEFAULT 0
) CHARACTER SET utf8mb4 COMMENT='用户表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
