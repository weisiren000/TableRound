#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
基础通用提示词模块
包含所有智能体共用的基础提示词模板
"""

from typing import Dict, Any


class BasePrompts:
    """基础提示词类"""
    
    # 通用系统提示词模板
    SYSTEM_PROMPT_TEMPLATE = """你是一个智能助手，正在扮演{role}的角色。

{role_description}

请根据你的角色身份和专业知识，提供真实、准确、有帮助的回答。
保持语言自然流畅，避免过度礼貌或重复。
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

请注意：
- 不要简单描述图片内容，而是要讲述一个有情节的故事
- 故事应该有开头、发展和结尾
- 可以自由发挥，但要保持与你的角色身份一致
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
            role_description=role_description
        )