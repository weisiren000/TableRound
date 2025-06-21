#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
制造商人智能体模块
"""

import logging
from typing import Dict, List

from src.core.agent import Agent
from src.core.memory_adapter import MemoryAdapter
from src.models.base import BaseModel


class Manufacturer(Agent):
    """制造商人智能体类"""

    def __init__(
        self,
        agent_id: str,
        name: str,
        model: BaseModel,
        memory: MemoryAdapter,
        **kwargs
    ):
        """
        初始化制造商人智能体

        Args:
            agent_id: 智能体ID
            name: 智能体名称
            model: AI模型
            memory: 记忆模块
            **kwargs: 其他参数
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="manufacturer",
            name=name,
            model=model,
            memory=memory
        )

        # 制造商人特定属性
        self.age = kwargs.get("age", 35)  # 年龄：35岁
        self.background = kwargs.get("background", "文化创意产品生产商")  # 人物介绍
        self.experience = kwargs.get("experience", "对文化创意产品的市场有相关了解，从事有四年手工艺品生产和开发的基础")  # 相关经历
        self.company_size = kwargs.get("company_size", "中型")  # 小型、中型、大型
        self.production_capacity = kwargs.get("production_capacity", 5000)  # 每月产能
        self.specialties = kwargs.get("specialties", ["文创产品", "工艺品", "纪念品"])
        self.manufacturing_methods = kwargs.get("manufacturing_methods", ["手工制作", "半自动化", "定制化生产"])

        self.logger = logging.getLogger(f"agent.manufacturer.{agent_id}")

    async def evaluate_feasibility(self, design: str) -> str:
        """
        评估设计方案的可行性

        Args:
            design: 设计方案

        Returns:
            可行性评估结果
        """
        self.logger.info(f"制造商 {self.name} 正在评估设计方案的可行性")

        from src.config.prompts.agent_prompts import ManufacturerPrompts
        from src.config.prompts.template_manager import PromptTemplates

        # 构建包含制造商信息的设计描述
        design_with_info = f"""
        设计方案：{design}

        制造商基本信息：
        - 年龄：{self.age}岁
        - 背景：{self.background}
        - 经验：{self.experience}
        - 公司规模：{self.company_size}
        - 月产能：{self.production_capacity}件
        - 制造方法：{', '.join(self.manufacturing_methods)}
        """

        # 使用专门的制造商生产可行性评估提示词
        prompt = ManufacturerPrompts.get_production_feasibility_prompt(design_with_info)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate(prompt, system_prompt)

        # 将评估结果存入记忆
        await self.memory.add_memory(
            "feasibility_evaluation",
            {
                "role": self.current_role,
                "design": design,
                "evaluation": response
            }
        )

        return response

    async def estimate_costs(self, design: str) -> Dict[str, float]:
        """
        估算生产成本

        Args:
            design: 设计方案

        Returns:
            成本估算结果
        """
        self.logger.info(f"制造商 {self.name} 正在估算生产成本")

        from src.config.prompts.agent_prompts import ManufacturerPrompts
        from src.config.prompts.template_manager import PromptTemplates

        # 使用专门的制造商成本估算提示词
        prompt = ManufacturerPrompts.get_cost_estimation_prompt(design)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate(prompt, system_prompt)

        # 解析成本估算
        try:
            import json
            costs = json.loads(response)
        except:
            # 解析失败时的备选方案
            costs = {
                "material_cost": 20.0,
                "labor_cost": 15.0,
                "equipment_cost": 5.0,
                "packaging_cost": 8.0,
                "shipping_cost": 7.0,
                "other_cost": 5.0,
                "total_cost": 60.0,
                "unit_price": 99.0,
                "profit_margin": 0.4
            }

        # 将成本估算存入记忆
        await self.memory.add_memory(
            "cost_estimation",
            {
                "role": self.current_role,
                "design": design,
                "costs": costs
            }
        )

        return costs

    async def suggest_production_plan(self, design: str) -> str:
        """
        针对设计方案提供生产建议

        Args:
            design: 设计方案

        Returns:
            生产建议
        """
        self.logger.info(f"制造商 {self.name} 正在提供生产建议")

        from src.config.prompts.template_manager import PromptTemplates
        
        # ... existing code ...

    async def estimate_production_cost(self, design: str) -> str:
        """
        估算设计方案的生产成本

        Args:
            design: 设计方案

        Returns:
            成本估算
        """
        self.logger.info(f"制造商 {self.name} 正在估算生产成本")

        from src.config.prompts.template_manager import PromptTemplates
