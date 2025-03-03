import code
import asyncio

from commands import load_models
from commands.base import BaseCommand

from db.async_engine import async_engine, create_async_session


class ShellCommand(BaseCommand):
    """实现 shell 命令"""

    help = "启动 FastAPI Shell"

    def handle(self, *args, **options):
        """启动 Python 交互式 shell"""
        banner = "FastAPI Shell - 可直接操作数据库\n"
        banner += "已导入: `session`, `engine`, 所有数据库模型\n"

        async_session = asyncio.run(create_async_session())  # 获取数据库会话

        model_context = load_models()

        local_context = {
            "engine": async_engine,
            "session": async_session,
            **model_context,  # 添加所有Model
        }

        try:
            import IPython
            IPython.start_ipython(argv=[], user_ns=local_context)
        except ImportError:
            code.interact(banner=banner, local=local_context)
