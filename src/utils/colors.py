#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
终端颜色支持模块
"""

import os
import sys
from typing import Dict, List, Any, Optional


class Colors:
    """终端颜色类"""

    # 前景色
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # 背景色
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # 样式
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ITALIC = "\033[3m"
    
    # 重置
    RESET = "\033[0m"
    
    # 是否启用颜色
    _enabled = True
    
    @classmethod
    def disable(cls) -> None:
        """禁用颜色"""
        cls._enabled = False
    
    @classmethod
    def enable(cls) -> None:
        """启用颜色"""
        cls._enabled = True
    
    @classmethod
    def is_enabled(cls) -> bool:
        """是否启用颜色"""
        return cls._enabled
    
    @classmethod
    def auto_detect(cls) -> None:
        """自动检测是否支持颜色"""
        # Windows 10 以上版本支持 ANSI 颜色
        if sys.platform == "win32":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # 获取控制台模式
            mode = ctypes.c_int()
            if kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(mode)):
                # 启用 ANSI 颜色
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), mode.value | 0x0004)
                cls._enabled = True
            else:
                cls._enabled = False
        else:
            # 检查是否是终端
            cls._enabled = sys.stdout.isatty()
            
            # 检查环境变量
            if "NO_COLOR" in os.environ:
                cls._enabled = False
            elif "FORCE_COLOR" in os.environ:
                cls._enabled = True
    
    @classmethod
    def colorize(cls, text: str, color: str, bg_color: Optional[str] = None, bold: bool = False, underline: bool = False, italic: bool = False) -> str:
        """
        为文本添加颜色

        Args:
            text: 文本
            color: 颜色
            bg_color: 背景色
            bold: 是否加粗
            underline: 是否下划线
            italic: 是否斜体

        Returns:
            带颜色的文本
        """
        if not cls._enabled:
            return text
        
        result = ""
        if color:
            result += color
        if bg_color:
            result += bg_color
        if bold:
            result += cls.BOLD
        if underline:
            result += cls.UNDERLINE
        if italic:
            result += cls.ITALIC
        
        result += text + cls.RESET
        return result
    
    @classmethod
    def green(cls, text: str) -> str:
        """绿色文本"""
        return cls.colorize(text, cls.GREEN)
    
    @classmethod
    def red(cls, text: str) -> str:
        """红色文本"""
        return cls.colorize(text, cls.RED)
    
    @classmethod
    def yellow(cls, text: str) -> str:
        """黄色文本"""
        return cls.colorize(text, cls.YELLOW)
    
    @classmethod
    def blue(cls, text: str) -> str:
        """蓝色文本"""
        return cls.colorize(text, cls.BLUE)
    
    @classmethod
    def magenta(cls, text: str) -> str:
        """洋红色文本"""
        return cls.colorize(text, cls.MAGENTA)
    
    @classmethod
    def cyan(cls, text: str) -> str:
        """青色文本"""
        return cls.colorize(text, cls.CYAN)
    
    @classmethod
    def bold(cls, text: str) -> str:
        """加粗文本"""
        return cls.colorize(text, "", bold=True)


# 自动检测是否支持颜色
Colors.auto_detect()
