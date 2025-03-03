import argparse
import importlib
import inspect
import os
import pkgutil
import sys

import models
from db import Base
from .base import BaseCommand


def load_commands():
    """自动加载 `commands/` 目录下的所有命令"""
    command_classes = {}

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"commands.{module_name}")
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, BaseCommand) and obj is not BaseCommand:
                command_classes[module_name] = obj  # key: `shell`, `runserver`, etc.
    return command_classes


def load_models():
    """自动导入 `models/` 目录下的所有模型"""
    model_classes = {}
    for _, module_name, _ in pkgutil.iter_modules(models.__path__):
        module = importlib.import_module(f"models.{module_name}")
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Base) and obj is not Base:
                model_classes[name] = obj
    return model_classes


class ManagementUtility:
    """命令行管理工具，负责解析和分发命令"""

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])

        self.commands = load_commands()  # 动态加载命令
        self.parser = argparse.ArgumentParser(description="FastAPI 管理工具")
        self.subparsers = self.parser.add_subparsers(dest="command", help="可用命令")

        self.register_commands()

    def register_commands(self):
        """注册所有可用命令"""
        for command_name, command_class in self.commands.items():
            command_parser = self.subparsers.add_parser(command_name, help=command_class.help)
            command_instance = command_class()
            command_instance.add_arguments(command_parser)

    def execute(self):
        """解析命令并执行"""
        args = self.parser.parse_args(self.argv[1:])
        if args.command in self.commands:
            command_instance = self.commands[args.command]()
            command_options = vars(args)  # 转换为字典
            del command_options["command"]  # 删除 `command` 这个 key
            command_instance.handle(**command_options)
        else:
            self.parser.print_help()


def execute_from_command_line(argv=None):
    utility = ManagementUtility(argv)
    utility.execute()
