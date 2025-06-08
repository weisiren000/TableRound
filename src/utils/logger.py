#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志工具模块
"""

import os
import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_to_console: bool = True,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    设置日志记录器

    Args:
        level: 日志级别
        log_file: 日志文件路径
        log_to_console: 是否输出到控制台
        log_format: 日志格式

    Returns:
        日志记录器
    """
    # 创建根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # 清除现有处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 设置日志格式
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # 添加控制台处理器
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # 添加文件处理器
    if log_file:
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # 创建文件处理器
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return root_logger


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    获取日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别

    Returns:
        日志记录器
    """
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    return logger
