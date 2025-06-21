#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
关键词提取功能提示词模块
包含关键词提取相关的所有提示词
"""

from typing import Dict, List


class KeywordExtractionPrompts:
    """关键词提取提示词类"""
    
    # 基础关键词提取提示词
    BASIC_EXTRACTION_PROMPT = """
请从以下内容中提取关键词，这些关键词应该能够概括内容的核心元素和主题。

内容：
{content}

主题：{topic}

提取关键词时，请遵循以下原则：
1. 关键词应该是名词或短语，避免使用动词、形容词或完整句子
2. 关键词应该具有代表性，能够反映内容的核心概念
3. 关键词应该相互独立，避免语义重复
4. 关键词应该简洁明了，通常为1-3个词
5. 关键词应该与主题相关，能够帮助理解和分类内容

请根据内容的丰富程度提取合适数量的关键词，通常3-10个即可。
重要：请将关键词放在<key_words>标签中，用逗号分隔。

格式示例：
<key_words>关键词1, 关键词2, 关键词3</key_words>

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
            topic=topic
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