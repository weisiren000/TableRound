#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI组件库
提供各种终端UI组件
"""

import time
from typing import List, Optional, Dict, Any
from .enhanced_colors import EnhancedColors
from .icons import Icons, ASCIIArt, Decorations


class Panel:
    """面板组件"""
    
    def __init__(self, title: str = "", width: int = 60, border_style: str = "single"):
        self.title = title
        self.width = width
        self.border_style = border_style
        self.content_lines = []
    
    def add_line(self, text: str, color: str = ""):
        """添加一行内容"""
        if color:
            text = EnhancedColors.colorize(text, color)
        self.content_lines.append(text)
    
    def add_separator(self):
        """添加分隔线"""
        self.content_lines.append(Icons.BOX_HORIZONTAL * (self.width - 4))
    
    def render(self) -> str:
        """渲染面板"""
        lines = []
        
        # 顶部边框
        if self.title:
            title_text = f"┤ {self.title} ├"
            title_padding = (self.width - len(title_text)) // 2
            remaining = self.width - len(title_text) - title_padding - 2
            top = Icons.BOX_TOP_LEFT + Icons.BOX_HORIZONTAL * title_padding + title_text + Icons.BOX_HORIZONTAL * remaining + Icons.BOX_TOP_RIGHT
        else:
            top = Icons.BOX_TOP_LEFT + Icons.BOX_HORIZONTAL * (self.width - 2) + Icons.BOX_TOP_RIGHT
        lines.append(top)
        
        # 内容行
        for line in self.content_lines:
            # 移除ANSI颜色代码来计算实际长度
            import re
            clean_line = re.sub(r'\033\[[0-9;]*m', '', line)
            line_len = len(clean_line)
            
            if line_len <= self.width - 4:
                padding = self.width - line_len - 4
                content_line = Icons.BOX_VERTICAL + " " + line + " " * padding + " " + Icons.BOX_VERTICAL
            else:
                # 截断过长的行
                truncated = line[:self.width-6] + "..."
                content_line = Icons.BOX_VERTICAL + " " + truncated + " " + Icons.BOX_VERTICAL
            
            lines.append(content_line)
        
        # 底部边框
        bottom = Icons.BOX_BOTTOM_LEFT + Icons.BOX_HORIZONTAL * (self.width - 2) + Icons.BOX_BOTTOM_RIGHT
        lines.append(bottom)
        
        return "\n".join(lines)


class ProgressBar:
    """进度条组件"""
    
    def __init__(self, total: int, width: int = 40, style: str = "classic"):
        self.total = total
        self.current = 0
        self.width = width
        self.style = style
        self.start_time = time.time()
    
    def update(self, current: int):
        """更新进度"""
        self.current = min(current, self.total)
    
    def increment(self):
        """增加进度"""
        self.current = min(self.current + 1, self.total)
    
    def render(self, show_percentage: bool = True, show_eta: bool = True) -> str:
        """渲染进度条"""
        progress = self.current / self.total if self.total > 0 else 0
        
        # 创建进度条
        bar = ASCIIArt.create_progress_bar(progress, self.width, self.style)
        
        # 添加颜色
        if progress < 0.3:
            bar = EnhancedColors.red(bar)
        elif progress < 0.7:
            bar = EnhancedColors.yellow(bar)
        else:
            bar = EnhancedColors.green(bar)
        
        result = f"[{bar}]"
        
        # 添加百分比
        if show_percentage:
            percentage = f" {progress*100:.1f}%"
            result += percentage
        
        # 添加计数
        result += f" ({self.current}/{self.total})"
        
        # 添加ETA
        if show_eta and self.current > 0:
            elapsed = time.time() - self.start_time
            if self.current < self.total:
                eta = elapsed * (self.total - self.current) / self.current
                eta_str = f" ETA: {eta:.1f}s"
                result += eta_str
        
        return result


class Menu:
    """菜单组件"""
    
    def __init__(self, title: str = "", width: int = 50):
        self.title = title
        self.width = width
        self.options = []
    
    def add_option(self, key: str, text: str, description: str = "", icon: str = ""):
        """添加菜单选项"""
        self.options.append({
            "key": key,
            "text": text,
            "description": description,
            "icon": icon
        })
    
    def render(self) -> str:
        """渲染菜单"""
        lines = []
        
        # 标题
        if self.title:
            title_panel = Panel(self.title, self.width)
            lines.append(title_panel.render())
            lines.append("")
        
        # 选项
        for option in self.options:
            icon = option["icon"] + " " if option["icon"] else ""
            key_text = EnhancedColors.bright_cyan(f"[{option['key']}]")
            option_text = EnhancedColors.bright_white(option["text"])
            
            line = f"  {icon}{key_text} {option_text}"
            
            if option["description"]:
                desc_text = EnhancedColors.silver(f" - {option['description']}")
                line += desc_text
            
            lines.append(line)
        
        return "\n".join(lines)


class StatusIndicator:
    """状态指示器"""
    
    @staticmethod
    def success(message: str) -> str:
        """成功状态"""
        icon = EnhancedColors.bright_green(Icons.SUCCESS)
        text = EnhancedColors.bright_white(message)
        return f"{icon} {text}"
    
    @staticmethod
    def error(message: str) -> str:
        """错误状态"""
        icon = EnhancedColors.bright_red(Icons.ERROR)
        text = EnhancedColors.bright_white(message)
        return f"{icon} {text}"
    
    @staticmethod
    def warning(message: str) -> str:
        """警告状态"""
        icon = EnhancedColors.bright_yellow(Icons.WARNING)
        text = EnhancedColors.bright_white(message)
        return f"{icon} {text}"
    
    @staticmethod
    def info(message: str) -> str:
        """信息状态"""
        icon = EnhancedColors.bright_blue(Icons.INFO)
        text = EnhancedColors.bright_white(message)
        return f"{icon} {text}"
    
    @staticmethod
    def loading(message: str, frame: int = 0) -> str:
        """加载状态"""
        icon = EnhancedColors.bright_cyan(ASCIIArt.get_loading_frame(frame))
        text = EnhancedColors.bright_white(message)
        return f"{icon} {text}"


class AgentCard:
    """智能体卡片"""
    
    def __init__(self, agent_name: str, agent_type: str, status: str = "idle"):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.status = status
    
    def render(self, width: int = 30) -> str:
        """渲染智能体卡片"""
        icon = Icons.get_agent_icon(self.agent_type)
        
        # 状态颜色
        status_colors = {
            "idle": EnhancedColors.silver,
            "thinking": EnhancedColors.bright_yellow,
            "speaking": EnhancedColors.bright_green,
            "listening": EnhancedColors.bright_blue,
            "error": EnhancedColors.bright_red
        }
        
        color_func = status_colors.get(self.status, EnhancedColors.bright_white)
        
        panel = Panel(f"{icon} {self.agent_name}", width)
        panel.add_line(f"类型: {self.agent_type}")
        panel.add_line(f"状态: {color_func(self.status)}")
        
        return panel.render()


class UIComponents:
    """UI组件工具类"""
    
    @staticmethod
    def clear_screen():
        """清屏"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title: str, subtitle: str = ""):
        """打印页面头部"""
        UIComponents.clear_screen()
        
        # Logo
        logo = EnhancedColors.gradient_text(
            ASCIIArt.SIMPLE_LOGO, 
            (0, 150, 255), 
            (255, 0, 150)
        )
        print(logo)
        print()
        
        # 标题
        if title:
            title_text = EnhancedColors.bright_cyan(title)
            print(f"  {title_text}")
            
        if subtitle:
            subtitle_text = EnhancedColors.silver(subtitle)
            print(f"  {subtitle_text}")
            
        print()
    
    @staticmethod
    def print_separator(width: int = 60):
        """打印分隔线"""
        separator = EnhancedColors.silver(Decorations.create_separator(width))
        print(separator)
    
    @staticmethod
    def wait_for_input(prompt: str = "按回车键继续...") -> str:
        """等待用户输入"""
        prompt_text = EnhancedColors.bright_yellow(prompt)
        return input(f"\n{prompt_text}")
