import logging
import os
import sys
import time

from loguru import logger

from core.utils.local import get_request_id
from settings import settings


def _ensure_request_id(record):
    # 如果 extra 里没有 request_id，就补一个
    record["extra"].setdefault("request_id", "NOT_CONTEXT")
    return True  # 继续让这条记录流向后续处理


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
        logger.bind(request_id=get_request_id()).opt(depth=6, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_logger():
    logger.remove()  # 移除默认的日志配置

    formatstr = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "request_id=<cyan>{extra[request_id]}</cyan> | "
        "{message}"
    )

    # 配置控制台输出
    logger.add(sys.stderr, level=settings.LOGGER_LEVEL, filter=_ensure_request_id, format=formatstr)

    # 配置文件输出：日志文件轮转、压缩、过期保留
    log_path_file = os.path.join(settings.LOG_FILE_PATH, f'{time.strftime(settings.LOGFILE_NAME + "_%Y_%m_%d")}.log')
    logger.add(
        log_path_file,
        level=settings.LOGGER_LEVEL,  # 控制输出的日志等级
        format=formatstr,
        filter=_ensure_request_id,
        rotation="10 MB",  # 每个日志文件的最大大小，超过时自动切割
        retention="30 days",  # 保留最近 30 天的日志
        compression="zip",  # 过期日志压缩为 zip 格式
        enqueue=True,  # 启用异步日志（适用于高并发环境）
        encoding="utf-8",  # 设置编码
    )

    # 用 InterceptHandler 劫持标准库 logging 模块日志
    root = logging.getLogger()
    root.handlers = [InterceptHandler()]
    root.setLevel(settings.LOGGER_LEVEL.upper())

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):  # logging.root.manager.loggerDict
        _logger = logging.getLogger(logger_name)
        _logger.handlers = [InterceptHandler()]
        _logger.setLevel(settings.LOGGER_LEVEL.upper())
        _logger.propagate = False  # 关闭向上冒泡，防止日志重复
