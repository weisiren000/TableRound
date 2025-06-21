#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
设计师智能体提示词模块
包含设计师相关的所有提示词
"""

from typing import Dict, List


class DesignerPrompts:
    """设计师提示词类"""
    
    # 角色描述
    ROLE_DESCRIPTION = """你是一位23岁的研究生设计师，有四年产品设计经验。
你擅长将创意转化为具体的设计方案，注重产品的视觉表达和用户体验。
你了解设计趋势和美学原则，能够平衡艺术性和实用性。

语言风格特点：
- 说话充满创意和想象力，经常用视觉化的语言描述
- 喜欢从美学和用户体验的角度分析问题
- 会引用设计理论和流行趋势来支持观点
- 语言比较年轻化，有时会用设计专业术语
- 善于发现细节，经常提出创新的想法
- 表达方式比较感性，注重情感和体验"""
    
    # 专业技能描述
    SKILLS = [
        "产品设计",
        "视觉设计",
        "用户体验设计",
        "创意思维",
        "美学理论",
        "设计软件应用"
    ]
    
    # 关注领域
    FOCUS_AREAS = [
        "视觉美感",
        "用户体验",
        "设计创新",
        "功能性设计",
        "文化表达",
        "设计趋势"
    ]
    
    # 设计方案创作提示词
    DESIGN_CREATION_PROMPT = """
作为一名产品设计师，请为以下需求创作设计方案：

设计需求：
{design_requirements}

设计主题：{theme}

请提供：
1. 设计理念和灵感来源
2. 视觉风格定义
3. 色彩搭配方案
4. 造型设计说明
5. 材质选择建议
6. 功能性设计考虑
7. 用户体验优化
8. 文化元素融入

请提供完整的设计方案说明。
"""
    
    # 视觉优化建议提示词
    VISUAL_OPTIMIZATION_PROMPT = """
作为设计师，请对以下设计进行视觉优化：

当前设计：
{current_design}

优化目标：
{optimization_goals}

请提供：
1. 视觉问题分析
2. 美学改进建议
3. 色彩调整方案
4. 比例优化建议
5. 细节完善措施
6. 整体协调性提升
7. 视觉冲击力增强

请提供详细的视觉优化方案。
"""
    
    # 用户体验设计提示词
    USER_EXPERIENCE_DESIGN_PROMPT = """
作为UX设计师，请为以下产品设计用户体验方案：

产品概念：
{product_concept}

目标用户：
{target_users}

请设计：
1. 用户使用流程
2. 交互方式设计
3. 功能布局优化
4. 易用性考虑
5. 无障碍设计
6. 情感化设计
7. 用户反馈机制

请提供完整的用户体验设计方案。
"""
    
    # 文化元素融入提示词
    CULTURAL_INTEGRATION_PROMPT = """
作为设计师，请将传统文化元素融入现代设计：

文化元素：
{cultural_elements}

现代应用场景：
{modern_context}

请提供：
1. 文化元素提取和抽象
2. 现代化转换方法
3. 视觉表现形式
4. 文化内涵保持
5. 现代审美适配
6. 创新融合方案
7. 文化传承价值

请提供文化与现代设计的融合方案。
"""
    
    # 设计评估与改进提示词
    DESIGN_EVALUATION_PROMPT = """
作为设计师，请评估以下设计方案：

设计方案：
{design_proposal}

评估标准：
{evaluation_criteria}

请评估：
1. 美学价值
2. 功能性
3. 创新性
4. 可实现性
5. 市场适应性
6. 文化表达力
7. 用户接受度

请提供专业的设计评估和改进建议。
"""
    
    # 设计趋势分析提示词
    DESIGN_TREND_ANALYSIS_PROMPT = """
作为设计师，请分析当前设计趋势对产品的影响：

产品类型：
{product_type}

市场环境：
{market_environment}

请分析：
1. 当前设计趋势
2. 流行元素识别
3. 色彩趋势分析
4. 材质趋势研究
5. 功能趋势预测
6. 用户偏好变化
7. 设计应用建议

请提供基于趋势的设计指导。
"""
    
    # 创意激发提示词
    CREATIVE_INSPIRATION_PROMPT = """
作为设计师，请为以下项目提供创意灵感：

项目背景：
{project_background}

创意方向：
{creative_direction}

请提供：
1. 灵感来源探索
2. 创意概念发散
3. 视觉元素提取
4. 设计语言定义
5. 创新点挖掘
6. 差异化策略
7. 创意实现路径

请提供丰富的创意灵感和设计思路。
"""
    
    # 设计规范制定提示词
    DESIGN_SPECIFICATION_PROMPT = """
作为设计师，请为以下产品制定设计规范：

产品系列：
{product_series}

品牌要求：
{brand_requirements}

请制定：
1. 视觉识别规范
2. 色彩使用标准
3. 字体应用规范
4. 图形元素标准
5. 布局设计原则
6. 材质选择指南
7. 质量控制标准

请提供完整的设计规范文档。
"""

    # AI图像生成提示词创作
    AI_IMAGE_PROMPT_GENERATION = """
作为一名有四年经验的产品设计师，请基于以下设计概念生成一个详细的设计提示词，用于AI图像生成：

设计概念：
{design_concept}

请生成一个详细的设计提示词，描述"对称的剪纸风格的中国传统蝙蝠吉祥纹样"的视觉特征。提示词应该包括：
1. 整体风格和氛围
2. 颜色方案
3. 构图和布局
4. 细节和纹理
5. 文化元素和象征意义

提示词应该详细具体，能够指导AI生成符合设计概念的图像。请确保提示词强调对称的剪纸风格和中国传统蝙蝠吉祥纹样的特点。
"""

    # 设计图像分析提示词
    DESIGN_IMAGE_ANALYSIS_PROMPT = """
作为一名有四年经验的产品设计师，请分析这张设计图像，重点关注"对称的剪纸风格的中国传统蝙蝠吉祥纹样"的表现。

请从以下几个方面进行分析：
1. 视觉风格和美感
2. 对称性和平衡感
3. 传统元素的运用
4. 色彩搭配
5. 细节处理
6. 文化内涵表达
7. 改进建议

请给出详细的分析意见，并提供具体的改进建议。
"""

    @staticmethod
    def get_role_description() -> str:
        """获取角色描述"""
        return DesignerPrompts.ROLE_DESCRIPTION
    
    @staticmethod
    def get_skills() -> List[str]:
        """获取专业技能列表"""
        return DesignerPrompts.SKILLS.copy()
    
    @staticmethod
    def get_focus_areas() -> List[str]:
        """获取关注领域列表"""
        return DesignerPrompts.FOCUS_AREAS.copy()
    
    @staticmethod
    def get_design_creation_prompt(design_requirements: str, theme: str) -> str:
        """
        获取设计方案创作提示词
        
        Args:
            design_requirements: 设计需求
            theme: 设计主题
            
        Returns:
            格式化的设计方案创作提示词
        """
        return DesignerPrompts.DESIGN_CREATION_PROMPT.format(
            design_requirements=design_requirements,
            theme=theme
        )
    
    @staticmethod
    def get_visual_optimization_prompt(current_design: str, optimization_goals: str) -> str:
        """
        获取视觉优化建议提示词
        
        Args:
            current_design: 当前设计
            optimization_goals: 优化目标
            
        Returns:
            格式化的视觉优化建议提示词
        """
        return DesignerPrompts.VISUAL_OPTIMIZATION_PROMPT.format(
            current_design=current_design,
            optimization_goals=optimization_goals
        )
    
    @staticmethod
    def get_user_experience_design_prompt(product_concept: str, target_users: str) -> str:
        """
        获取用户体验设计提示词
        
        Args:
            product_concept: 产品概念
            target_users: 目标用户
            
        Returns:
            格式化的用户体验设计提示词
        """
        return DesignerPrompts.USER_EXPERIENCE_DESIGN_PROMPT.format(
            product_concept=product_concept,
            target_users=target_users
        )
    
    @staticmethod
    def get_cultural_integration_prompt(cultural_elements: str, modern_context: str) -> str:
        """
        获取文化元素融入提示词
        
        Args:
            cultural_elements: 文化元素
            modern_context: 现代应用场景
            
        Returns:
            格式化的文化元素融入提示词
        """
        return DesignerPrompts.CULTURAL_INTEGRATION_PROMPT.format(
            cultural_elements=cultural_elements,
            modern_context=modern_context
        )
    
    @staticmethod
    def get_design_evaluation_prompt(design_proposal: str, evaluation_criteria: str) -> str:
        """
        获取设计评估与改进提示词
        
        Args:
            design_proposal: 设计方案
            evaluation_criteria: 评估标准
            
        Returns:
            格式化的设计评估与改进提示词
        """
        return DesignerPrompts.DESIGN_EVALUATION_PROMPT.format(
            design_proposal=design_proposal,
            evaluation_criteria=evaluation_criteria
        )
    
    @staticmethod
    def get_design_trend_analysis_prompt(product_type: str, market_environment: str) -> str:
        """
        获取设计趋势分析提示词
        
        Args:
            product_type: 产品类型
            market_environment: 市场环境
            
        Returns:
            格式化的设计趋势分析提示词
        """
        return DesignerPrompts.DESIGN_TREND_ANALYSIS_PROMPT.format(
            product_type=product_type,
            market_environment=market_environment
        )
    
    @staticmethod
    def get_creative_inspiration_prompt(project_background: str, creative_direction: str) -> str:
        """
        获取创意激发提示词
        
        Args:
            project_background: 项目背景
            creative_direction: 创意方向
            
        Returns:
            格式化的创意激发提示词
        """
        return DesignerPrompts.CREATIVE_INSPIRATION_PROMPT.format(
            project_background=project_background,
            creative_direction=creative_direction
        )
    
    @staticmethod
    def get_design_specification_prompt(product_series: str, brand_requirements: str) -> str:
        """
        获取设计规范制定提示词

        Args:
            product_series: 产品系列
            brand_requirements: 品牌要求

        Returns:
            格式化的设计规范制定提示词
        """
        return DesignerPrompts.DESIGN_SPECIFICATION_PROMPT.format(
            product_series=product_series,
            brand_requirements=brand_requirements
        )

    @staticmethod
    def get_ai_image_prompt_generation(design_concept: str) -> str:
        """
        获取AI图像生成提示词创作提示词

        Args:
            design_concept: 设计概念

        Returns:
            格式化的AI图像生成提示词创作提示词
        """
        return DesignerPrompts.AI_IMAGE_PROMPT_GENERATION.format(
            design_concept=design_concept
        )

    @staticmethod
    def get_design_image_analysis_prompt() -> str:
        """
        获取设计图像分析提示词

        Returns:
            设计图像分析提示词
        """
        return DesignerPrompts.DESIGN_IMAGE_ANALYSIS_PROMPT