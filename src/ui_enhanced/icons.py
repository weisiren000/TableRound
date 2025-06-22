#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图标和符号库
提供各种Unicode图标和ASCII艺术
"""

from typing import Dict, List


class Icons:
    """图标类"""
    
    # 基础符号
    ARROW_RIGHT = "→"
    ARROW_LEFT = "←"
    ARROW_UP = "↑"
    ARROW_DOWN = "↓"
    ARROW_RIGHT_DOUBLE = "⇒"
    ARROW_LEFT_DOUBLE = "⇐"
    
    # 状态图标
    SUCCESS = "✓"
    ERROR = "✗"
    WARNING = "⚠"
    INFO = "ℹ"
    QUESTION = "?"
    LOADING = "⟳"
    STAR = "★"
    HEART = "♥"
    
    # 智能体角色图标
    CRAFTSMAN = "🔨"  # 手工艺人
    CONSUMER = "👤"   # 消费者
    MANUFACTURER = "🏭"  # 制造商
    DESIGNER = "🎨"   # 设计师
    GOD_VIEW = "👁"   # 上帝视角
    
    # 进度和状态
    PROGRESS_FULL = "█"
    PROGRESS_EMPTY = "░"
    PROGRESS_PARTIAL = "▓"
    
    # 装饰性符号
    DIAMOND = "◆"
    CIRCLE = "●"
    SQUARE = "■"
    TRIANGLE = "▲"
    
    # 边框符号
    BOX_HORIZONTAL = "─"
    BOX_VERTICAL = "│"
    BOX_TOP_LEFT = "┌"
    BOX_TOP_RIGHT = "┐"
    BOX_BOTTOM_LEFT = "└"
    BOX_BOTTOM_RIGHT = "┘"
    BOX_CROSS = "┼"
    BOX_T_DOWN = "┬"
    BOX_T_UP = "┴"
    BOX_T_RIGHT = "├"
    BOX_T_LEFT = "┤"
    
    # 双线边框
    DOUBLE_HORIZONTAL = "═"
    DOUBLE_VERTICAL = "║"
    DOUBLE_TOP_LEFT = "╔"
    DOUBLE_TOP_RIGHT = "╗"
    DOUBLE_BOTTOM_LEFT = "╚"
    DOUBLE_BOTTOM_RIGHT = "╝"
    
    # 圆角边框
    ROUND_TOP_LEFT = "╭"
    ROUND_TOP_RIGHT = "╮"
    ROUND_BOTTOM_LEFT = "╰"
    ROUND_BOTTOM_RIGHT = "╯"
    
    @classmethod
    def get_agent_icon(cls, agent_type: str) -> str:
        """获取智能体图标"""
        icons = {
            "craftsman": cls.CRAFTSMAN,
            "consumer": cls.CONSUMER,
            "manufacturer": cls.MANUFACTURER,
            "designer": cls.DESIGNER,
            "god_view": cls.GOD_VIEW
        }
        return icons.get(agent_type.lower(), "🤖")
    
    @classmethod
    def get_status_icon(cls, status: str) -> str:
        """获取状态图标"""
        icons = {
            "success": cls.SUCCESS,
            "error": cls.ERROR,
            "warning": cls.WARNING,
            "info": cls.INFO,
            "loading": cls.LOADING,
            "question": cls.QUESTION
        }
        return icons.get(status.lower(), cls.INFO)


class ASCIIArt:
    """ASCII艺术类"""
    
    # 项目Logo
    TABLEROUND_LOGO = """
        ╔══════════════════════════════════════════════════╗
        ║                                                  ║
        ║    ████████  █████  ██████  ██      ███████      ║
        ║       ██    ██   ██ ██   ██ ██      ██           ║
        ║       ██    ███████ ██████  ██      █████        ║
        ║       ██    ██   ██ ██   ██ ██      ██           ║
        ║       ██    ██   ██ ██████  ███████ ███████      ║
        ║                                                  ║
        ║    ██████   ██████  ██    ██ ███    ██ ██████    ║
        ║    ██   ██ ██    ██ ██    ██ ████   ██ ██   ██   ║
        ║    ██████  ██    ██ ██    ██ ██ ██  ██ ██   ██   ║
        ║    ██   ██ ██    ██ ██    ██ ██  ██ ██ ██   ██   ║
        ║    ██   ██  ██████   ██████  ██   ████ ██████    ║
        ║                                                  ║
        ║              圆桌会议智能体系统                    ║
        ╚══════════════════════════════════════════════════╝
"""
    
    # 简化版Logo
    SIMPLE_LOGO = """
    ╔═══════════════════════════╗
    ║     TableRound System     ║
    ║      圆桌会议系统          ║
    ╚═══════════════════════════╝
"""
    
    # 加载动画帧
    LOADING_FRAMES = [
        "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
    ]
    
    # 进度条样式
    PROGRESS_STYLES = {
        "classic": {
            "full": "█",
            "empty": "░",
            "partial": ["▏", "▎", "▍", "▌", "▋", "▊", "▉"]
        },
        "dots": {
            "full": "●",
            "empty": "○",
            "partial": ["◔", "◑", "◕"]
        },
        "blocks": {
            "full": "■",
            "empty": "□",
            "partial": ["▪", "▫"]
        }
    }
    
    @classmethod
    def get_loading_frame(cls, frame_index: int) -> str:
        """获取加载动画帧"""
        return cls.LOADING_FRAMES[frame_index % len(cls.LOADING_FRAMES)]
    
    @classmethod
    def create_progress_bar(cls, progress: float, width: int = 20, style: str = "classic") -> str:
        """创建进度条"""
        if style not in cls.PROGRESS_STYLES:
            style = "classic"
        
        style_config = cls.PROGRESS_STYLES[style]
        filled_width = int(progress * width)
        empty_width = width - filled_width
        
        # 处理部分填充
        partial_progress = (progress * width) - filled_width
        partial_char = ""
        if partial_progress > 0 and "partial" in style_config:
            partial_index = int(partial_progress * len(style_config["partial"]))
            if partial_index < len(style_config["partial"]):
                partial_char = style_config["partial"][partial_index]
                empty_width -= 1
        
        bar = (style_config["full"] * filled_width + 
               partial_char + 
               style_config["empty"] * empty_width)
        
        return bar


class Decorations:
    """装饰性元素类"""
    
    @classmethod
    def create_separator(cls, width: int = 50, char: str = "─") -> str:
        """创建分隔线"""
        return char * width
    
    @classmethod
    def create_title_box(cls, title: str, width: int = 50) -> str:
        """创建标题框"""
        title_len = len(title)
        padding = (width - title_len - 2) // 2

        top = Icons.BOX_TOP_LEFT + Icons.BOX_HORIZONTAL * (width - 2) + Icons.BOX_TOP_RIGHT
        middle = Icons.BOX_VERTICAL + " " * padding + title + " " * (width - title_len - padding - 2) + Icons.BOX_VERTICAL
        bottom = Icons.BOX_BOTTOM_LEFT + Icons.BOX_HORIZONTAL * (width - 2) + Icons.BOX_BOTTOM_RIGHT

        return f"{top}\n{middle}\n{bottom}"

    @classmethod
    def create_panel(cls, content: str, title: str = "", width: int = 50) -> str:
        """创建面板"""
        lines = content.split('\n')

        # 标题行
        if title:
            title_line = f"┤ {title} ├"
            title_padding = (width - len(title_line)) // 2
            top = Icons.BOX_TOP_LEFT + Icons.BOX_HORIZONTAL * title_padding + title_line + Icons.BOX_HORIZONTAL * (width - len(title_line) - title_padding - 2) + Icons.BOX_TOP_RIGHT
        else:
            top = Icons.BOX_TOP_LEFT + Icons.BOX_HORIZONTAL * (width - 2) + Icons.BOX_TOP_RIGHT

        # 内容行
        middle_lines = []
        for line in lines:
            line_len = len(line)
            padding = width - line_len - 2
            if padding > 0:
                middle_lines.append(Icons.BOX_VERTICAL + line + " " * padding + Icons.BOX_VERTICAL)
            else:
                # 截断过长的行
                middle_lines.append(Icons.BOX_VERTICAL + line[:width-2] + Icons.BOX_VERTICAL)

        # 底部
        bottom = Icons.BOX_BOTTOM_LEFT + Icons.BOX_HORIZONTAL * (width - 2) + Icons.BOX_BOTTOM_RIGHT

        return f"{top}\n" + "\n".join(middle_lines) + f"\n{bottom}"
