#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uvicorn
from loguru import logger

from core import create_app
from settings import settings


app = create_app()


if __name__ == '__main__':
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
            host=settings.HOST,
            port=settings.PORT,
            log_level=settings.LOG_LEVEL,
            reload=settings.RELOAD,
            reload_dirs=[settings.BASE_PATH],
            workers=settings.WORKERS
        )
    except Exception as e:
        logger.error(f'❌ FastAPI start filed: {e}')
