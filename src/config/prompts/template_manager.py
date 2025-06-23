#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
提示词模板管理器
统一管理所有提示词模板，提供向后兼容的接口
"""

from typing import Dict, List, Any, Optional
import logging

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


class PromptTemplateManager:
    """提示词模板管理器"""
    
    def __init__(self):
        """初始化提示词管理器"""
        self.logger = logging.getLogger("prompt_manager")
        
        # 角色描述映射
        self._role_descriptions = {
            "craftsman": CraftsmanPrompts.get_role_description(),
            "consumer": ConsumerPrompts.get_role_description(),
            "manufacturer": ManufacturerPrompts.get_role_description(),
            "designer": DesignerPrompts.get_role_description()
        }
        
        # 角色转换提示词
        self._role_switch_prompt = """你现在需要从原来的{original_role}角色转换为{new_role}角色。

重要说明：
1. 这只是一种思维方式的转变，你仍然记得之前所有的对话内容
2. 你需要以新的视角思考问题，但保持记忆的连续性
3. 你不是在扮演预定义的其他智能体，而是采用一个全新的角色视角，但仍然保持你原有的记忆和知识库

作为{new_role}，你应该：
- 从{new_role}的视角思考问题
- 保持对之前讨论内容的记忆
- 考虑{new_role}可能关注的独特方面

请以新角色的身份简短介绍自己（100字以内），然后继续参与关于"{topic}"的讨论。
"""
        
        # 剪纸研讨会场景
        self._paper_cutting_scenario = """
场景：你们正在参加一个剪纸文创产品设计研讨会。

研讨会目标：设计出一个让消费者都满意的剪纸文创产品，以对称的剪纸风格的中国传统蝴蝶吉祥纹样为设计主题。

蝴蝶在中国传统文化中象征着美好、自由和变化，寓意着美丽与重生。对称的剪纸风格是中国传统民间艺术的重要表现形式，具有浓厚的文化底蕴和艺术价值。

在这个研讨会中，每位参与者都应该基于自己的专业背景和经验，为剪纸文创产品设计提供独特的见解和建议。最终，你们需要共同设计出一个既保留传统文化元素，又符合现代审美和使用需求的剪纸文创产品。
"""
    
    def get_system_prompt(self, role: str) -> str:
        """
        获取系统提示词
        
        Args:
            role: 角色名称
            
        Returns:
            系统提示词
        """
        role_description = self._role_descriptions.get(role, "")
        return BasePrompts.get_system_prompt(role, role_description)
    
    def get_introduction_prompt(self, role: str) -> str:
        """
        获取自我介绍提示词
        
        Args:
            role: 角色名称
            
        Returns:
            自我介绍提示词
        """
        role_description = self._role_descriptions.get(role, "")
        return BasePrompts.get_introduction_prompt(role, role_description)
    
    def get_discussion_prompt(self, role: str, topic: str) -> str:
        """
        获取讨论提示词
        
        Args:
            role: 角色名称
            topic: 讨论主题
            
        Returns:
            讨论提示词
        """
        role_description = self._role_descriptions.get(role, "")
        return BasePrompts.get_discussion_prompt(role, role_description, topic)
    
    def get_keyword_extraction_prompt(self, content: str, topic: str,
                                    extraction_type: str = "design_elements",
                                    role: str = None) -> str:
        """
        获取关键词提取提示词

        Args:
            content: 要提取关键词的内容
            topic: 主题
            extraction_type: 提取类型 (basic, domain, multilingual, hierarchical, sentiment, design_elements)
            role: 角色名称（用于设计要素提取）

        Returns:
            关键词提取提示词
        """
        if extraction_type == "design_elements" and role:
            return KeywordExtractionPrompts.get_design_elements_prompt(content, topic, role)
        elif extraction_type == "basic":
            return KeywordExtractionPrompts.get_basic_extraction_prompt(content, topic)
        elif extraction_type == "multilingual":
            return KeywordExtractionPrompts.get_multilingual_prompt(content, topic)
        elif extraction_type == "hierarchical":
            return KeywordExtractionPrompts.get_hierarchical_prompt(content, topic)
        elif extraction_type == "sentiment":
            return KeywordExtractionPrompts.get_sentiment_based_prompt(content, topic)
        else:
            # 默认使用设计要素提取（如果有角色信息）
            if role:
                return KeywordExtractionPrompts.get_design_elements_prompt(content, topic, role)
            else:
                return KeywordExtractionPrompts.get_basic_extraction_prompt(content, topic)
    
    def get_image_story_prompt(self, role: str) -> str:
        """
        获取图片故事提示词
        
        Args:
            role: 角色名称
            
        Returns:
            图片故事提示词
        """
        role_description = self._role_descriptions.get(role, "")
        return BasePrompts.get_image_story_prompt(role, role_description)
    
    def get_role_switch_prompt(self, original_role: str, new_role: str, topic: str) -> str:
        """
        获取角色转换提示词
        
        Args:
            original_role: 原始角色
            new_role: 新角色
            topic: 主题
            
        Returns:
            角色转换提示词
        """
        return self._role_switch_prompt.format(
            original_role=original_role,
            new_role=new_role,
            topic=topic
        )
    
    def get_paper_cutting_scenario(self) -> str:
        """
        获取剪纸研讨会场景描述
        
        Returns:
            剪纸研讨会场景描述
        """
        return self._paper_cutting_scenario
    
    def get_craftsman_design_evaluation_prompt(self, design: str) -> str:
        """
        获取手工艺人设计评估提示词
        
        Args:
            design: 设计方案描述
            
        Returns:
            设计评估提示词
        """
        return CraftsmanPrompts.get_design_evaluation_prompt(design)
    
    def get_craftsman_material_suggestion_prompt(self, design: str) -> str:
        """
        获取手工艺人材料建议提示词

        Args:
            design: 设计方案描述

        Returns:
            材料建议提示词
        """
        return CraftsmanPrompts.get_material_suggestion_prompt(design)

    def get_role_switch_prompt_advanced(self, original_role: str, new_role: str,
                                      topic: str, switch_type: str = "basic") -> str:
        """
        获取高级角色转换提示词

        Args:
            original_role: 原始角色
            new_role: 新角色
            topic: 主题
            switch_type: 转换类型 (basic, professional, contextual, gradual, multi_dimensional, memory)

        Returns:
            角色转换提示词
        """
        if switch_type == "basic":
            return RoleSwitchPrompts.get_basic_role_switch_prompt(original_role, new_role, topic)
        elif switch_type == "memory":
            return RoleSwitchPrompts.get_memory_preservation_prompt(original_role, new_role, topic)
        else:
            # 默认使用基础转换
            return RoleSwitchPrompts.get_basic_role_switch_prompt(original_role, new_role, topic)

    def get_scenario_prompt(self, scenario_type: str, **kwargs) -> str:
        """
        获取场景提示词

        Args:
            scenario_type: 场景类型
            **kwargs: 场景参数

        Returns:
            场景提示词
        """
        if scenario_type == "paper_cutting_workshop":
            return ScenarioPrompts.get_paper_cutting_workshop_scenario()
        elif scenario_type == "product_launch":
            return ScenarioPrompts.get_product_launch_scenario(
                kwargs.get("product_name", ""),
                kwargs.get("launch_date", ""),
                kwargs.get("target_market", ""),
                kwargs.get("budget_range", "")
            )
        elif scenario_type == "design_review":
            return ScenarioPrompts.get_design_review_scenario(
                kwargs.get("design_object", ""),
                kwargs.get("review_stage", "")
            )
        else:
            return ScenarioPrompts.get_paper_cutting_workshop_scenario()

    def get_image_story_prompt_advanced(self, role: str, story_type: str = "basic", **kwargs) -> str:
        """
        获取高级图片故事提示词

        Args:
            role: 角色名称
            story_type: 故事类型 (basic, professional, emotional, cultural, creative, educational, multi_perspective)
            **kwargs: 故事参数

        Returns:
            图片故事提示词
        """
        role_description = self._role_descriptions.get(role, "")

        if story_type == "basic":
            return ImageStoryPrompts.get_basic_image_story_prompt(role, role_description)
        elif story_type == "professional":
            return ImageStoryPrompts.get_professional_image_story_prompt(role)
        elif story_type == "emotional":
            return ImageStoryPrompts.get_emotional_image_story_prompt(
                kwargs.get("main_character", ""),
                kwargs.get("emotional_theme", ""),
                kwargs.get("background_setting", "")
            )
        elif story_type == "cultural":
            return ImageStoryPrompts.get_cultural_image_story_prompt(
                kwargs.get("cultural_theme", ""),
                kwargs.get("historical_context", "")
            )
        else:
            return ImageStoryPrompts.get_basic_image_story_prompt(role, role_description)
    
    def get_role_description(self, role: str) -> str:
        """
        获取角色描述
        
        Args:
            role: 角色名称
            
        Returns:
            角色描述
        """
        return self._role_descriptions.get(role, "")
    
    def add_role_description(self, role: str, description: str) -> None:
        """
        添加新的角色描述
        
        Args:
            role: 角色名称
            description: 角色描述
        """
        self._role_descriptions[role] = description
        self.logger.info(f"添加新角色描述: {role}")
    
    def get_available_roles(self) -> List[str]:
        """
        获取可用的角色列表
        
        Returns:
            角色名称列表
        """
        return list(self._role_descriptions.keys())


# 创建全局实例，保持向后兼容
prompt_manager = PromptTemplateManager()


# 向后兼容的PromptTemplates类
class PromptTemplates:
    """向后兼容的提示词模板类"""
    
    # 保持原有的角色描述字典，用于向后兼容
    ROLE_DESCRIPTIONS = prompt_manager._role_descriptions
    
    # 保持原有的角色转换提示词
    ROLE_SWITCH_PROMPT = prompt_manager._role_switch_prompt
    
    @staticmethod
    def get_system_prompt(role: str) -> str:
        """向后兼容的系统提示词获取方法"""
        return prompt_manager.get_system_prompt(role)
    
    @staticmethod
    def get_introduction_prompt(role: str) -> str:
        """向后兼容的自我介绍提示词获取方法"""
        return prompt_manager.get_introduction_prompt(role)
    
    @staticmethod
    def get_discussion_prompt(role: str, topic: str) -> str:
        """向后兼容的讨论提示词获取方法"""
        return prompt_manager.get_discussion_prompt(role, topic)
    
    @staticmethod
    def get_keyword_extraction_prompt(content: str, topic: str,
                                    extraction_type: str = "design_elements",
                                    role: str = None) -> str:
        """向后兼容的关键词提取提示词获取方法"""
        return prompt_manager.get_keyword_extraction_prompt(content, topic, extraction_type, role)
    
    @staticmethod
    def get_image_story_prompt(role: str) -> str:
        """向后兼容的图片故事提示词获取方法"""
        return prompt_manager.get_image_story_prompt(role)
    
    @staticmethod
    def get_role_switch_prompt(original_role: str, new_role: str, topic: str) -> str:
        """向后兼容的角色转换提示词获取方法"""
        return prompt_manager.get_role_switch_prompt(original_role, new_role, topic)
    
    @staticmethod
    def get_paper_cutting_scenario() -> str:
        """向后兼容的剪纸研讨会场景获取方法"""
        return prompt_manager.get_paper_cutting_scenario()