#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
智能体提示词模块初始化文件
"""

from .craftsman_prompts import CraftsmanPrompts
from .consumer_prompts import ConsumerPrompts
from .manufacturer_prompts import ManufacturerPrompts
from .designer_prompts import DesignerPrompts

__all__ = [
    'CraftsmanPrompts',
    'ConsumerPrompts',
    'ManufacturerPrompts',
    'DesignerPrompts',
]