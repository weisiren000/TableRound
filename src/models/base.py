#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
模型基类模块
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Callable


class BaseModel(ABC):
    """模型基类"""

    def __init__(self, model_name: str, **kwargs):
        """
        初始化模型

        Args:
            model_name: 模型名称
            **kwargs: 其他参数
        """
        self.model_name = model_name
        self.logger = logging.getLogger(f"model.{model_name}")

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        生成文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词

        Returns:
            生成的文本
        """
        pass

    @abstractmethod
    async def generate_with_image(self, prompt: str, system_prompt: str, image_path: str) -> str:
        """
        基于图像生成文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词
            image_path: 图像路径

        Returns:
            生成的文本
        """
        pass

    @abstractmethod
    async def generate_stream(
        self, 
        prompt: str, 
        system_prompt: str = "", 
        callback: Callable[[str], None] = None
    ) -> str:
        """
        流式生成文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词
            callback: 回调函数，用于处理流式输出

        Returns:
            生成的完整文本
        """
        pass

    def supports_vision(self) -> bool:
        """
        是否支持图像处理

        Returns:
            是否支持图像处理
        """
        return False
