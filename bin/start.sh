#!/bin/bash

# 获取当前脚本所在目录
SCRIPT_DIR=$(dirname $(realpath $0))

# 设置 PYTHONPATH
export PYTHONPATH=$(dirname "$SCRIPT_DIR")

# 打印 PYTHONPATH 以进行调试
echo "PYTHONPATH is set to: $PYTHONPATH"

# 检测操作系统并获取 CPU 核心数量
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    WORKERS=${WEB_CONCURRENCY:-$(nproc)}
elif [[ "$OSTYPE" == "darwin"* ]]; then
    WORKERS=${WEB_CONCURRENCY:-$(sysctl -n hw.ncpu)}
else
    echo "Unsupported OS type: $OSTYPE. Defaulting to 1 CPU."
    WORKERS=1
fi

# 获取环境变量配置
HOST=${HOST:-$HOST}
PORT=${PORT:-$PORT}
RELOAD=${RELOAD:-$RELOAD}
LOG_LEVEL=${LOG_LEVEL:-$LOG_LEVEL}

# 确保 RELOAD 变量已设置
RELOAD=${RELOAD:-false}

# 打印所有重要环境变量以进行调试
echo "HOST: $HOST"
echo "PORT: $PORT"
echo "RELOAD: $RELOAD"
echo "LOG_LEVEL: $LOG_LEVEL"
echo "WORKERS: $WORKERS"

# 运行 Alembic 迁移
echo "Running Alembic migrations"
alembic upgrade head

# 运行msgfmt生成.mo编译消息文件
echo "Running msgfmt output messages.mo"
msgfmt app/locales/en/LC_MESSAGES/messages.po -o app/locales/en/LC_MESSAGES/messages.mo
msgfmt app/locales/zh/LC_MESSAGES/messages.po -o app/locales/zh/LC_MESSAGES/messages.mo
msgfmt app/locales/fil_ph/LC_MESSAGES/messages.po -o app/locales/fil_ph/LC_MESSAGES/messages.mo
msgfmt app/locales/id/LC_MESSAGES/messages.po -o app/locales/id/LC_MESSAGES/messages.mo

# 启动 Uvicorn 服务器，动态配置多进程和多线程
uvicorn app.main:app \
    --host $HOST \
    --port $PORT \
    --workers $WORKERS \
    --loop uvloop \
    --http h11 \
    --log-level $LOG_LEVEL \
    $( [ "$RELOAD" = true ] && echo --reload )
