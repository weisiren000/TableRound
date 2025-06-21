#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
场景设置功能提示词模块
包含各种场景设置相关的提示词
"""

from typing import Dict, List


class ScenarioPrompts:
    """场景设置提示词类"""
    
    # 剪纸研讨会场景
    PAPER_CUTTING_WORKSHOP_SCENARIO = """
场景：你们正在参加一个剪纸文创产品设计研讨会。

研讨会目标：设计出一个让消费者都满意的剪纸文创产品，以对称的剪纸风格的中国传统蝙蝠吉祥纹样为设计主题。

蝙蝠在中国传统文化中象征着福气，因为"蝠"与"福"谐音。对称的剪纸风格是中国传统民间艺术的重要表现形式，具有浓厚的文化底蕴和艺术价值。

在这个研讨会中，每位参与者都应该基于自己的专业背景和经验，为剪纸文创产品设计提供独特的见解和建议。最终，你们需要共同设计出一个既保留传统文化元素，又符合现代审美和使用需求的剪纸文创产品。
"""
    
    # 产品发布会场景
    PRODUCT_LAUNCH_SCENARIO = """
场景：你们正在参加一个文创产品发布会的策划会议。

会议背景：
- 产品：{product_name}
- 发布时间：{launch_date}
- 目标市场：{target_market}
- 预算范围：{budget_range}

会议目标：
1. 确定产品发布策略
2. 设计营销推广方案
3. 制定媒体宣传计划
4. 规划用户体验活动
5. 评估市场风险和机会

每位参与者需要从自己的专业角度提供建议，共同制定一个成功的产品发布方案。
"""
    
    # 设计评审会场景
    DESIGN_REVIEW_SCENARIO = """
场景：你们正在参加一个设计方案评审会。

评审对象：{design_object}
评审阶段：{review_stage}

评审标准：
1. 创新性和独特性
2. 实用性和功能性
3. 美学价值和视觉效果
4. 技术可行性
5. 市场潜力
6. 成本控制
7. 文化价值

评审流程：
1. 设计方案展示
2. 各专业角度分析
3. 问题识别和讨论
4. 改进建议提出
5. 最终评审结论

请各位专家基于自己的专业背景，对设计方案进行全面评审。
"""
    
    @staticmethod
    def get_paper_cutting_workshop_scenario() -> str:
        """
        获取剪纸研讨会场景
        
        Returns:
            剪纸研讨会场景描述
        """
        return ScenarioPrompts.PAPER_CUTTING_WORKSHOP_SCENARIO
    
    @staticmethod
    def get_product_launch_scenario(product_name: str, launch_date: str,
                                  target_market: str, budget_range: str) -> str:
        """
        获取产品发布会场景
        
        Args:
            product_name: 产品名称
            launch_date: 发布时间
            target_market: 目标市场
            budget_range: 预算范围
            
        Returns:
            格式化的产品发布会场景
        """
        return ScenarioPrompts.PRODUCT_LAUNCH_SCENARIO.format(
            product_name=product_name,
            launch_date=launch_date,
            target_market=target_market,
            budget_range=budget_range
        )
    
    @staticmethod
    def get_design_review_scenario(design_object: str, review_stage: str) -> str:
        """
        获取设计评审会场景
        
        Args:
            design_object: 评审对象
            review_stage: 评审阶段
            
        Returns:
            格式化的设计评审会场景
        """
        return ScenarioPrompts.DESIGN_REVIEW_SCENARIO.format(
            design_object=design_object,
            review_stage=review_stage
        )