#!/bin/env python3
# -*- encoding: utf-8 -*-
import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List


class Settings(BaseSettings):
    """
    Pydantic读取系统环境变量或.env文件中的配置项
    https://docs.pydantic.dev/latest/concepts/pydantic_settings/
    优先级：.env > system environment variable > define default value
    """
    # pydantic 配置
    # # env_file加载.env文件
    # # case_sensitive环境变量名是/否区分大小写
    # # env_prefix='my_prefix_'用于更改所有环境变量名的前缀
    model_config = SettingsConfigDict(env_file=('.env', 'local.env'), case_sensitive=False)

    BASE_PATH: str = os.path.dirname(os.path.abspath(__file__))

    # server 配置
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    RELOAD: bool = True
    DEBUG: bool = True
    LOG_LEVEL: str = "info"  # 按等级过滤url请求日志，只做debug输出
    API_PREFIX: str = "/api/v1"
    WORKERS: int = 1

    # swagger 配置
    TITLE: str = "FastAPI"
    DESCRIPTION: str = "FastApi Api Service"
    VERSION: str = "1.0.0"
    # OPENAPI_URL: Optional[str] = "/openapi.json"
    # OPENAPI_TAGS: Optional[List[Dict[str, Any]]] = None
    DOCS_URL: Optional[str] = None  # 默认关闭"/docs"路径的Swagger接口文档
    REDOC_URL: Optional[str] = None  # 默认关闭"/redoc"路径的Redocly接口文档
    # SWAGGER_UI_OAUTH2_REDIRECT_URL: Optional[str] = "/docs/oauth2-redirect"  # 默认swagger认证后回调地址
    # SWAGGER_UI_INIT_OAUTH: Optional[dict] = None  # 默认swagger开启认证
    SWAGGER_PASSWORD: str = "demo"

    # logger 配置
    LOGFILE_OUTPUT: bool = False
    LOGFILE_NAME: str = "FastAPI"
    LOG_FILE_PATH: str = os.path.join(BASE_PATH, 'logs')
    LOGGER_LEVEL: str = 'INFO'

    # Cors 配置
    ALLOWED_HOSTS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]

    # JWT配置
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_TOKEN_PREFIX: str = "Bearer"  # noqa: S105
    TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 8天
    SECRET_KEY_API: str = ""

    # database 配置
    PGSQL_URL: str = "postgresql://<username>:<password>@<host:port>/<dbname>"
    DB_ECHO: bool = False

    # redis 配置
    REDIS_URL: str = "redis://:<password>@<host:port>/<db-number>"

    # sns auth 配置
    SNS_PROVIDER: list = ["google"]
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_OAUTH_INFO: dict = {
        'auth_uri': "https://accounts.google.com/o/oauth2/auth",
        'token_uri': "https://oauth2.googleapis.com/token",
        'userinfo_uri': "https://www.googleapis.com/oauth2/v1/userinfo",
        'scope': "openid email profile"
    }

    # 本地化配置
    USE_TZ: bool = True  # 启用时区支持
    TIME_ZONE: str = "Asia/Shanghai"  # 默认时区
    LANGUAGE_CODE: str = "en"     # 默认语言


settings = Settings()
