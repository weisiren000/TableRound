#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
流式输出处理模块 - 增强版
"""

import sys
import time
import asyncio
from typing import Callable, Optional

# 导入UI美化组件
try:
    from ..ui_enhanced import (
        EnhancedColors, Icons, ASCIIArt, Decorations,
        StatusIndicator, Animations
    )
    UI_ENHANCED_AVAILABLE = True
except ImportError:
    UI_ENHANCED_AVAILABLE = False


class StreamHandler:
    """增强版流式输出处理类"""

    def __init__(self, output_func: Optional[Callable[[str], None]] = None, enable_ui_enhancement: bool = True):
        """
        初始化流式输出处理器

        Args:
            output_func: 输出函数，默认为 print
            enable_ui_enhancement: 是否启用UI美化
        """
        self.output_func = output_func or print
        self.delay = 0.01  # 输出延迟，单位：秒
        self.enable_ui_enhancement = enable_ui_enhancement and UI_ENHANCED_AVAILABLE
        self.current_agent = None  # 当前发言的智能体

    async def stream_output(self, text: str, delay: Optional[float] = None) -> None:
        """
        流式输出文本

        Args:
            text: 文本内容
            delay: 输出延迟，单位：秒
        """
        delay = delay or self.delay
        
        # 如果延迟为0，直接输出
        if delay <= 0:
            self.output_func(text)
            return
        
        # 流式输出
        for char in text:
            self.output_func(char, end="", flush=True)
            await asyncio.sleep(delay)
        
        # 输出换行
        self.output_func("", flush=True)

    async def stream_output_chunk(self, text: str, chunk_size: int = 5, delay: Optional[float] = None) -> None:
        """
        分块流式输出文本

        Args:
            text: 文本内容
            chunk_size: 块大小
            delay: 输出延迟，单位：秒
        """
        delay = delay or self.delay
        
        # 如果延迟为0，直接输出
        if delay <= 0:
            self.output_func(text)
            return
        
        # 分块流式输出
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            self.output_func(chunk, end="", flush=True)
            await asyncio.sleep(delay)
        
        # 输出换行
        self.output_func("", flush=True)

    def set_delay(self, delay: float) -> None:
        """
        设置输出延迟

        Args:
            delay: 输出延迟，单位：秒
        """
        self.delay = max(0, delay)

    def set_output_func(self, output_func: Callable[[str], None]) -> None:
        """
        设置输出函数

        Args:
            output_func: 输出函数
        """
        self.output_func = output_func

    def set_current_agent(self, agent_name: str, agent_type: str = "") -> None:
        """
        设置当前发言的智能体

        Args:
            agent_name: 智能体名称
            agent_type: 智能体类型
        """
        self.current_agent = {
            "name": agent_name,
            "type": agent_type
        }

    async def stream_enhanced_output(self, text: str, message_type: str = "normal", delay: Optional[float] = None) -> None:
        """
        增强版流式输出

        Args:
            text: 文本内容
            message_type: 消息类型 (introduction, discussion, system, etc.)
            delay: 输出延迟
        """
        if not self.enable_ui_enhancement:
            await self.stream_output(text, delay)
            return

        delay = delay or self.delay

        # 根据消息类型进行美化
        if message_type == "introduction_header":
            # 智能体自我介绍标题
            separator = EnhancedColors.rainbow_text(Decorations.create_separator(60, "="))
            self.output_func(separator)
            title = EnhancedColors.bright_cyan("智能体自我介绍")
            self.output_func(f"\n{title}\n")
            separator = EnhancedColors.rainbow_text(Decorations.create_separator(60, "="))
            self.output_func(separator)
            self.output_func("")

        elif message_type == "agent_introduction":
            # 智能体介绍
            if self.current_agent:
                agent_name = self.current_agent["name"]
                agent_type = self.current_agent["type"]
                icon = Icons.get_agent_icon(agent_type) if agent_type else "🤖"

                # 美化的智能体标题
                header = f"===== {icon} {agent_name} 发言 ====="
                colored_header = EnhancedColors.bright_green(header)
                self.output_func(colored_header)
                self.output_func("")

                # 流式输出内容
                await self._stream_with_typewriter(text, delay)
                self.output_func("")
            else:
                await self.stream_output(text, delay)

        elif message_type == "discussion_header":
            # 讨论阶段标题
            separator = EnhancedColors.bright_blue(Decorations.create_separator(60, "─"))
            self.output_func(separator)
            title = EnhancedColors.bright_yellow("🎯 圆桌讨论阶段")
            self.output_func(f"\n{title}\n")
            separator = EnhancedColors.bright_blue(Decorations.create_separator(60, "─"))
            self.output_func(separator)
            self.output_func("")

        elif message_type == "agent_discussion":
            # 智能体讨论发言
            if self.current_agent:
                agent_name = self.current_agent["name"]
                agent_type = self.current_agent["type"]
                icon = Icons.get_agent_icon(agent_type) if agent_type else "🤖"

                # 美化的发言标题
                header = f"💬 {icon} {agent_name}:"
                colored_header = EnhancedColors.bright_magenta(header)
                self.output_func(colored_header)

                # 流式输出内容
                await self._stream_with_typewriter(text, delay)
                self.output_func("")
            else:
                await self.stream_output(text, delay)

        elif message_type == "system":
            # 系统消息
            system_text = EnhancedColors.bright_cyan(f"ℹ {text}")
            self.output_func(system_text)

        elif message_type == "waiting":
            # 等待消息（带加载动画）
            await self._show_waiting_animation(text)

        else:
            # 默认输出
            await self.stream_output(text, delay)

    async def _stream_with_typewriter(self, text: str, delay: float) -> None:
        """
        打字机效果的流式输出
        """
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            await asyncio.sleep(delay)
        sys.stdout.write("\n")
        sys.stdout.flush()

    async def _show_waiting_animation(self, message: str, duration: float = 2.0) -> None:
        """
        显示等待动画
        """
        frames = ASCIIArt.LOADING_FRAMES
        start_time = time.time()
        frame_index = 0

        while time.time() - start_time < duration:
            frame = frames[frame_index % len(frames)]
            colored_frame = EnhancedColors.bright_cyan(frame)
            text = f"\r{colored_frame} {message}..."

            sys.stdout.write(text)
            sys.stdout.flush()

            await asyncio.sleep(0.1)
            frame_index += 1

        # 清除加载动画
        sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')
        sys.stdout.flush()
