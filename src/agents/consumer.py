#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
消费者智能体模块
"""

import logging
import random
from typing import Dict, List, Any, Optional

from src.core.agent import Agent
from src.core.memory_adapter import MemoryAdapter
from src.models.base import BaseModel


class Consumer(Agent):
    """消费者智能体类"""

    def __init__(
        self,
        agent_id: str,
        name: str,
        model: BaseModel,
        memory: MemoryAdapter,
        **kwargs
    ):
        """
        初始化消费者智能体

        Args:
            agent_id: 智能体ID
            name: 智能体名称
            model: AI模型
            memory: 记忆模块
            **kwargs: 其他参数
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="consumer",
            name=name,
            model=model,
            memory=memory
        )

        # 消费者特定属性
        consumer_id = int(agent_id.split("_")[-1]) if "_" in agent_id else 1

        # 根据消费者ID设置不同的属性
        if consumer_id == 1:
            # 第一个消费者：学生，23岁
            self.age = kwargs.get("age", 23)
            self.background = kwargs.get("background", "学生")
            self.experience = kwargs.get("experience", "少数民族，喜欢购买具有文化特色的手工艺品")
            self.interests = kwargs.get("interests", ["文化", "艺术", "手工艺品"])
        elif consumer_id == 2:
            # 第二个消费者：自由职业者，27岁
            self.age = kwargs.get("age", 27)
            self.background = kwargs.get("background", "自由职业者")
            self.experience = kwargs.get("experience", "喜欢旅游，经常购买文化创意品")
            self.interests = kwargs.get("interests", ["旅游", "文化创意", "收藏"])
        else:
            # 第三个消费者：学生，22岁
            self.age = kwargs.get("age", 22)
            self.background = kwargs.get("background", "学生")
            self.experience = kwargs.get("experience", "经常购买文化创意品")
            self.interests = kwargs.get("interests", ["设计", "创意", "时尚"])

        # 消费者通用属性
        self.gender = kwargs.get("gender", random.choice(["男", "女"]))
        self.preferences = kwargs.get("preferences", {
            "price_sensitivity": random.uniform(0.3, 0.9),  # 价格敏感度
            "quality_focus": random.uniform(0.5, 1.0),      # 质量关注度
            "design_focus": random.uniform(0.4, 0.9),       # 设计关注度
            "tradition_value": random.uniform(0.3, 0.8)     # 传统价值关注度
        })

        self.logger = logging.getLogger(f"agent.consumer.{agent_id}")

    async def evaluate_product(self, product: str) -> str:
        """
        评估产品

        Args:
            product: 产品描述

        Returns:
            评估结果
        """
        self.logger.info(f"消费者 {self.name} 正在评估产品")

        from src.config.prompts.agent_prompts import ConsumerPrompts
        from src.config.prompts.template_manager import PromptTemplates

        # 构建包含个人信息的产品描述
        product_with_info = f"""
        产品描述：{product}

        消费者基本信息：
        - 年龄：{self.age}岁
        - 性别：{self.gender}
        - 背景：{self.background}
        - 经验：{self.experience}
        - 兴趣：{', '.join(self.interests)}
        """

        # 使用专门的消费者产品评估提示词
        prompt = ConsumerPrompts.get_product_evaluation_prompt(product_with_info)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate(prompt, system_prompt)

        # 将评估结果存入记忆
        await self.memory.add_memory(
            "product_evaluation",
            {
                "role": self.current_role,
                "product": product,
                "evaluation": response
            }
        )

        return response

    async def suggest_improvements(self, product: str) -> List[str]:
        """
        建议产品改进

        Args:
            product: 产品描述

        Returns:
            改进建议列表
        """
        self.logger.info(f"消费者 {self.name} 正在建议产品改进")

        from src.config.prompts.agent_prompts import ConsumerPrompts
        from src.config.prompts.template_manager import PromptTemplates

        # 构建包含个人信息的产品描述
        product_with_info = f"""
        产品描述：{product}

        消费者基本信息：
        - 年龄：{self.age}岁
        - 性别：{self.gender}
        - 背景：{self.background}
        - 经验：{self.experience}
        - 兴趣：{', '.join(self.interests)}
        """

        # 使用专门的消费者产品改进建议提示词
        prompt = ConsumerPrompts.get_product_improvement_prompt(product_with_info)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate(prompt, system_prompt)

        # 解析改进建议
        try:
            import json
            improvements = json.loads(response)
            suggestions = [imp.get("suggestion", "") for imp in improvements]
        except:
            # 解析失败时的备选方案
            import re
            suggestions = re.findall(r'"suggestion":\s*"([^"]+)"', response)
            if not suggestions:
                suggestions = ["提高产品质量", "降低价格", "增加文化元素", "改进包装设计", "增加实用功能"]

        # 将改进建议存入记忆
        await self.memory.add_memory(
            "improvement_suggestion",
            {
                "role": self.current_role,
                "product": product,
                "suggestions": suggestions
            }
        )

        return suggestions

    async def evaluate_market_potential(self, design: str) -> str:
        """
        评估设计的市场潜力

        Args:
            design: 设计方案

        Returns:
            市场潜力评估
        """
        self.logger.info(f"消费者 {self.name} 正在评估设计的市场潜力")

        from src.config.prompts.template_manager import PromptTemplates
        
        # 构建包含个人信息的设计描述
        design_with_info = f"""
        设计描述：{design}

        消费者基本信息：
        - 年龄：{self.age}岁
        - 性别：{self.gender}
        - 背景：{self.background}
        - 经验：{self.experience}
        - 兴趣：{', '.join(self.interests)}
        """

        # 使用专门的消费者设计市场潜力评估提示词
        prompt = ConsumerPrompts.get_design_market_potential_prompt(design_with_info)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate(prompt, system_prompt)

        # 将市场潜力评估存入记忆
        await self.memory.add_memory(
            "design_market_potential",
            {
                "role": self.current_role,
                "design": design,
                "potential": response
            }
        )

        return response

    async def provide_feedback(self, design: str) -> str:
        """
        针对设计方案提供反馈

        Args:
            design: 设计方案

        Returns:
            反馈意见
        """
        self.logger.info(f"消费者 {self.name} 正在针对设计方案提供反馈")

        from src.config.prompts.template_manager import PromptTemplates

        # 构建包含个人信息的设计描述
        design_with_info = f"""
        设计描述：{design}

        消费者基本信息：
        - 年龄：{self.age}岁
        - 性别：{self.gender}
        - 背景：{self.background}
        - 经验：{self.experience}
        - 兴趣：{', '.join(self.interests)}
        """

        # 使用专门的消费者设计反馈提示词
        prompt = ConsumerPrompts.get_design_feedback_prompt(design_with_info)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)
        response = await self.model.generate(prompt, system_prompt)

        # 将反馈意见存入记忆
        await self.memory.add_memory(
            "design_feedback",
            {
                "role": self.current_role,
                "design": design,
                "feedback": response
            }
        )

        return response
