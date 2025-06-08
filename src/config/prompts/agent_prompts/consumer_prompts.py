#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
消费者智能体提示词模块
包含消费者相关的所有提示词
"""

from typing import Dict, List


class ConsumerPrompts:
    """消费者提示词类"""
    
    # 角色描述
    ROLE_DESCRIPTION = """你是一位消费者，关注产品的使用体验和价值。
你代表市场上的普通用户，关心产品的实用性、美观性、价格和耐用性。
你的意见反映了大众消费者的需求和偏好，对产品的市场接受度有重要参考价值。"""
    
    # 消费者类型定义
    CONSUMER_TYPES = {
        "student": {
            "age": 23,
            "background": "学生",
            "characteristics": "少数民族，喜欢购买具有文化特色的手工艺品",
            "focus": ["文化价值", "价格敏感", "个性化", "教育意义"]
        },
        "freelancer": {
            "age": 27,
            "background": "自由职业者",
            "characteristics": "喜欢旅游，经常购买文化创意品",
            "focus": ["便携性", "纪念价值", "独特性", "品质"]
        },
        "young_professional": {
            "age": 22,
            "background": "学生",
            "characteristics": "经常购买文化创意品",
            "focus": ["时尚性", "实用性", "社交价值", "品牌认知"]
        }
    }
    
    # 产品评估提示词
    PRODUCT_EVALUATION_PROMPT = """
作为一名消费者，请评估以下剪纸文创产品：

产品描述：
{product_description}

请从消费者角度评估以下方面：
1. 实用性：产品的实际使用价值
2. 美观性：视觉吸引力和设计美感
3. 价格合理性：性价比评估
4. 耐用性：产品质量和使用寿命
5. 文化价值：文化内涵和教育意义
6. 购买意愿：是否愿意购买及原因

请提供具体的评价和建议。
"""
    
    # 市场需求分析提示词
    MARKET_DEMAND_PROMPT = """
作为消费者代表，请分析以下产品的市场需求：

产品概念：
{product_concept}

请分析：
1. 目标用户群体
2. 市场需求程度
3. 竞争产品对比
4. 价格接受范围
5. 销售渠道建议
6. 营销策略建议

请基于消费者视角提供市场分析。
"""
    
    # 用户体验反馈提示词
    USER_EXPERIENCE_PROMPT = """
作为产品用户，请提供以下产品的使用体验反馈：

产品信息：
{product_info}

使用场景：
{usage_scenario}

请反馈：
1. 使用便利性
2. 功能满足度
3. 外观满意度
4. 遇到的问题
5. 改进建议
6. 推荐指数（1-10分）

请提供真实的用户体验反馈。
"""
    
    # 购买决策分析提示词
    PURCHASE_DECISION_PROMPT = """
作为潜在消费者，请分析对以下产品的购买决策：

产品详情：
{product_details}

价格：{price}

请分析：
1. 购买动机
2. 决策因素
3. 顾虑和担忧
4. 对比考虑的产品
5. 最终决策
6. 决策理由

请模拟真实的消费者购买决策过程。
"""

    # 产品改进建议提示词
    PRODUCT_IMPROVEMENT_PROMPT = """
作为消费者，请为以下产品提供改进建议：

{product_description}

请提供3-5条具体的改进建议，这些建议应该能够提高产品的吸引力、实用性或文化价值。

请以JSON格式返回改进建议列表，格式如下：
[
    {{"aspect": "改进方面", "suggestion": "具体建议", "reason": "原因说明"}},
    ...
]

请基于消费者的实际需求和使用体验提供建议。
"""

    @staticmethod
    def get_role_description(consumer_type: str = "general") -> str:
        """
        获取角色描述
        
        Args:
            consumer_type: 消费者类型
            
        Returns:
            角色描述
        """
        if consumer_type in ConsumerPrompts.CONSUMER_TYPES:
            type_info = ConsumerPrompts.CONSUMER_TYPES[consumer_type]
            return f"""你是一位{type_info['age']}岁的{type_info['background']}，{type_info['characteristics']}。
你关注产品的{', '.join(type_info['focus'])}等方面。
{ConsumerPrompts.ROLE_DESCRIPTION}"""
        return ConsumerPrompts.ROLE_DESCRIPTION
    
    @staticmethod
    def get_product_evaluation_prompt(product_description: str) -> str:
        """
        获取产品评估提示词
        
        Args:
            product_description: 产品描述
            
        Returns:
            格式化的产品评估提示词
        """
        return ConsumerPrompts.PRODUCT_EVALUATION_PROMPT.format(
            product_description=product_description
        )
    
    @staticmethod
    def get_market_demand_prompt(product_concept: str) -> str:
        """
        获取市场需求分析提示词
        
        Args:
            product_concept: 产品概念
            
        Returns:
            格式化的市场需求分析提示词
        """
        return ConsumerPrompts.MARKET_DEMAND_PROMPT.format(
            product_concept=product_concept
        )
    
    @staticmethod
    def get_user_experience_prompt(product_info: str, usage_scenario: str) -> str:
        """
        获取用户体验反馈提示词
        
        Args:
            product_info: 产品信息
            usage_scenario: 使用场景
            
        Returns:
            格式化的用户体验反馈提示词
        """
        return ConsumerPrompts.USER_EXPERIENCE_PROMPT.format(
            product_info=product_info,
            usage_scenario=usage_scenario
        )
    
    @staticmethod
    def get_purchase_decision_prompt(product_details: str, price: str) -> str:
        """
        获取购买决策分析提示词
        
        Args:
            product_details: 产品详情
            price: 价格
            
        Returns:
            格式化的购买决策分析提示词
        """
        return ConsumerPrompts.PURCHASE_DECISION_PROMPT.format(
            product_details=product_details,
            price=price
        )
    
    @staticmethod
    def get_product_improvement_prompt(product_description: str) -> str:
        """
        获取产品改进建议提示词

        Args:
            product_description: 产品描述

        Returns:
            格式化的产品改进建议提示词
        """
        return ConsumerPrompts.PRODUCT_IMPROVEMENT_PROMPT.format(
            product_description=product_description
        )

    @staticmethod
    def get_consumer_types() -> Dict[str, Dict]:
        """
        获取消费者类型定义

        Returns:
            消费者类型字典
        """
        return ConsumerPrompts.CONSUMER_TYPES.copy()