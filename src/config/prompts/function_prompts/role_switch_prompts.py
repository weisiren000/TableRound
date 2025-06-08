#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
角色转换功能提示词模块
包含角色转换相关的所有提示词
"""

from typing import Dict, List


class RoleSwitchPrompts:
    """角色转换提示词类"""
    
    # 基础角色转换提示词
    BASIC_ROLE_SWITCH_PROMPT = """你现在需要从原来的{original_role}角色转换为{new_role}角色。

重要说明：
1. 这只是一种思维方式的转变，你仍然记得之前所有的对话内容
2. 你需要以新的视角思考问题，但保持记忆的连续性
3. 你不是在扮演预定义的其他智能体，而是采用一个全新的角色

作为{new_role}，你应该：
- 从{new_role}的视角思考问题
- 保持对之前讨论内容的记忆
- 考虑{new_role}可能关注的独特方面

请以新角色的身份简短介绍自己（100字以内），然后继续参与关于"{topic}"的讨论。
"""
    
    # 专业角色转换提示词
    PROFESSIONAL_ROLE_SWITCH_PROMPT = """你现在需要从{original_role}的专业视角转换为{new_role}的专业视角。

角色转换要求：
1. 保持所有之前的对话记忆和上下文
2. 采用{new_role}的专业知识体系和思维模式
3. 关注{new_role}特有的专业关注点
4. 运用{new_role}的专业术语和分析方法

{new_role}的专业特点：
{role_characteristics}

转换后的任务：
基于{new_role}的专业视角，重新审视关于"{topic}"的讨论，并提供你的专业见解。

请先简要说明你的角色转换（50字以内），然后开始专业分析。
"""
    
    # 情境化角色转换提示词
    CONTEXTUAL_ROLE_SWITCH_PROMPT = """在"{scenario}"的情境下，你需要从{original_role}转换为{new_role}。

情境背景：
{scenario_description}

角色转换指导：
1. 适应新的情境环境
2. 采用{new_role}在此情境下的行为模式
3. 保持之前讨论的记忆和连续性
4. 考虑情境对角色行为的影响

{new_role}在此情境下的特点：
- 关注重点：{focus_points}
- 行为方式：{behavior_style}
- 决策考虑：{decision_factors}

请以新角色身份参与关于"{topic}"的讨论，体现情境化的专业特色。
"""
    
    # 渐进式角色转换提示词
    GRADUAL_ROLE_SWITCH_PROMPT = """请进行渐进式角色转换，从{original_role}逐步过渡到{new_role}。

转换步骤：
1. 第一阶段：保持{original_role}身份，但开始关注{new_role}的视角
2. 第二阶段：在{original_role}基础上，融入{new_role}的思考方式
3. 第三阶段：完全转换为{new_role}，但保持对之前讨论的记忆

当前阶段：{current_stage}

阶段要求：
{stage_requirements}

请按照当前阶段的要求，参与关于"{topic}"的讨论。
"""
    
    # 多维度角色转换提示词
    MULTI_DIMENSIONAL_SWITCH_PROMPT = """请进行多维度角色转换：

原始角色：{original_role}
目标角色：{new_role}

转换维度：
1. 专业知识维度：从{original_expertise}转向{new_expertise}
2. 关注重点维度：从{original_focus}转向{new_focus}
3. 思维方式维度：从{original_thinking}转向{new_thinking}
4. 价值观维度：从{original_values}转向{new_values}

转换要求：
- 在每个维度上都要体现角色特色
- 保持记忆的完整性和连续性
- 展现角色转换的深度和广度

请以多维度转换后的新角色身份，深入分析"{topic}"。
"""
    
    # 角色记忆保持提示词
    MEMORY_PRESERVATION_PROMPT = """在角色转换过程中，请特别注意记忆保持：

转换信息：
- 原角色：{original_role}
- 新角色：{new_role}
- 讨论主题：{topic}

需要保持的记忆：
1. 之前的所有发言内容
2. 其他参与者的观点
3. 讨论的发展脉络
4. 已达成的共识
5. 存在的分歧点

记忆整合要求：
- 以新角色的视角重新理解之前的讨论
- 识别之前可能忽略的重要信息
- 发现新角色特有的关注点
- 建立新的分析框架

请展示你对之前讨论的完整记忆，并以新角色身份提供见解。
"""
    
    @staticmethod
    def get_basic_role_switch_prompt(original_role: str, new_role: str, topic: str) -> str:
        """
        获取基础角色转换提示词
        
        Args:
            original_role: 原始角色
            new_role: 新角色
            topic: 讨论主题
            
        Returns:
            格式化的基础角色转换提示词
        """
        return RoleSwitchPrompts.BASIC_ROLE_SWITCH_PROMPT.format(
            original_role=original_role,
            new_role=new_role,
            topic=topic
        )
    
    @staticmethod
    def get_professional_switch_prompt(original_role: str, new_role: str, 
                                     topic: str, role_characteristics: str) -> str:
        """
        获取专业角色转换提示词
        
        Args:
            original_role: 原始角色
            new_role: 新角色
            topic: 讨论主题
            role_characteristics: 角色特点
            
        Returns:
            格式化的专业角色转换提示词
        """
        return RoleSwitchPrompts.PROFESSIONAL_ROLE_SWITCH_PROMPT.format(
            original_role=original_role,
            new_role=new_role,
            topic=topic,
            role_characteristics=role_characteristics
        )
    
    @staticmethod
    def get_contextual_switch_prompt(original_role: str, new_role: str, topic: str,
                                   scenario: str, scenario_description: str,
                                   focus_points: str, behavior_style: str,
                                   decision_factors: str) -> str:
        """
        获取情境化角色转换提示词
        
        Args:
            original_role: 原始角色
            new_role: 新角色
            topic: 讨论主题
            scenario: 情境名称
            scenario_description: 情境描述
            focus_points: 关注重点
            behavior_style: 行为方式
            decision_factors: 决策考虑
            
        Returns:
            格式化的情境化角色转换提示词
        """
        return RoleSwitchPrompts.CONTEXTUAL_ROLE_SWITCH_PROMPT.format(
            original_role=original_role,
            new_role=new_role,
            topic=topic,
            scenario=scenario,
            scenario_description=scenario_description,
            focus_points=focus_points,
            behavior_style=behavior_style,
            decision_factors=decision_factors
        )
    
    @staticmethod
    def get_gradual_switch_prompt(original_role: str, new_role: str, topic: str,
                                current_stage: str, stage_requirements: str) -> str:
        """
        获取渐进式角色转换提示词
        
        Args:
            original_role: 原始角色
            new_role: 新角色
            topic: 讨论主题
            current_stage: 当前阶段
            stage_requirements: 阶段要求
            
        Returns:
            格式化的渐进式角色转换提示词
        """
        return RoleSwitchPrompts.GRADUAL_ROLE_SWITCH_PROMPT.format(
            original_role=original_role,
            new_role=new_role,
            topic=topic,
            current_stage=current_stage,
            stage_requirements=stage_requirements
        )
    
    @staticmethod
    def get_multi_dimensional_switch_prompt(original_role: str, new_role: str, topic: str,
                                          original_expertise: str, new_expertise: str,
                                          original_focus: str, new_focus: str,
                                          original_thinking: str, new_thinking: str,
                                          original_values: str, new_values: str) -> str:
        """
        获取多维度角色转换提示词
        
        Args:
            original_role: 原始角色
            new_role: 新角色
            topic: 讨论主题
            original_expertise: 原始专业知识
            new_expertise: 新专业知识
            original_focus: 原始关注重点
            new_focus: 新关注重点
            original_thinking: 原始思维方式
            new_thinking: 新思维方式
            original_values: 原始价值观
            new_values: 新价值观
            
        Returns:
            格式化的多维度角色转换提示词
        """
        return RoleSwitchPrompts.MULTI_DIMENSIONAL_SWITCH_PROMPT.format(
            original_role=original_role,
            new_role=new_role,
            topic=topic,
            original_expertise=original_expertise,
            new_expertise=new_expertise,
            original_focus=original_focus,
            new_focus=new_focus,
            original_thinking=original_thinking,
            new_thinking=new_thinking,
            original_values=original_values,
            new_values=new_values
        )
    
    @staticmethod
    def get_memory_preservation_prompt(original_role: str, new_role: str, topic: str) -> str:
        """
        获取角色记忆保持提示词
        
        Args:
            original_role: 原始角色
            new_role: 新角色
            topic: 讨论主题
            
        Returns:
            格式化的角色记忆保持提示词
        """
        return RoleSwitchPrompts.MEMORY_PRESERVATION_PROMPT.format(
            original_role=original_role,
            new_role=new_role,
            topic=topic
        )