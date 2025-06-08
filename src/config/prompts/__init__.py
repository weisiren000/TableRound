#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
提示词模块初始化文件
统一导出所有提示词相关的类和函数
"""

# 导入基础提示词
from .base_prompts import BasePrompts

# 导入智能体提示词
from .agent_prompts.craftsman_prompts import CraftsmanPrompts
from .agent_prompts.consumer_prompts import ConsumerPrompts
from .agent_prompts.manufacturer_prompts import ManufacturerPrompts
from .agent_prompts.designer_prompts import DesignerPrompts

# 导入功能提示词
from .function_prompts.keyword_extraction_prompts import KeywordExtractionPrompts
from .function_prompts.role_switch_prompts import RoleSwitchPrompts
from .function_prompts.scenario_prompts import ScenarioPrompts
from .function_prompts.image_story_prompts import ImageStoryPrompts

# 导入提示词管理器
from .template_manager import PromptTemplateManager, PromptTemplates, prompt_manager

# 定义公开的API
__all__ = [
    # 基础类
    'BasePrompts',

    # 智能体提示词
    'CraftsmanPrompts',
    'ConsumerPrompts',
    'ManufacturerPrompts',
    'DesignerPrompts',

    # 功能提示词
    'KeywordExtractionPrompts',
    'RoleSwitchPrompts',
    'ScenarioPrompts',
    'ImageStoryPrompts',

    # 管理器
    'PromptTemplateManager',
    'PromptTemplates',  # 向后兼容
    'prompt_manager',   # 全局实例
]

# 版本信息
__version__ = '2.0.0'
__author__ = 'TableRound Team'
__description__ = 'Modular prompt management system for TableRound project'