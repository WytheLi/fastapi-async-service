#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from commands import execute_from_command_line
from core import create_app

app = create_app()


def main():
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
