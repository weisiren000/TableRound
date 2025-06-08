#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
模拟模型模块，用于测试
"""

import logging
from typing import Dict, List, Any, Optional

from src.models.base import BaseModel


class MockModel(BaseModel):
    """模拟模型类"""

    def __init__(self, model_name: str = "mock_model", **kwargs):
        """
        初始化模拟模型

        Args:
            model_name: 模型名称
            **kwargs: 其他参数
        """
        super().__init__(model_name=model_name, **kwargs)
        self.logger = logging.getLogger("model.mock")
        self.logger.info("初始化模拟模型")

    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """
        生成文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词

        Returns:
            生成的文本
        """
        self.logger.debug(f"生成文本，提示词长度: {len(prompt)}")

        # 根据提示词类型返回不同的模拟响应
        if "自我介绍" in prompt or "介绍自己" in prompt:
            return "这是一个模拟的自我介绍。我是一个测试智能体，用于测试系统功能。"

        elif "角色转换" in prompt or "从原来的" in prompt:
            return "我现在已经从原来的角色转换为新角色。作为新角色，我将从新的视角思考问题，但保持记忆的连续性。"

        elif "讨论" in prompt:
            return "这是一个模拟的讨论回复。作为我当前的角色，我认为这个话题很有意思，我有以下几点看法..."

        elif "关键词" in prompt:
            return '["测试", "模拟", "关键词", "智能体", "系统"]'

        elif "设计卡牌" in prompt or "剪纸文创产品" in prompt:
            return """# 设计卡牌

## 产品形式
- 立体剪纸灯笼

## 设计元素
- 传统对称蝙蝠图案
- 中国红色调
- 金色点缀

## 功能特点
- 装饰性与实用性结合
- 可折叠便于存储
- LED灯源，节能环保

## 目标用户
- 25-45岁文化爱好者
- 家居装饰爱好者
- 传统文化收藏者

## 文化内涵
- 蝙蝠象征福气吉祥
- 红色象征喜庆与好运
- 传统与现代工艺结合
"""

        elif "投票" in prompt:
            return '["传统", "对称", "蝙蝠", "吉祥", "红色"]'

        elif "图片" in prompt or "故事" in prompt:
            return "这是一个模拟的图片故事。在这张图片中，我看到了..."

        else:
            return "这是一个模拟的回复，用于测试系统功能。"

    async def generate_with_image(self, prompt: str, system_prompt: str, image_path: str) -> str:
        """
        生成带图像的文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词
            image_path: 图像路径

        Returns:
            生成的文本
        """
        self.logger.debug(f"生成带图像的文本，提示词长度: {len(prompt)}，图像路径: {image_path}")
        return f"这是一个模拟的带图像的回复。我看到了图像 {image_path} 并生成了这个回复。"

    async def generate_stream(self, prompt: str, system_prompt: str = None) -> str:
        """
        流式生成文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词

        Returns:
            生成的文本
        """
        self.logger.debug(f"流式生成文本，提示词长度: {len(prompt)}")

        # 直接返回非流式生成的结果
        result = await self.generate(prompt, system_prompt)

        # 模拟流式输出
        for i in range(0, len(result), 10):
            chunk = result[i:i+10]
            yield chunk

    def supports_vision(self) -> bool:
        """
        是否支持视觉

        Returns:
            是否支持视觉
        """
        return True
