#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
智能体基类模块
"""

import logging
import json
import re
import random
from typing import Dict, List, Any, Tuple, Optional, Union

from src.models.base import BaseModel
from src.core.memory import Memory
from src.core.memory_adapter import MemoryAdapter
from src.core.global_memory import GlobalMemory


class Agent:
    """智能体基类"""

    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        name: str,
        model: BaseModel,
        memory: Union[Memory, MemoryAdapter],
        global_memory: Optional[GlobalMemory] = None,
        **kwargs
    ):
        """
        初始化智能体

        Args:
            agent_id: 智能体ID
            agent_type: 智能体类型
            name: 智能体名称
            model: AI模型
            memory: 记忆模块
            **kwargs: 其他参数
        """
        self.id = agent_id
        self.type = agent_type
        self.name = name
        self.model = model
        self.memory = memory
        self.global_memory = global_memory  # 全局记忆模块
        self.logger = logging.getLogger(f"agent.{agent_type}.{agent_id}")

        # 智能体状态
        self.introduced = False
        self.current_role = agent_type
        self.original_role = agent_type
        self.keywords: List[str] = []

        # 通用角色属性
        self.age = kwargs.get("age", 30)  # 默认年龄
        self.background = kwargs.get("background", "")  # 人物介绍
        self.experience = kwargs.get("experience", "")  # 相关经历/经验

    async def _call_memory_method(self, method_name: str, *args, **kwargs):
        """
        调用记忆方法的辅助函数，处理同步和异步兼容性

        Args:
            method_name: 方法名
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            方法调用结果
        """
        method = getattr(self.memory, method_name)
        if hasattr(method, '__call__'):
            result = method(*args, **kwargs)
            # 如果是协程，则await
            if hasattr(result, '__await__'):
                return await result
            return result
        return None

    async def introduce(self) -> str:
        """
        智能体自我介绍

        Returns:
            自我介绍内容（限制300字以内）
        """
        self.logger.info(f"智能体 {self.name} 正在进行自我介绍")

        from src.config.prompts import PromptTemplates
        prompt = PromptTemplates.get_introduction_prompt(self.current_role)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)

        # 添加字数限制提示
        prompt += "\n\n请注意：自我介绍需控制在300字以内。"

        # 添加角色属性信息
        prompt += f"\n\n你的基本信息：\n年龄：{self.age}岁\n背景：{self.background}\n经验：{self.experience}"

        response = await self.model.generate(prompt, system_prompt)

        # 确保字数限制
        if len(response) > 600:  # 假设中文平均一个字符2个字节
            response = response[:600] + "..."

        # 将自我介绍存入个人记忆
        await self._call_memory_method(
            "add_memory",
            "introduction",
            {"role": self.current_role, "content": response}
        )

        # 将自我介绍记录到全局记忆
        if self.global_memory:
            await self.global_memory.record_speech(
                agent_id=self.id,
                agent_name=self.name,
                speech_type="introduction",
                content=response,
                stage="introduction",
                additional_data={"role": self.current_role}
            )

        self.introduced = True
        return response

    async def discuss(self, topic: str, context: str = "") -> str:
        """
        参与讨论

        Args:
            topic: 讨论主题
            context: 上下文信息

        Returns:
            讨论内容
        """
        self.logger.info(f"智能体 {self.name} 正在参与讨论，主题: {topic}")

        from src.config.prompts import PromptTemplates
        prompt = PromptTemplates.get_discussion_prompt(self.current_role, topic)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)

        # 添加上下文信息
        if context:
            prompt += f"\n\n讨论上下文:\n{context}"

        # 添加全局记忆上下文（会议中其他人的发言）
        if self.global_memory:
            global_context = await self.global_memory.get_current_context(
                requesting_agent_id=self.id,
                max_context=8
            )
            if global_context and "暂无" not in global_context:
                prompt += f"\n\n{global_context}"

        # 添加个人记忆信息
        memories = await self._call_memory_method("get_relevant_memories", topic)
        if memories:
            memory_text = "\n\n个人相关记忆:\n" + "\n".join(memories)
            prompt += memory_text

        response = await self.model.generate(prompt, system_prompt)

        # 将讨论内容存入个人记忆
        await self._call_memory_method(
            "add_memory",
            "discussion",
            {
                "role": self.current_role,
                "topic": topic,
                "content": response
            }
        )

        # 将讨论内容记录到全局记忆
        if self.global_memory:
            await self.global_memory.record_speech(
                agent_id=self.id,
                agent_name=self.name,
                speech_type="discussion",
                content=response,
                stage="discussion",
                additional_data={
                    "role": self.current_role,
                    "topic": topic
                }
            )

        return response

    async def extract_keywords(self, content: str, topic: str) -> List[str]:
        """
        从内容中提取关键词

        Args:
            content: 内容文本
            topic: 主题

        Returns:
            关键词列表
        """
        self.logger.info(f"智能体 {self.name} 正在提取关键词")

        from src.config.prompts import PromptTemplates
        prompt = PromptTemplates.get_keyword_extraction_prompt(content, topic)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)

        response = await self.model.generate(prompt, system_prompt)

        # 解析关键词
        try:
            # 尝试直接解析JSON
            keywords = json.loads(response)
        except:
            # 如果解析失败，尝试提取方括号内的内容
            match = re.search(r'\[(.*?)\]', response, re.DOTALL)
            if match:
                # 分割并清理关键词
                keywords_str = match.group(1)
                keywords = [k.strip().strip('"\'') for k in keywords_str.split(',')]
            else:
                # 如果仍然失败，使用简单的分行提取
                keywords = [line.strip().strip('"-,') for line in response.split('\n')
                           if line.strip() and not line.strip().startswith(('[', ']'))]

        # 确保关键词是列表类型
        if not isinstance(keywords, list):
            keywords = []

        # 如果关键词为空或数量不足，生成默认关键词
        if len(keywords) < 5:
            self.logger.warning(f"智能体 {self.name} 提取的关键词数量不足，生成默认关键词")

            # 再次尝试提取关键词，使用更明确的提示
            fallback_prompt = f"""
            请从以下内容中提取5-10个关键词：

            {content}

            关键词应该是名词或短语，能够概括内容的核心元素和主题。

            请直接列出5-10个关键词，每行一个，不要有编号或其他格式。
            这是一个重要任务，你必须提供至少5个关键词，不能少于这个数量。
            """

            fallback_response = await self.model.generate(fallback_prompt, system_prompt)

            # 简单处理：按行分割并清理
            fallback_keywords = [line.strip() for line in fallback_response.split('\n')
                               if line.strip() and not line.strip().startswith(('[', ']', '-', '*', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'))]

            # 如果仍然不足，添加一些通用关键词
            if len(fallback_keywords) < 5:
                default_keywords = ["传统文化", "剪纸艺术", "文创产品", "中国风", "吉祥图案",
                                   "蝙蝠纹样", "对称设计", "红色喜庆", "民间工艺", "文化传承"]

                # 根据角色添加一些特定关键词
                if self.current_role == "craftsman":
                    default_keywords.extend(["手工技艺", "传统工艺", "匠心精神", "技艺传承", "精细制作"])
                elif self.current_role == "consumer":
                    default_keywords.extend(["用户体验", "消费喜好", "实用性", "审美需求", "购买意愿"])
                elif self.current_role == "manufacturer":
                    default_keywords.extend(["批量生产", "成本控制", "材料选择", "工艺流程", "市场需求"])
                elif self.current_role == "designer":
                    default_keywords.extend(["创新设计", "美学原则", "视觉效果", "设计理念", "艺术表达"])

                # 随机选择一些默认关键词补充
                needed = 5 - len(fallback_keywords)
                fallback_keywords.extend(random.sample(default_keywords, min(needed, len(default_keywords))))

            # 合并关键词
            keywords.extend(fallback_keywords)

        # 去重
        keywords = list(dict.fromkeys(keywords))

        # 限制关键词数量
        keywords = keywords[:10]

        # 将关键词存入个人记忆
        await self._call_memory_method(
            "add_memory",
            "keywords",
            {
                "role": self.current_role,
                "topic": topic,
                "keywords": keywords
            }
        )

        # 将关键词记录到全局记忆
        if self.global_memory:
            await self.global_memory.record_speech(
                agent_id=self.id,
                agent_name=self.name,
                speech_type="keywords",
                content=", ".join(keywords),
                stage="keywords",
                additional_data={
                    "role": self.current_role,
                    "topic": topic,
                    "keywords": keywords
                }
            )

        self.keywords = keywords
        return keywords

    async def tell_story_from_image(self, image_path: str) -> Tuple[str, List[str]]:
        """
        根据图片讲故事并提取关键词

        Args:
            image_path: 图片路径

        Returns:
            故事内容和关键词列表
        """
        self.logger.info(f"智能体 {self.name} 正在根据图片讲故事")

        # 检查模型是否支持图像
        if not self.model.supports_vision():
            return "该模型不支持图像处理", []

        from src.config.prompts import PromptTemplates
        prompt = PromptTemplates.get_image_story_prompt(self.current_role)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)

        # 添加角色属性信息
        prompt += f"\n\n你的基本信息：\n年龄：{self.age}岁\n背景：{self.background}\n经验：{self.experience}"

        # 生成故事
        story = await self.model.generate_with_image(prompt, system_prompt, image_path)

        # 提取关键词
        keywords_prompt = f"""
        基于你刚才讲述的故事：

        {story}

        请提取5-10个关键词，这些关键词应该能够概括故事的核心元素和主题。

        提取关键词时，请遵循以下原则：
        1. 关键词应该是名词或短语，避免使用动词、形容词或完整句子
        2. 关键词应该具有代表性，能够反映故事的核心概念
        3. 关键词应该相互独立，避免语义重复
        4. 关键词应该简洁明了，通常为1-3个词
        5. 关键词应该与故事主题相关，能够帮助理解和分类内容

        请确保提取的关键词数量在5-10个之间，不多不少。

        请以JSON格式返回关键词列表，格式如下：
        ["关键词1", "关键词2", "关键词3", ...]
        """

        keywords_response = await self.model.generate(keywords_prompt, system_prompt)

        # 解析关键词
        try:
            # 尝试直接解析JSON
            keywords = json.loads(keywords_response)
        except:
            # 如果解析失败，尝试提取方括号内的内容
            match = re.search(r'\[(.*?)\]', keywords_response, re.DOTALL)
            if match:
                # 分割并清理关键词
                keywords_str = match.group(1)
                keywords = [k.strip().strip('"\'') for k in keywords_str.split(',')]
            else:
                # 如果仍然失败，使用简单的分行提取
                keywords = [line.strip().strip('"-,') for line in keywords_response.split('\n')
                           if line.strip() and not line.strip().startswith(('[', ']'))]

        # 确保关键词是列表类型
        if not isinstance(keywords, list):
            keywords = []

        # 限制关键词数量
        keywords = keywords[:10]

        # 将故事和关键词存入记忆
        await self._call_memory_method(
            "add_memory",
            "image_story",
            {
                "role": self.current_role,
                "story": story,
                "keywords": keywords,
                "image_path": image_path
            }
        )

        self.keywords = keywords
        return story, keywords

    async def switch_role(self, new_role: str, topic: str) -> str:
        """
        转换角色

        Args:
            new_role: 新角色
            topic: 讨论主题

        Returns:
            角色转换后的自我介绍
        """
        self.logger.info(f"智能体 {self.name} 正在从 {self.current_role} 转换为 {new_role}")

        # 保存原始角色
        original_role = self.current_role

        # 更新当前角色
        self.current_role = new_role

        from src.config.prompts import PromptTemplates
        # 获取角色描述
        new_role_description = PromptTemplates.ROLE_DESCRIPTIONS.get(new_role, "")

        # 获取角色转换提示词
        prompt = PromptTemplates.get_role_switch_prompt(
            original_role=original_role,
            new_role=new_role,
            topic=topic
        )

        # 添加角色描述
        prompt += f"\n\n新角色描述：\n{new_role_description}"

        # 获取系统提示词
        system_prompt = f"""你现在需要假设自己是{new_role}，但你仍然是原来的{original_role}。
这不是角色的完全转变，而是一种视角的转换。你需要从{new_role}的视角去思考问题，但保持你作为{original_role}的所有记忆和知识。
请记住：
1. 你仍然是原来的{original_role}，只是暂时从{new_role}的视角思考
2. 你保留所有之前对话的记忆和你的原始身份
3. 你不是在扮演一个全新的角色，而是以{new_role}的视角审视问题
4. 你的回答应该体现出你作为{original_role}对{new_role}视角的理解和模拟

请简短介绍一下你作为{original_role}如何理解{new_role}的视角（100字以内），然后从这个新视角继续参与关于"{topic}"的讨论。"""

        # 获取对话历史记忆
        discussion_memories = await self._call_memory_method("get_conversation_history")
        if discussion_memories:
            prompt += f"\n\n对话历史：\n{discussion_memories}"

        # 获取关键词记忆
        keyword_memories = await self._call_memory_method("get_memories_by_type", "keywords")
        if keyword_memories:
            keywords_text = "\n".join(keyword_memories)
            prompt += f"\n\n关键词记忆：\n{keywords_text}"

        # 获取角色转换记忆
        role_switch_memories = await self._call_memory_method("get_memories_by_type", "role_switch")
        if role_switch_memories:
            role_switch_text = "\n".join(role_switch_memories)
            prompt += f"\n\n角色转换记忆：\n{role_switch_text}"

        # 生成角色转换后的自我介绍
        response = await self.model.generate(prompt, system_prompt)

        # 将角色转换记录存入记忆
        await self._call_memory_method(
            "add_memory",
            "role_switch",
            {
                "previous_role": original_role,
                "new_role": new_role,
                "topic": topic,
                "introduction": response
            }
        )

        return response

    async def generate_design_card(self, keywords: List[str]) -> str:
        """
        生成设计卡牌

        Args:
            keywords: 关键词列表

        Returns:
            设计卡牌内容
        """
        self.logger.info(f"智能体 {self.name} 正在生成设计卡牌")

        from src.config.prompts import PromptTemplates
        # 获取剪纸研讨会场景描述
        scenario = PromptTemplates.get_paper_cutting_scenario()

        # 准备提示词
        prompt = f"""
        {scenario}

        基于以下关键词：
        {', '.join(keywords)}

        请你作为一名{self.current_role}，为对称的剪纸风格的中国传统蝙蝠吉祥纹样文创产品设计提供你的想法和建议。

        请包含以下内容：
        1. 产品形式（如：贴纸、书签、灯饰、壁挂等）
        2. 设计元素（如：色彩、图案、材质等）
        3. 功能特点（如：实用性、装饰性、收藏价值等）
        4. 目标用户（如：年龄段、兴趣爱好、消费习惯等）
        5. 文化内涵（如：传统象征意义、现代诠释等）

        请以设计卡牌的形式呈现你的想法，内容应该简洁明了，突出重点。
        """

        system_prompt = PromptTemplates.get_system_prompt(self.current_role)

        # 生成设计卡牌
        design_card = await self.model.generate(prompt, system_prompt)

        # 将设计卡牌存入记忆
        await self._call_memory_method(
            "add_memory",
            "design_card",
            {
                "role": self.current_role,
                "keywords": keywords,
                "content": design_card
            }
        )

        return design_card
