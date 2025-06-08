#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图片故事功能提示词模块
包含图片故事生成相关的所有提示词
"""

from typing import Dict, List


class ImageStoryPrompts:
    """图片故事提示词类"""
    
    # 基础图片故事提示词
    BASIC_IMAGE_STORY_PROMPT = """
你是一名{role}，请根据提供的图片讲述一个故事。

{role_description}

在讲述故事时，请基于你的身份和经验，进行联想和思维发散。故事应该：
1. 与你的专业背景和经验相关
2. 展现你对图片的独特理解和联想
3. 包含丰富的细节和情感
4. 长度控制在500字左右

请注意：
- 不要简单描述图片内容，而是要讲述一个有情节的故事
- 故事应该有开头、发展和结尾
- 可以自由发挥，但要保持与你的角色身份一致
"""
    
    # 专业视角图片故事提示词
    PROFESSIONAL_IMAGE_STORY_PROMPT = """
作为{role}，请从专业角度分析这张图片并讲述相关故事。

专业分析要求：
1. 运用{role}的专业知识和经验
2. 识别图片中的专业元素
3. 分析图片的专业价值和意义
4. 结合行业背景和发展趋势

故事创作要求：
1. 以专业分析为基础
2. 融入个人经验和见解
3. 体现专业特色和深度
4. 具有教育和启发意义

请创作一个既有专业深度又有故事性的内容。
"""
    
    # 情感导向图片故事提示词
    EMOTIONAL_IMAGE_STORY_PROMPT = """
请基于这张图片创作一个情感丰富的故事。

情感创作指导：
1. 观察图片中的情感元素
2. 挖掘潜在的情感冲突
3. 构建情感发展脉络
4. 表达深层的情感主题

故事要素：
- 主角：{main_character}
- 情感主线：{emotional_theme}
- 背景设定：{background_setting}

创作要求：
1. 情感真实可信
2. 情节引人入胜
3. 语言生动感人
4. 主题积极向上

请创作一个能够触动人心的故事。
"""
    
    # 文化解读图片故事提示词
    CULTURAL_IMAGE_STORY_PROMPT = """
请从文化角度解读这张图片并创作相关故事。

文化解读要点：
1. 识别图片中的文化元素
2. 分析文化符号和象征意义
3. 探讨文化背景和历史渊源
4. 思考文化传承和发展

故事创作方向：
1. 以文化元素为核心
2. 融入历史背景和传说
3. 体现文化价值和精神
4. 展现文化的传承和创新

文化主题：{cultural_theme}
历史背景：{historical_context}

请创作一个富有文化内涵的故事。
"""
    
    # 创意想象图片故事提示词
    CREATIVE_IMAGE_STORY_PROMPT = """
请发挥创意想象，基于这张图片创作一个独特的故事。

创意要求：
1. 打破常规思维
2. 运用丰富想象力
3. 创造独特的世界观
4. 设计新颖的情节

创意元素：
- 奇幻元素：{fantasy_elements}
- 科幻元素：{sci_fi_elements}
- 魔法元素：{magic_elements}

故事风格：{story_style}

创作指导：
1. 不受现实限制
2. 大胆创新和想象
3. 构建完整的故事世界
4. 保持逻辑一致性

请创作一个充满创意和想象力的故事。
"""
    
    # 教育启发图片故事提示词
    EDUCATIONAL_IMAGE_STORY_PROMPT = """
请基于这张图片创作一个具有教育意义的故事。

教育目标：{educational_goals}
目标受众：{target_audience}

教育要素：
1. 知识传授：{knowledge_points}
2. 技能培养：{skill_development}
3. 价值观引导：{value_guidance}
4. 行为示范：{behavior_modeling}

故事创作要求：
1. 寓教于乐
2. 深入浅出
3. 生动有趣
4. 启发思考

请创作一个既有趣又有教育价值的故事。
"""
    
    # 多角度图片故事提示词
    MULTI_PERSPECTIVE_IMAGE_STORY_PROMPT = """
请从多个角度观察这张图片，创作多层次的故事。

观察角度：
1. 表面层次：直观可见的内容
2. 深层含义：隐藏的信息和暗示
3. 象征意义：抽象的概念和理念
4. 情感层面：触发的情感和感受

故事结构：
- 第一层：{first_layer}
- 第二层：{second_layer}
- 第三层：{third_layer}

创作要求：
1. 层次分明
2. 逻辑清晰
3. 内容丰富
4. 主题深刻

请创作一个多层次、多角度的复合故事。
"""
    
    @staticmethod
    def get_basic_image_story_prompt(role: str, role_description: str) -> str:
        """
        获取基础图片故事提示词
        
        Args:
            role: 角色名称
            role_description: 角色描述
            
        Returns:
            格式化的基础图片故事提示词
        """
        return ImageStoryPrompts.BASIC_IMAGE_STORY_PROMPT.format(
            role=role,
            role_description=role_description
        )
    
    @staticmethod
    def get_professional_image_story_prompt(role: str) -> str:
        """
        获取专业视角图片故事提示词
        
        Args:
            role: 角色名称
            
        Returns:
            格式化的专业视角图片故事提示词
        """
        return ImageStoryPrompts.PROFESSIONAL_IMAGE_STORY_PROMPT.format(role=role)
    
    @staticmethod
    def get_emotional_image_story_prompt(main_character: str, emotional_theme: str,
                                       background_setting: str) -> str:
        """
        获取情感导向图片故事提示词
        
        Args:
            main_character: 主角
            emotional_theme: 情感主题
            background_setting: 背景设定
            
        Returns:
            格式化的情感导向图片故事提示词
        """
        return ImageStoryPrompts.EMOTIONAL_IMAGE_STORY_PROMPT.format(
            main_character=main_character,
            emotional_theme=emotional_theme,
            background_setting=background_setting
        )
    
    @staticmethod
    def get_cultural_image_story_prompt(cultural_theme: str, historical_context: str) -> str:
        """
        获取文化解读图片故事提示词
        
        Args:
            cultural_theme: 文化主题
            historical_context: 历史背景
            
        Returns:
            格式化的文化解读图片故事提示词
        """
        return ImageStoryPrompts.CULTURAL_IMAGE_STORY_PROMPT.format(
            cultural_theme=cultural_theme,
            historical_context=historical_context
        )
    
    @staticmethod
    def get_creative_image_story_prompt(fantasy_elements: str, sci_fi_elements: str,
                                      magic_elements: str, story_style: str) -> str:
        """
        获取创意想象图片故事提示词
        
        Args:
            fantasy_elements: 奇幻元素
            sci_fi_elements: 科幻元素
            magic_elements: 魔法元素
            story_style: 故事风格
            
        Returns:
            格式化的创意想象图片故事提示词
        """
        return ImageStoryPrompts.CREATIVE_IMAGE_STORY_PROMPT.format(
            fantasy_elements=fantasy_elements,
            sci_fi_elements=sci_fi_elements,
            magic_elements=magic_elements,
            story_style=story_style
        )
    
    @staticmethod
    def get_educational_image_story_prompt(educational_goals: str, target_audience: str,
                                         knowledge_points: str, skill_development: str,
                                         value_guidance: str, behavior_modeling: str) -> str:
        """
        获取教育启发图片故事提示词
        
        Args:
            educational_goals: 教育目标
            target_audience: 目标受众
            knowledge_points: 知识点
            skill_development: 技能培养
            value_guidance: 价值观引导
            behavior_modeling: 行为示范
            
        Returns:
            格式化的教育启发图片故事提示词
        """
        return ImageStoryPrompts.EDUCATIONAL_IMAGE_STORY_PROMPT.format(
            educational_goals=educational_goals,
            target_audience=target_audience,
            knowledge_points=knowledge_points,
            skill_development=skill_development,
            value_guidance=value_guidance,
            behavior_modeling=behavior_modeling
        )
    
    @staticmethod
    def get_multi_perspective_image_story_prompt(first_layer: str, second_layer: str,
                                               third_layer: str) -> str:
        """
        获取多角度图片故事提示词
        
        Args:
            first_layer: 第一层内容
            second_layer: 第二层内容
            third_layer: 第三层内容
            
        Returns:
            格式化的多角度图片故事提示词
        """
        return ImageStoryPrompts.MULTI_PERSPECTIVE_IMAGE_STORY_PROMPT.format(
            first_layer=first_layer,
            second_layer=second_layer,
            third_layer=third_layer
        )