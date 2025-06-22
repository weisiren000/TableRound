#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主题管理系统
提供不同的UI主题配置
"""

from typing import Dict, Any
from .enhanced_colors import EnhancedColors


class Theme:
    """主题类"""
    
    def __init__(self, name: str, colors: Dict[str, str], styles: Dict[str, Any] = None):
        self.name = name
        self.colors = colors
        self.styles = styles or {}
    
    def get_color(self, element: str) -> str:
        """获取元素颜色"""
        return self.colors.get(element, EnhancedColors.BRIGHT_WHITE)
    
    def get_style(self, element: str) -> Any:
        """获取元素样式"""
        return self.styles.get(element, {})


class ThemeManager:
    """主题管理器"""
    
    def __init__(self):
        self.current_theme = None
        self.themes = {}
        self._init_default_themes()
    
    def _init_default_themes(self):
        """初始化默认主题"""
        
        # 默认主题
        default_theme = Theme(
            name="default",
            colors={
                "primary": EnhancedColors.BRIGHT_CYAN,
                "secondary": EnhancedColors.BRIGHT_BLUE,
                "success": EnhancedColors.BRIGHT_GREEN,
                "warning": EnhancedColors.BRIGHT_YELLOW,
                "error": EnhancedColors.BRIGHT_RED,
                "info": EnhancedColors.BRIGHT_BLUE,
                "text": EnhancedColors.BRIGHT_WHITE,
                "muted": EnhancedColors.SILVER,
                "accent": EnhancedColors.BRIGHT_MAGENTA,
                "background": "",
                "border": EnhancedColors.SILVER
            },
            styles={
                "panel_width": 60,
                "progress_width": 30,
                "menu_width": 50
            }
        )
        
        # 暗色主题
        dark_theme = Theme(
            name="dark",
            colors={
                "primary": EnhancedColors.CYAN,
                "secondary": EnhancedColors.BLUE,
                "success": EnhancedColors.GREEN,
                "warning": EnhancedColors.YELLOW,
                "error": EnhancedColors.RED,
                "info": EnhancedColors.BLUE,
                "text": EnhancedColors.WHITE,
                "muted": EnhancedColors.BRIGHT_BLACK,
                "accent": EnhancedColors.MAGENTA,
                "background": EnhancedColors.BG_BLACK,
                "border": EnhancedColors.BRIGHT_BLACK
            }
        )
        
        # 彩虹主题
        rainbow_theme = Theme(
            name="rainbow",
            colors={
                "primary": EnhancedColors.BRIGHT_MAGENTA,
                "secondary": EnhancedColors.BRIGHT_CYAN,
                "success": EnhancedColors.LIME,
                "warning": EnhancedColors.GOLD,
                "error": EnhancedColors.PINK,
                "info": EnhancedColors.PURPLE,
                "text": EnhancedColors.BRIGHT_WHITE,
                "muted": EnhancedColors.SILVER,
                "accent": EnhancedColors.ORANGE,
                "background": "",
                "border": EnhancedColors.BRIGHT_CYAN
            }
        )
        
        # 商务主题
        business_theme = Theme(
            name="business",
            colors={
                "primary": EnhancedColors.BLUE,
                "secondary": EnhancedColors.BRIGHT_BLUE,
                "success": EnhancedColors.GREEN,
                "warning": EnhancedColors.ORANGE,
                "error": EnhancedColors.RED,
                "info": EnhancedColors.CYAN,
                "text": EnhancedColors.WHITE,
                "muted": EnhancedColors.SILVER,
                "accent": EnhancedColors.GOLD,
                "background": "",
                "border": EnhancedColors.BLUE
            }
        )
        
        # 温暖主题
        warm_theme = Theme(
            name="warm",
            colors={
                "primary": EnhancedColors.ORANGE,
                "secondary": EnhancedColors.GOLD,
                "success": EnhancedColors.LIME,
                "warning": EnhancedColors.BRIGHT_YELLOW,
                "error": EnhancedColors.BRIGHT_RED,
                "info": EnhancedColors.BRIGHT_CYAN,
                "text": EnhancedColors.BRIGHT_WHITE,
                "muted": EnhancedColors.SILVER,
                "accent": EnhancedColors.PINK,
                "background": "",
                "border": EnhancedColors.ORANGE
            }
        )
        
        # 冷色主题
        cool_theme = Theme(
            name="cool",
            colors={
                "primary": EnhancedColors.BRIGHT_CYAN,
                "secondary": EnhancedColors.BRIGHT_BLUE,
                "success": EnhancedColors.BRIGHT_GREEN,
                "warning": EnhancedColors.BRIGHT_YELLOW,
                "error": EnhancedColors.BRIGHT_MAGENTA,
                "info": EnhancedColors.CYAN,
                "text": EnhancedColors.BRIGHT_WHITE,
                "muted": EnhancedColors.SILVER,
                "accent": EnhancedColors.PURPLE,
                "background": "",
                "border": EnhancedColors.BRIGHT_CYAN
            }
        )
        
        # 注册主题
        self.themes = {
            "default": default_theme,
            "dark": dark_theme,
            "rainbow": rainbow_theme,
            "business": business_theme,
            "warm": warm_theme,
            "cool": cool_theme
        }
        
        # 设置默认主题
        self.current_theme = default_theme
    
    def set_theme(self, theme_name: str) -> bool:
        """设置当前主题"""
        if theme_name in self.themes:
            self.current_theme = self.themes[theme_name]
            return True
        return False
    
    def get_current_theme(self) -> Theme:
        """获取当前主题"""
        return self.current_theme
    
    def list_themes(self) -> list:
        """列出所有主题"""
        return list(self.themes.keys())
    
    def add_theme(self, theme: Theme):
        """添加自定义主题"""
        self.themes[theme.name] = theme
    
    def get_color(self, element: str) -> str:
        """获取当前主题的颜色"""
        if self.current_theme:
            return self.current_theme.get_color(element)
        return EnhancedColors.BRIGHT_WHITE
    
    def get_style(self, element: str) -> Any:
        """获取当前主题的样式"""
        if self.current_theme:
            return self.current_theme.get_style(element)
        return {}
    
    def apply_color(self, text: str, element: str) -> str:
        """应用主题颜色到文本"""
        color = self.get_color(element)
        if color:
            return EnhancedColors.colorize(text, color)
        return text


# 全局主题管理器实例
theme_manager = ThemeManager()


# 便捷函数
def set_theme(theme_name: str) -> bool:
    """设置主题"""
    return theme_manager.set_theme(theme_name)


def get_theme_color(element: str) -> str:
    """获取主题颜色"""
    return theme_manager.get_color(element)


def apply_theme_color(text: str, element: str) -> str:
    """应用主题颜色"""
    return theme_manager.apply_color(text, element)


def list_available_themes() -> list:
    """列出可用主题"""
    return theme_manager.list_themes()


def get_current_theme_name() -> str:
    """获取当前主题名称"""
    return theme_manager.current_theme.name if theme_manager.current_theme else "none"


# 主题颜色便捷函数
def primary(text: str) -> str:
    """主色"""
    return apply_theme_color(text, "primary")


def secondary(text: str) -> str:
    """次色"""
    return apply_theme_color(text, "secondary")


def success(text: str) -> str:
    """成功色"""
    return apply_theme_color(text, "success")


def warning(text: str) -> str:
    """警告色"""
    return apply_theme_color(text, "warning")


def error(text: str) -> str:
    """错误色"""
    return apply_theme_color(text, "error")


def info(text: str) -> str:
    """信息色"""
    return apply_theme_color(text, "info")


def text(text: str) -> str:
    """文本色"""
    return apply_theme_color(text, "text")


def muted(text: str) -> str:
    """静音色"""
    return apply_theme_color(text, "muted")


def accent(text: str) -> str:
    """强调色"""
    return apply_theme_color(text, "accent")
