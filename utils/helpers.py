"""
工具函数

作者：kinbos 严富坤
邮箱：fookinbos@gmail.com
个人网站：htttps://www.yanfukun.com
"""

import importlib
import os
import sys
from pathlib import Path


def ensure_directory(path):
    """
    确保目录存在，如果不存在则创建

    Args:
        path: 目录路径

    Returns:
        Path: 目录路径对象
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def import_module_from_path(module_name, module_path):
    """
    从路径导入模块

    Args:
        module_name: 模块名称
        module_path: 模块路径

    Returns:
        module: 导入的模块
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        return None

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def format_error(e):
    """
    格式化异常信息

    Args:
        e: 异常对象

    Returns:
        str: 格式化后的异常信息
    """
    return f"{type(e).__name__}: {str(e)}"