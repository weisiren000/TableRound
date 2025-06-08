#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
设计师智能体模块
"""

import logging
import random
from typing import Dict, List, Any, Optional

from typing import Union
from src.core.agent import Agent
from src.core.memory import Memory
from src.core.memory_adapter import MemoryAdapter
from src.models.base import BaseModel


class Designer(Agent):
    """设计师智能体类"""

    def __init__(
        self,
        agent_id: str,
        name: str,
        model: BaseModel,
        memory: Union[Memory, MemoryAdapter],
        **kwargs
    ):
        """
        初始化设计师智能体

        Args:
            agent_id: 智能体ID
            name: 智能体名称
            model: AI模型
            memory: 记忆模块
            **kwargs: 其他参数
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="designer",
            name=name,
            model=model,
            memory=memory
        )

        # 设计师特定属性
        self.age = kwargs.get("age", 23)  # 年龄：23岁
        self.background = kwargs.get("background", "研究生")  # 人物介绍
        self.experience = kwargs.get("experience", "有四年产品设计经验")  # 相关经历
        self.design_style = kwargs.get("design_style", "融合传统与现代")
        self.specialties = kwargs.get("specialties", ["视觉设计", "产品设计", "文创设计"])
        self.design_philosophy = kwargs.get("design_philosophy", "在尊重传统的基础上创新，追求美学与实用的平衡")

        self.logger = logging.getLogger(f"agent.designer.{agent_id}")

    async def create_design_concept(self, keywords: List[str]) -> str:
        """
        创建设计概念

        Args:
            keywords: 关键词列表

        Returns:
            设计概念
        """
        self.logger.info(f"设计师 {self.name} 正在创建设计概念")

        from src.config.prompts import PromptTemplates
        prompt = f"""
        作为一名有四年经验的产品设计师，请基于以下关键词创建一个剪纸文创产品的设计概念：

        关键词：{', '.join(keywords)}

        你的基本信息：
        - 年龄：{self.age}岁
        - 背景：{self.background}
        - 经验：{self.experience}
        - 设计风格：{self.design_style}
        - 设计理念：{self.design_philosophy}

        请创建一个详细的设计概念，包括：
        1. 产品形式和功能
        2. 设计灵感和理念
        3. 视觉风格和元素
        4. 材质和工艺建议
        5. 目标用户群体
        6. 使用场景

        请确保设计概念围绕"对称的剪纸风格的中国传统蝙蝠吉祥纹样"这一主题，同时融入关键词中的元素。
        """

        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate(prompt, system_prompt)

        # 将设计概念存入记忆
        self.memory.add_memory(
            "design_concept",
            {
                "role": self.current_role,
                "keywords": keywords,
                "concept": response
            }
        )

        return response

    async def generate_design_prompt(self, design_concept: str) -> str:
        """
        生成设计提示词

        Args:
            design_concept: 设计概念

        Returns:
            设计提示词
        """
        self.logger.info(f"设计师 {self.name} 正在生成设计提示词")

        from src.config.prompts.agent_prompts import DesignerPrompts
        from src.config.prompts import PromptTemplates

        # 使用专门的设计师AI图像生成提示词创作提示词
        prompt = DesignerPrompts.get_ai_image_prompt_generation(design_concept)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate(prompt, system_prompt)

        # 将设计提示词存入记忆
        self.memory.add_memory(
            "design_prompt",
            {
                "role": self.current_role,
                "concept": design_concept,
                "prompt": response
            }
        )

        return response

    async def analyze_design_image(self, image_path: str) -> str:
        """
        分析设计图像

        Args:
            image_path: 图像路径

        Returns:
            分析结果
        """
        self.logger.info(f"设计师 {self.name} 正在分析设计图像")

        # 检查模型是否支持图像
        if not self.model.supports_vision():
            return "该模型不支持图像处理"

        from src.config.prompts.agent_prompts import DesignerPrompts
        from src.config.prompts import PromptTemplates

        # 使用专门的设计师图像分析提示词
        prompt = DesignerPrompts.get_design_image_analysis_prompt()
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate_with_image(prompt, system_prompt, image_path)

        # 将分析结果存入记忆
        self.memory.add_memory(
            "design_analysis",
            {
                "role": self.current_role,
                "image_path": image_path,
                "analysis": response
            }
        )

        return response
