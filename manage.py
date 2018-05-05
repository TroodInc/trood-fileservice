#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "file_service.settings")


def rel(*x):
    # get absolute path from relative to bin
    base = os.path.abspath(os.path.dirname(__file__))
    return os.path.normpath(os.path.join(base, *x))


if __name__ == '__main__':

    source_root_path = rel('.')
    if os.path.isdir(source_root_path):
        sys.path.insert(0, source_root_path)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)