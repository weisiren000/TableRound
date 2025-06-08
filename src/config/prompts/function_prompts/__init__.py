#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
功能提示词模块初始化文件
"""

from .keyword_extraction_prompts import KeywordExtractionPrompts
from .role_switch_prompts import RoleSwitchPrompts
from .scenario_prompts import ScenarioPrompts
from .image_story_prompts import ImageStoryPrompts

__all__ = [
    'KeywordExtractionPrompts',
    'RoleSwitchPrompts',
    'ScenarioPrompts',
    'ImageStoryPrompts',
]