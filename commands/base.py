import argparse


class BaseCommand:
    """命令基类，所有命令都应继承此类"""

    help = "Base command"

    def add_arguments(self, parser: argparse.ArgumentParser):
        """可选，添加命令行参数"""
        pass

    def handle(self, *args, **options):
        """必须实现的命令逻辑"""
        raise NotImplementedError("handle() must be implemented.")
