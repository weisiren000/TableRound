#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
增强的终端颜色系统
支持更多颜色、渐变、主题等
"""

import os
import sys
from typing import Dict, List, Any, Optional, Tuple
from ..utils.colors import Colors


class EnhancedColors(Colors):
    """增强的终端颜色类"""

    # 扩展前景色 (亮色)
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # 扩展背景色 (亮色)
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"
    
    # 256色支持
    @classmethod
    def color_256(cls, color_code: int) -> str:
        """256色前景色"""
        return f"\033[38;5;{color_code}m"
    
    @classmethod
    def bg_color_256(cls, color_code: int) -> str:
        """256色背景色"""
        return f"\033[48;5;{color_code}m"
    
    # RGB色彩支持
    @classmethod
    def rgb(cls, r: int, g: int, b: int) -> str:
        """RGB前景色"""
        return f"\033[38;2;{r};{g};{b}m"
    
    @classmethod
    def bg_rgb(cls, r: int, g: int, b: int) -> str:
        """RGB背景色"""
        return f"\033[48;2;{r};{g};{b}m"
    
    # 预定义的美观颜色
    ORANGE = "\033[38;5;208m"
    PINK = "\033[38;5;205m"
    PURPLE = "\033[38;5;135m"
    LIME = "\033[38;5;154m"
    GOLD = "\033[38;5;220m"
    SILVER = "\033[38;5;250m"
    
    # 渐变色效果
    @classmethod
    def gradient_text(cls, text: str, start_color: Tuple[int, int, int], end_color: Tuple[int, int, int]) -> str:
        """创建渐变色文本"""
        if not cls._enabled or len(text) == 0:
            return text
        
        result = ""
        text_len = len(text)
        
        for i, char in enumerate(text):
            # 计算当前位置的颜色
            ratio = i / max(text_len - 1, 1)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            result += cls.rgb(r, g, b) + char
        
        result += cls.RESET
        return result
    
    # 彩虹色效果
    @classmethod
    def rainbow_text(cls, text: str) -> str:
        """创建彩虹色文本"""
        if not cls._enabled:
            return text
        
        colors = [
            cls.RED, cls.BRIGHT_RED, cls.YELLOW, cls.BRIGHT_YELLOW,
            cls.GREEN, cls.BRIGHT_GREEN, cls.CYAN, cls.BRIGHT_CYAN,
            cls.BLUE, cls.BRIGHT_BLUE, cls.MAGENTA, cls.BRIGHT_MAGENTA
        ]
        
        result = ""
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            result += color + char
        
        result += cls.RESET
        return result
    
    # 便捷方法
    @classmethod
    def bright_green(cls, text: str) -> str:
        """亮绿色文本"""
        return cls.colorize(text, cls.BRIGHT_GREEN)
    
    @classmethod
    def bright_red(cls, text: str) -> str:
        """亮红色文本"""
        return cls.colorize(text, cls.BRIGHT_RED)
    
    @classmethod
    def bright_yellow(cls, text: str) -> str:
        """亮黄色文本"""
        return cls.colorize(text, cls.BRIGHT_YELLOW)
    
    @classmethod
    def bright_blue(cls, text: str) -> str:
        """亮蓝色文本"""
        return cls.colorize(text, cls.BRIGHT_BLUE)
    
    @classmethod
    def bright_magenta(cls, text: str) -> str:
        """亮洋红色文本"""
        return cls.colorize(text, cls.BRIGHT_MAGENTA)
    
    @classmethod
    def bright_cyan(cls, text: str) -> str:
        """亮青色文本"""
        return cls.colorize(text, cls.BRIGHT_CYAN)

    @classmethod
    def bright_white(cls, text: str) -> str:
        """亮白色文本"""
        return cls.colorize(text, cls.BRIGHT_WHITE)

    @classmethod
    def orange(cls, text: str) -> str:
        """橙色文本"""
        return cls.colorize(text, cls.ORANGE)
    
    @classmethod
    def pink(cls, text: str) -> str:
        """粉色文本"""
        return cls.colorize(text, cls.PINK)
    
    @classmethod
    def purple(cls, text: str) -> str:
        """紫色文本"""
        return cls.colorize(text, cls.PURPLE)
    
    @classmethod
    def lime(cls, text: str) -> str:
        """青柠色文本"""
        return cls.colorize(text, cls.LIME)
    
    @classmethod
    def gold(cls, text: str) -> str:
        """金色文本"""
        return cls.colorize(text, cls.GOLD)
    
    @classmethod
    def silver(cls, text: str) -> str:
        """银色文本"""
        return cls.colorize(text, cls.SILVER)


# 自动检测颜色支持
EnhancedColors.auto_detect()
