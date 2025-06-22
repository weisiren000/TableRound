#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
手工艺人智能体模块
"""

import logging
from typing import List

from src.core.agent import Agent
from src.core.memory_adapter import MemoryAdapter
from src.models.base import BaseModel


class Craftsman(Agent):
    """手工艺人智能体类"""

    def __init__(
        self,
        agent_id: str,
        name: str,
        model: BaseModel,
        memory: MemoryAdapter,
        **kwargs
    ):
        """
        初始化手工艺人智能体

        Args:
            agent_id: 智能体ID
            name: 智能体名称
            model: AI模型
            memory: 记忆模块
            **kwargs: 其他参数
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="craftsman",
            name=name,
            model=model,
            memory=memory
        )

        # 手工艺人特定属性
        self.age = kwargs.get("age", 60)  # 年龄：60岁
        self.background = kwargs.get("background", "蒙古族传统剪纸承人")  # 人物介绍
        self.experience = kwargs.get("experience", "从事蒙古族剪纸技艺长达40年")  # 相关经历
        # 如果没有指定名字，使用默认的固定名字
        if name == "手工艺人1" or name.startswith("手工艺人"):
            self.name = "巴雅尔"
        self.crafts = kwargs.get("crafts", ["剪纸", "刺绣", "木雕", "陶艺"])
        self.specialties = kwargs.get("specialties", ["传统工艺", "文化传承", "手工制作"])

        self.logger = logging.getLogger(f"agent.craftsman.{agent_id}")

    async def evaluate_design(self, design: str) -> str:
        """
        评估设计的可行性和传统工艺价值

        Args:
            design: 设计方案

        Returns:
            评估结果
        """
        self.logger.info(f"手工艺人 {self.name} 正在评估设计方案")

        from src.config.prompts.template_manager import PromptTemplates
        from src.config.prompts.agent_prompts import CraftsmanPrompts

        # 使用专门的手工艺人设计评估提示词
        prompt = CraftsmanPrompts.get_design_evaluation_prompt(design)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate(prompt, system_prompt)

        # 将评估结果存入记忆
        await self.memory.add_memory(
            "design_evaluation",
            {
                "role": self.current_role,
                "design": design,
                "evaluation": response
            }
        )

        return response

    async def suggest_materials(self, design: str) -> List[str]:
        """
        为设计建议合适的材料

        Args:
            design: 设计方案

        Returns:
            材料建议
        """
        self.logger.info(f"手工艺人 {self.name} 正在为设计建议材料")

        from src.config.prompts.template_manager import PromptTemplates
        from src.config.prompts.agent_prompts import CraftsmanPrompts

        # 使用专门的手工艺人材料建议提示词
        prompt = CraftsmanPrompts.get_material_suggestion_prompt(design)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate(prompt, system_prompt)

        # 解析材料列表
        try:
            import json
            materials = json.loads(response)
            material_names = [m.get("name", "") for m in materials]
        except:
            # 解析失败时的备选方案
            import re
            material_names = re.findall(r'"name":\s*"([^"]+)"', response)
            if not material_names:
                material_names = ["宣纸", "彩纸", "牛皮纸", "丝绸", "木材"]

        # 将材料建议存入记忆
        await self.memory.add_memory(
            "material_suggestion",
            {
                "role": self.current_role,
                "design": design,
                "materials": material_names
            }
        )

        return material_names
