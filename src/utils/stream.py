#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
流式输出处理模块
"""

import sys
import time
import asyncio
from typing import Callable, Optional


class StreamHandler:
    """流式输出处理类"""

    def __init__(self, output_func: Optional[Callable[[str], None]] = None):
        """
        初始化流式输出处理器

        Args:
            output_func: 输出函数，默认为 print
        """
        self.output_func = output_func or print
        self.delay = 0.01  # 输出延迟，单位：秒

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
