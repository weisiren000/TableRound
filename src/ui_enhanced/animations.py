#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
动画效果库
提供各种终端动画效果
"""

import time
import sys
import threading
from typing import List, Callable, Optional
from .enhanced_colors import EnhancedColors
from .icons import ASCIIArt


class Animations:
    """动画效果类"""
    
    @staticmethod
    def typewriter_effect(text: str, delay: float = 0.05, color: str = ""):
        """打字机效果"""
        if color:
            text = EnhancedColors.colorize(text, color)
        
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()  # 换行
    
    @staticmethod
    def fade_in_text(text: str, steps: int = 10, delay: float = 0.1):
        """文字淡入效果"""
        for i in range(steps + 1):
            # 清除当前行
            sys.stdout.write('\r' + ' ' * len(text) + '\r')
            
            # 计算透明度
            alpha = i / steps
            if alpha < 0.3:
                colored_text = EnhancedColors.colorize(text, EnhancedColors.BRIGHT_BLACK)
            elif alpha < 0.6:
                colored_text = EnhancedColors.colorize(text, EnhancedColors.SILVER)
            else:
                colored_text = EnhancedColors.colorize(text, EnhancedColors.BRIGHT_WHITE)
            
            sys.stdout.write(colored_text)
            sys.stdout.flush()
            time.sleep(delay)
        
        print()  # 换行
    
    @staticmethod
    def loading_spinner(duration: float = 3.0, message: str = "加载中"):
        """加载旋转动画"""
        frames = ASCIIArt.LOADING_FRAMES
        start_time = time.time()
        frame_index = 0
        
        while time.time() - start_time < duration:
            frame = frames[frame_index % len(frames)]
            colored_frame = EnhancedColors.bright_cyan(frame)
            text = f"\r{colored_frame} {message}..."
            
            sys.stdout.write(text)
            sys.stdout.flush()
            
            time.sleep(0.1)
            frame_index += 1
        
        # 清除加载动画
        sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')
        sys.stdout.flush()
    
    @staticmethod
    def progress_animation(total_steps: int, step_duration: float = 0.1, message: str = "处理中"):
        """进度条动画"""
        from .ui_components import ProgressBar
        
        progress_bar = ProgressBar(total_steps, width=30)
        
        for i in range(total_steps + 1):
            progress_bar.update(i)
            bar_text = progress_bar.render()
            
            sys.stdout.write(f'\r{message}: {bar_text}')
            sys.stdout.flush()
            
            time.sleep(step_duration)
        
        print()  # 换行
    
    @staticmethod
    def wave_text(text: str, waves: int = 3, delay: float = 0.1):
        """波浪文字效果"""
        colors = [
            EnhancedColors.BRIGHT_RED,
            EnhancedColors.BRIGHT_YELLOW,
            EnhancedColors.BRIGHT_GREEN,
            EnhancedColors.BRIGHT_CYAN,
            EnhancedColors.BRIGHT_BLUE,
            EnhancedColors.BRIGHT_MAGENTA
        ]
        
        for wave in range(waves):
            for offset in range(len(colors)):
                colored_text = ""
                for i, char in enumerate(text):
                    color_index = (i + offset) % len(colors)
                    colored_char = EnhancedColors.colorize(char, colors[color_index])
                    colored_text += colored_char
                
                sys.stdout.write('\r' + colored_text)
                sys.stdout.flush()
                time.sleep(delay)
        
        print()  # 换行
    
    @staticmethod
    def bounce_text(text: str, bounces: int = 3, delay: float = 0.2):
        """弹跳文字效果"""
        for bounce in range(bounces):
            # 上升
            for i in range(3):
                sys.stdout.write('\r' + ' ' * i + text)
                sys.stdout.flush()
                time.sleep(delay / 3)
            
            # 下降
            for i in range(2, -1, -1):
                sys.stdout.write('\r' + ' ' * i + text)
                sys.stdout.flush()
                time.sleep(delay / 3)
        
        sys.stdout.write('\r' + text)
        print()  # 换行


class LoadingSpinner:
    """加载动画类（可控制的）"""
    
    def __init__(self, message: str = "加载中", style: str = "spinner"):
        self.message = message
        self.style = style
        self.running = False
        self.thread = None
        
        self.styles = {
            "spinner": ASCIIArt.LOADING_FRAMES,
            "dots": [".", "..", "...", ""],
            "bars": ["|", "/", "-", "\\"],
            "blocks": ["▁", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃"]
        }
    
    def start(self):
        """开始动画"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """停止动画"""
        self.running = False
        if self.thread:
            self.thread.join()
        
        # 清除动画
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()
    
    def _animate(self):
        """动画循环"""
        frames = self.styles.get(self.style, self.styles["spinner"])
        frame_index = 0
        
        while self.running:
            frame = frames[frame_index % len(frames)]
            colored_frame = EnhancedColors.bright_cyan(frame)
            text = f"\r{colored_frame} {self.message}..."
            
            sys.stdout.write(text)
            sys.stdout.flush()
            
            time.sleep(0.1)
            frame_index += 1


class ProgressTracker:
    """进度跟踪器（可控制的）"""
    
    def __init__(self, total: int, message: str = "处理中", width: int = 30):
        self.total = total
        self.current = 0
        self.message = message
        self.width = width
        self.start_time = time.time()
    
    def update(self, current: int, message: str = None):
        """更新进度"""
        self.current = min(current, self.total)
        if message:
            self.message = message
        
        self._render()
    
    def increment(self, message: str = None):
        """增加进度"""
        self.current = min(self.current + 1, self.total)
        if message:
            self.message = message
        
        self._render()
    
    def finish(self, message: str = "完成"):
        """完成进度"""
        self.current = self.total
        self.message = message
        self._render()
        print()  # 换行
    
    def _render(self):
        """渲染进度条"""
        from .ui_components import ProgressBar
        
        progress_bar = ProgressBar(self.total, self.width)
        progress_bar.current = self.current
        progress_bar.start_time = self.start_time
        
        bar_text = progress_bar.render()
        
        sys.stdout.write(f'\r{self.message}: {bar_text}')
        sys.stdout.flush()


# 便捷函数
def show_loading(duration: float = 2.0, message: str = "加载中"):
    """显示加载动画"""
    Animations.loading_spinner(duration, message)


def show_progress(steps: List[str], step_duration: float = 1.0):
    """显示步骤进度"""
    tracker = ProgressTracker(len(steps), "初始化")
    
    for i, step in enumerate(steps):
        tracker.update(i, step)
        time.sleep(step_duration)
    
    tracker.finish("完成")


def typewriter(text: str, delay: float = 0.05, color: str = ""):
    """打字机效果便捷函数"""
    Animations.typewriter_effect(text, delay, color)
