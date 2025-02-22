import os
import sys
import time

from loguru import logger

from settings import settings


def configure_logger():
    logger.remove()  # 移除默认的日志配置

    # 配置控制台输出
    logger.add(sys.stderr, level=settings.LOGGER_LEVEL, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

    # 配置文件输出：日志文件轮转、压缩、过期保留
    log_path_file = os.path.join(settings.LOG_FILE_PATH, f'{time.strftime(settings.LOGFILE_NAME + "_%Y_%m_%d")}.log')
    logger.add(
        log_path_file,
        level=settings.LOGGER_LEVEL,  # 控制输出的日志等级
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        rotation="10 MB",  # 每个日志文件的最大大小，超过时自动切割
        retention="30 days",  # 保留最近 30 天的日志
        compression="zip",  # 过期日志压缩为 zip 格式
        enqueue=True,  # 启用异步日志（适用于高并发环境）
        encoding="utf-8"  # 设置编码
    )

    # 配置其他日志（例如错误日志单独存放）
    # logger.add(
    #     os.path.join(LOG_DIR, "errors.log"),
    #     level="ERROR",
    #     format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    #     rotation="1 week",  # 每周切割
    #     retention="30 days",
    #     compression="zip",
    #     enqueue=True
    # )
