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
    
    # 市场调研会议场景
    MARKET_RESEARCH_SCENARIO = """
场景：你们正在参加一个市场调研分析会议。

调研主题：{research_topic}
调研范围：{research_scope}

会议议程：
1. 市场现状分析
2. 竞争对手研究
3. 消费者需求调研
4. 趋势预测分析
5. 机会点识别
6. 风险评估
7. 策略建议

数据来源：
- 行业报告：{industry_reports}
- 用户调研：{user_research}
- 竞品分析：{competitor_analysis}

请各位专家基于自己的专业领域，对市场调研数据进行深入分析。
"""
    
    # 创新工作坊场景
    INNOVATION_WORKSHOP_SCENARIO = """
场景：你们正在参加一个创新工作坊。

工作坊主题：{workshop_theme}
创新目标：{innovation_goals}

工作坊方法：
1. 头脑风暴阶段
2. 创意筛选阶段
3. 概念发展阶段
4. 原型设计阶段
5. 测试验证阶段

创新原则：
- 打破常规思维
- 鼓励大胆想象
- 注重实用性
- 考虑可行性
- 追求差异化

请各位参与者发挥创造力，从不同角度提出创新想法和解决方案。
"""
    
    # 危机处理会议场景
    CRISIS_MANAGEMENT_SCENARIO = """
场景：你们正在参加一个紧急危机处理会议。

危机情况：{crisis_situation}
影响范围：{impact_scope}
紧急程度：{urgency_level}

会议目标：
1. 快速评估危机影响
2. 制定应急处理方案
3. 分配责任和资源
4. 建立沟通机制
5. 制定恢复计划

处理原则：
- 快速响应
- 透明沟通
- 责任明确
- 资源协调
- 风险控制

请各位专家基于自己的专业经验，提供危机处理建议。
"""
    
    # 合作洽谈场景
    COLLABORATION_NEGOTIATION_SCENARIO = """
场景：你们正在参加一个合作项目洽谈会。

合作项目：{collaboration_project}
合作方：{collaboration_partners}
合作模式：{collaboration_model}

洽谈要点：
1. 合作目标和愿景
2. 各方资源和优势
3. 责任分工和权益
4. 风险分担机制
5. 收益分配方案
6. 合作期限和条件
7. 退出机制

洽谈原则：
- 互利共赢
- 优势互补
- 风险共担
- 透明合作
- 长期发展

请各位代表从自己的角度提出合作建议和关切。
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
    
    @staticmethod
    def get_market_research_scenario(research_topic: str, research_scope: str,
                                   industry_reports: str, user_research: str,
                                   competitor_analysis: str) -> str:
        """
        获取市场调研会议场景
        
        Args:
            research_topic: 调研主题
            research_scope: 调研范围
            industry_reports: 行业报告
            user_research: 用户调研
            competitor_analysis: 竞品分析
            
        Returns:
            格式化的市场调研会议场景
        """
        return ScenarioPrompts.MARKET_RESEARCH_SCENARIO.format(
            research_topic=research_topic,
            research_scope=research_scope,
            industry_reports=industry_reports,
            user_research=user_research,
            competitor_analysis=competitor_analysis
        )
    
    @staticmethod
    def get_innovation_workshop_scenario(workshop_theme: str, innovation_goals: str) -> str:
        """
        获取创新工作坊场景
        
        Args:
            workshop_theme: 工作坊主题
            innovation_goals: 创新目标
            
        Returns:
            格式化的创新工作坊场景
        """
        return ScenarioPrompts.INNOVATION_WORKSHOP_SCENARIO.format(
            workshop_theme=workshop_theme,
            innovation_goals=innovation_goals
        )
    
    @staticmethod
    def get_crisis_management_scenario(crisis_situation: str, impact_scope: str,
                                     urgency_level: str) -> str:
        """
        获取危机处理会议场景
        
        Args:
            crisis_situation: 危机情况
            impact_scope: 影响范围
            urgency_level: 紧急程度
            
        Returns:
            格式化的危机处理会议场景
        """
        return ScenarioPrompts.CRISIS_MANAGEMENT_SCENARIO.format(
            crisis_situation=crisis_situation,
            impact_scope=impact_scope,
            urgency_level=urgency_level
        )
    
    @staticmethod
    def get_collaboration_negotiation_scenario(collaboration_project: str,
                                             collaboration_partners: str,
                                             collaboration_model: str) -> str:
        """
        获取合作洽谈场景
        
        Args:
            collaboration_project: 合作项目
            collaboration_partners: 合作方
            collaboration_model: 合作模式
            
        Returns:
            格式化的合作洽谈场景
        """
        return ScenarioPrompts.COLLABORATION_NEGOTIATION_SCENARIO.format(
            collaboration_project=collaboration_project,
            collaboration_partners=collaboration_partners,
            collaboration_model=collaboration_model
        )