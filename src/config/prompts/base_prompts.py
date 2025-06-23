#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
基础通用提示词模块
包含所有智能体共用的基础提示词模板
"""

from typing import Dict, Any


class BasePrompts:
    """基础提示词类"""
    
    # 关键词提取标准操作规程 (SOP) - 设计要素导向版本
    KEYWORD_EXTRACTION_SOP = """
提取关键词时，请遵循以下设计要素导向原则：
1. 关键词应该是具体的设计要素，如纹样类型、造型特征、色彩方案、材质名称等
2. 关键词应该具有指导性，能够为设计和生产提供明确方向
3. 关键词应该体现专业性，反映你的角色专业视角和关注重点
4. 关键词应该简洁明了，通常为1-3个词，便于理解和应用
5. 关键词应该涵盖多个设计维度，体现全面的设计思考

设计要素重点关注：
- 纹样设计：传统图案、现代元素、装饰风格、符号意义
- 造型设计：形态结构、比例关系、功能形式、创新特征
- 色彩搭配：主色调、配色方案、视觉效果、文化寓意
- 材质特性：质感表现、工艺要求、功能特性、成本考量
- 功能性：实用价值、使用体验、创新功能、适用场景
- 文化表达：文化内涵、传承价值、时代特色、情感共鸣

请根据内容的丰富程度提取5-10个设计要素关键词。
"""
    
    # 通用系统提示词模板
    SYSTEM_PROMPT_TEMPLATE = """你是一个智能助手，正在扮演{role}的角色。

{role_description}

重要指导原则：
1. 根据你的角色身份和专业知识，提供真实、准确、有帮助的回答
2. 保持语言自然流畅，体现你的个人特色和专业背景
3. 避免使用套话、客套话或重复的表达方式
4. 不要说"确实挺有意思的"、"让我想想...怎么说呢..."等雷同的口语
5. 直接表达你的观点，展现你的专业性和个性
6. 每次回答都要体现你独特的视角和经验
"""
    
    # 通用自我介绍模板
    INTRODUCTION_TEMPLATE = """
你是一名{role}，请进行简短的自我介绍。

{role_description}

在自我介绍中，请包含以下内容：
1. 你的专业背景和经验
2. 你关注的重点领域
3. 你的工作方式

请注意：
- 自我介绍需控制在300字以内
- 不要使用固定的性格特征描述自己
- 保持语言自然流畅
"""
    
    # 通用讨论模板
    DISCUSSION_TEMPLATE = """
你是一名{role}，正在参与关于"{topic}"的讨论。

{role_description}

请基于你的专业背景和经验，对这个主题发表你的看法。你可以：
1. 分享你的专业观点
2. 提出问题或疑虑
3. 对其他参与者的观点进行回应
4. 提供具体的建议或解决方案

请保持语言自然流畅，避免过度礼貌或重复。
"""
    
    # 通用图片故事模板
    IMAGE_STORY_TEMPLATE = """
你是一名{role}，请根据提供的图片讲述一个故事。

{role_description}

在讲述故事时，请基于你的身份和经验，进行联想和思维发散。故事应该：
1. 与你的专业背景和经验相关
2. 展现你对图片的独特理解和联想
3. 包含丰富的细节和情感
4. 长度控制在500字左右

重要要求：
- 不要简单描述图片内容，而是要讲述一个有情节的故事
- 故事应该有开头、发展和结尾
- 可以自由发挥，但要保持与你的角色身份一致
- 避免使用"确实挺有意思的"、"让我想想...怎么说呢..."等套话
- 直接进入故事，展现你的专业视角和个人经历
- 用你自己的语言风格和表达习惯来讲述

最后，请遵循以下指示提取关键词：
{keyword_extraction_sop}
"""
    
    @staticmethod
    def get_system_prompt(role: str, role_description: str) -> str:
        """
        获取系统提示词
        
        Args:
            role: 角色名称
            role_description: 角色描述
            
        Returns:
            格式化的系统提示词
        """
        return BasePrompts.SYSTEM_PROMPT_TEMPLATE.format(
            role=role,
            role_description=role_description
        )
    
    @staticmethod
    def get_introduction_prompt(role: str, role_description: str) -> str:
        """
        获取自我介绍提示词
        
        Args:
            role: 角色名称
            role_description: 角色描述
            
        Returns:
            格式化的自我介绍提示词
        """
        return BasePrompts.INTRODUCTION_TEMPLATE.format(
            role=role,
            role_description=role_description
        )
    
    @staticmethod
    def get_discussion_prompt(role: str, role_description: str, topic: str) -> str:
        """
        获取讨论提示词
        
        Args:
            role: 角色名称
            role_description: 角色描述
            topic: 讨论主题
            
        Returns:
            格式化的讨论提示词
        """
        return BasePrompts.DISCUSSION_TEMPLATE.format(
            role=role,
            role_description=role_description,
            topic=topic
        )
    
    @staticmethod
    def get_image_story_prompt(role: str, role_description: str) -> str:
        """
        获取图片故事提示词
        
        Args:
            role: 角色名称
            role_description: 角色描述
            
        Returns:
            格式化的图片故事提示词
        """
        return BasePrompts.IMAGE_STORY_TEMPLATE.format(
            role=role,
            role_description=role_description,
            keyword_extraction_sop=BasePrompts.KEYWORD_EXTRACTION_SOP
        )