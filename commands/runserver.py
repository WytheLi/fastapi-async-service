import argparse

import uvicorn
from loguru import logger

from settings import settings
from .base import BaseCommand


class RunserverCommand(BaseCommand):
    """启动 FastAPI 服务器"""

    help = "启动 FastAPI 开发服务器"

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "--host", default=settings.HOST, help="服务器主机地址"
        )
        parser.add_argument(
            "--port", default=settings.PORT, type=int, help="服务器端口（默认：8000）"
        )

    def handle(self, *args, **options):
        """启动 FastAPI 服务器"""
        host = options.get("host")
        port = options.get("port")

        try:
            logger.info(
                """\n
     /$$$$$$$$                   /$$      /$$$$$$  /$$$$$$$  /$$$$$$
    | $$_____/                  | $$     /$$__  $$| $$__  $$|_  $$_/
    | $$    /$$$$$$   /$$$$$$$ /$$$$$$  | $$  | $$| $$  | $$  | $$
    | $$$$$|____  $$ /$$_____/|_  $$_/  | $$$$$$$$| $$$$$$$/  | $$
    | $$__/ /$$$$$$$|  $$$$$$   | $$    | $$__  $$| $$____/   | $$
    | $$   /$$__  $$ |____  $$  | $$ /$$| $$  | $$| $$        | $$
    | $$  |  $$$$$$$ /$$$$$$$/  |  $$$$/| $$  | $$| $$       /$$$$$$
    |__/   |_______/|_______/    |___/  |__/  |__/|__/      |______/

                """
            )
            uvicorn.run(
                'main:app',
                host=host,
                port=port,
                log_level=settings.LOG_LEVEL,
                reload=settings.RELOAD,
                reload_dirs=[settings.BASE_PATH],
                workers=settings.WORKERS
            )
        except Exception as e:
            logger.error(f'❌ FastAPI start filed: {e}')
