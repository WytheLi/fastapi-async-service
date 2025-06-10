import logging
import os
import sys
import time

from loguru import logger

from settings import settings


class InterceptHandler(logging.Handler):
    """
    劫持logging模块日志到loguru
    """
    def emit(self, record):
        # 把标准级别名转换成 Loguru 的级别，找不到就用 record.levelno
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        # depth=6 让 Loguru 能正确显示调用方代码位置
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


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

    # 用 InterceptHandler 劫持标准库 logging 模块日志
    root = logging.getLogger()
    root.handlers = [InterceptHandler()]
    root.setLevel(settings.LOGGER_LEVEL.upper())

    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
        _logger = logging.getLogger(logger_name)
        _logger.handlers = [InterceptHandler()]
        _logger.setLevel(settings.LOGGER_LEVEL.upper())
        _logger.propagate = False   # 关闭向上冒泡，防止日志重复