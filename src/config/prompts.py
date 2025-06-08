#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
提示词模板模块 - 向后兼容接口
此文件现在作为新模块化提示词系统的向后兼容接口
新的提示词管理系统位于 src/config/prompts/ 目录下
"""

import warnings
from typing import Dict, List, Any

# 导入新的模块化提示词系统
from .prompts import PromptTemplates as NewPromptTemplates

# 发出弃用警告
warnings.warn(
    "直接从 src.config.prompts 导入 PromptTemplates 已弃用。"
    "请使用 'from src.config.prompts import PromptTemplates' 或 "
    "'from src.config.prompts import prompt_manager'",
    DeprecationWarning,
    stacklevel=2
)


# 向后兼容的PromptTemplates类
class PromptTemplates:
    """向后兼容的提示词模板类"""

    # 保持原有接口，但委托给新系统
    ROLE_DESCRIPTIONS = NewPromptTemplates.ROLE_DESCRIPTIONS
    ROLE_SWITCH_PROMPT = NewPromptTemplates.ROLE_SWITCH_PROMPT

    @staticmethod
    def get_system_prompt(role: str) -> str:
        """向后兼容的系统提示词获取方法"""
        return NewPromptTemplates.get_system_prompt(role)

    @staticmethod
    def get_introduction_prompt(role: str) -> str:
        """向后兼容的自我介绍提示词获取方法"""
        return NewPromptTemplates.get_introduction_prompt(role)

    @staticmethod
    def get_discussion_prompt(role: str, topic: str) -> str:
        """向后兼容的讨论提示词获取方法"""
        return NewPromptTemplates.get_discussion_prompt(role, topic)

    @staticmethod
    def get_keyword_extraction_prompt(content: str, topic: str) -> str:
        """向后兼容的关键词提取提示词获取方法"""
        return NewPromptTemplates.get_keyword_extraction_prompt(content, topic)

    @staticmethod
    def get_image_story_prompt(role: str) -> str:
        """向后兼容的图片故事提示词获取方法"""
        return NewPromptTemplates.get_image_story_prompt(role)

    @staticmethod
    def get_role_switch_prompt(original_role: str, new_role: str, topic: str) -> str:
        """向后兼容的角色转换提示词获取方法"""
        return NewPromptTemplates.get_role_switch_prompt(original_role, new_role, topic)

    @staticmethod
    def get_paper_cutting_scenario() -> str:
        """向后兼容的剪纸研讨会场景获取方法"""
        return NewPromptTemplates.get_paper_cutting_scenario()
