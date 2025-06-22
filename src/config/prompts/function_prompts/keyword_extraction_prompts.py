#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
关键词提取功能提示词模块
包含关键词提取相关的所有提示词
"""

from typing import Dict, List
from src.config.prompts.base_prompts import BasePrompts


class KeywordExtractionPrompts:
    """关键词提取提示词类"""
    
    # 基础关键词提取提示词
    BASIC_EXTRACTION_PROMPT = """
请从以下内容中提取关键词，这些关键词应该能够概括内容的核心元素和主题。

内容：
{content}

主题：{topic}

{keyword_extraction_sop}

备选格式（如果无法使用标签）：
["关键词1", "关键词2", "关键词3"]
"""
    
    # 专业领域关键词提取
    DOMAIN_SPECIFIC_EXTRACTION_PROMPT = """
作为{role}，请从以下{domain}领域的内容中提取专业关键词：

内容：
{content}

主题：{topic}

请基于你的专业知识，提取5-10个最能代表该领域核心概念的关键词。

专业要求：
1. 关键词应体现{domain}领域的专业特色
2. 优先选择行业术语和专业概念
3. 考虑该领域的发展趋势和热点
4. 关键词应有助于专业人士理解和分类
5. 避免过于通用的词汇，突出专业性

请以JSON格式返回关键词列表：
["专业关键词1", "专业关键词2", "专业关键词3", ...]
"""
    
    # 多语言关键词提取
    MULTILINGUAL_EXTRACTION_PROMPT = """
请从以下多语言内容中提取关键词，支持中英文混合处理：

内容：
{content}

主题：{topic}

提取要求：
1. 识别中文和英文关键词
2. 保持原语言形式，不进行翻译
3. 中英文关键词可以混合存在
4. 优先选择更准确表达概念的语言版本
5. 确保关键词的语义完整性

格式要求：
- 中文关键词：保持中文形式
- 英文关键词：保持英文形式
- 混合词汇：保持原有形式

请以JSON格式返回关键词列表：
["关键词1", "keyword2", "混合关键词3", ...]
"""
    
    # 层次化关键词提取
    HIERARCHICAL_EXTRACTION_PROMPT = """
请从以下内容中提取层次化关键词，分为核心关键词和扩展关键词：

内容：
{content}

主题：{topic}

分层要求：
1. 核心关键词（3-5个）：最重要的概念，必须包含
2. 扩展关键词（3-5个）：补充性概念，丰富理解

核心关键词标准：
- 直接关联主题
- 高频出现或重要性突出
- 删除后会显著影响内容理解

扩展关键词标准：
- 提供额外上下文
- 有助于深入理解
- 体现内容的细节特征

请以JSON格式返回分层关键词：
{{
    "core_keywords": ["核心关键词1", "核心关键词2", ...],
    "extended_keywords": ["扩展关键词1", "扩展关键词2", ...]
}}
"""
    
    # 情感导向关键词提取
    SENTIMENT_BASED_EXTRACTION_PROMPT = """
请从以下内容中提取带有情感倾向的关键词：

内容：
{content}

主题：{topic}

情感分析要求：
1. 识别正面、负面、中性的关键词
2. 考虑词汇的情感色彩和语境
3. 提取能够反映内容情感态度的词汇
4. 平衡不同情感倾向的关键词

请以JSON格式返回情感分类的关键词：
{{
    "positive": ["正面关键词1", "正面关键词2", ...],
    "negative": ["负面关键词1", "负面关键词2", ...],
    "neutral": ["中性关键词1", "中性关键词2", ...]
}}
"""

    # 设计要素导向关键词提取
    DESIGN_ELEMENTS_EXTRACTION_PROMPT = """
作为{role}，请分析以下内容并提取关键词：

内容：
{content}

主题：{topic}

提取策略：
1. **首先判断内容性质**：
   - 如果内容与设计、产品、工艺、文创等相关，则从设计要素角度提取关键词
   - 如果内容是日常生活、一般性问题，则从内容本身的核心概念提取关键词

2. **设计相关内容的提取维度**（仅当内容与设计相关时使用）：
   🎨 纹样设计：传统图案、装饰元素、符号意义
   🏗️ 造型设计：形态结构、比例关系、功能形式
   🌈 色彩搭配：主色调、配色方案、视觉效果
   🧱 材质特性：质感表现、工艺要求、物理特性
   💡 功能性：实用价值、使用体验、创新功能
   🎯 文化表达：文化内涵、传承价值、情感共鸣

3. **一般内容的提取原则**：
   - 提取内容的核心概念和关键信息
   - 体现你作为{role}的专业视角和关注点
   - 选择对讨论和分析有价值的关键词

提取要求：
- 提取5-10个最具代表性的关键词
- 关键词应准确反映内容的核心要素
- 体现你的角色专业特色和关注重点
- 确保关键词对后续讨论有指导意义

请以JSON格式返回关键词列表：
["关键词1", "关键词2", "关键词3", ...]

注意：请根据内容的实际情况选择合适的提取策略，不要强制使用设计要素框架。
"""
    
    @staticmethod
    def get_basic_extraction_prompt(content: str, topic: str) -> str:
        """
        获取基础关键词提取提示词
        
        Args:
            content: 要提取关键词的内容
            topic: 主题
            
        Returns:
            格式化的关键词提取提示词
        """
        return KeywordExtractionPrompts.BASIC_EXTRACTION_PROMPT.format(
            content=content,
            topic=topic,
            keyword_extraction_sop=BasePrompts.KEYWORD_EXTRACTION_SOP
        )
    
    @staticmethod
    def get_domain_specific_prompt(content: str, topic: str, role: str, domain: str) -> str:
        """
        获取专业领域关键词提取提示词
        
        Args:
            content: 要提取关键词的内容
            topic: 主题
            role: 角色
            domain: 专业领域
            
        Returns:
            格式化的专业关键词提取提示词
        """
        return KeywordExtractionPrompts.DOMAIN_SPECIFIC_EXTRACTION_PROMPT.format(
            content=content,
            topic=topic,
            role=role,
            domain=domain
        )
    
    @staticmethod
    def get_multilingual_prompt(content: str, topic: str) -> str:
        """
        获取多语言关键词提取提示词
        
        Args:
            content: 要提取关键词的内容
            topic: 主题
            
        Returns:
            格式化的多语言关键词提取提示词
        """
        return KeywordExtractionPrompts.MULTILINGUAL_EXTRACTION_PROMPT.format(
            content=content,
            topic=topic
        )
    
    @staticmethod
    def get_hierarchical_prompt(content: str, topic: str) -> str:
        """
        获取层次化关键词提取提示词
        
        Args:
            content: 要提取关键词的内容
            topic: 主题
            
        Returns:
            格式化的层次化关键词提取提示词
        """
        return KeywordExtractionPrompts.HIERARCHICAL_EXTRACTION_PROMPT.format(
            content=content,
            topic=topic
        )
    
    @staticmethod
    def get_sentiment_based_prompt(content: str, topic: str) -> str:
        """
        获取情感导向关键词提取提示词

        Args:
            content: 要提取关键词的内容
            topic: 主题

        Returns:
            格式化的情感导向关键词提取提示词
        """
        return KeywordExtractionPrompts.SENTIMENT_BASED_EXTRACTION_PROMPT.format(
            content=content,
            topic=topic
        )

    @staticmethod
    def get_design_elements_prompt(content: str, topic: str, role: str) -> str:
        """
        获取设计要素导向关键词提取提示词

        Args:
            content: 要提取关键词的内容
            topic: 主题
            role: 角色名称

        Returns:
            格式化的设计要素导向关键词提取提示词
        """
        return KeywordExtractionPrompts.DESIGN_ELEMENTS_EXTRACTION_PROMPT.format(
            content=content,
            topic=topic,
            role=role
        )