#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
智能体基类模块
"""

import logging
import json
import re
from typing import Dict, List, Any, Tuple, Optional, Union

from src.models.base import BaseModel
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
        memory: MemoryAdapter,
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

        from src.config.prompts.template_manager import PromptTemplates
        base_prompt = PromptTemplates.get_introduction_prompt(self.current_role)
        base_system_prompt = PromptTemplates.get_system_prompt(self.current_role)

        # 构建拟人化的自我介绍prompt
        humanized_intro_prompt = f"""
你是{self.name}，{self.background}
年龄：{self.age}岁
经验：{self.experience}
当前角色：{self.current_role}

你需要进行一个自然、亲切的自我介绍，就像在真实的会议中与大家初次见面一样。

请遵循以下原则：
1. **自然开场**：用轻松、友好的语气开始，如"大家好！""很高兴见到大家"
2. **个人化表达**：分享一些个人经历和感受，让介绍更有温度
3. **口语化风格**：使用自然的口语表达，避免过于正式或机械化
4. **情感色彩**：表达你对工作的热情、对传统文化的感情等
5. **互动意识**：表现出对与大家交流的期待

在介绍中可以包含：
- 思考停顿："嗯...怎么说呢...""让我想想..."
- 情感表达："我特别喜欢...""让我印象深刻的是..."
- 生活化细节：具体的工作场景、难忘的经历等
- 谦逊表达："虽然我...""可能我的经验还不够..."

{base_prompt}

重要提示：
1. 请以第一人称进行自我介绍，体现你的个性和特色
2. 展现你的情感、态度和个人魅力
3. 使用自然的口语化表达，让人感到亲切
4. 字数控制在250-300字之间
5. 让介绍既专业又有人情味
"""

        # 增强系统prompt
        enhanced_system_prompt = f"""{base_system_prompt}

你现在需要进行一个自然、真实的自我介绍，就像在现实生活中与新朋友见面一样。请：
1. 保持角色的专业性，但要展现人性化的一面
2. 使用自然的口语化表达，避免机械化的自我介绍
3. 展现真实的情感和个性特征
4. 让听众感到你是一个有血有肉的真实人物
5. 表达出对即将开始的讨论的期待和兴趣
"""

        response = await self.model.generate(humanized_intro_prompt, enhanced_system_prompt)

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

    def _build_humanized_discussion_prompt(
        self,
        topic: str,
        context: str = "",
        global_context: Optional[str] = None,
        memories: Optional[List[str]] = None
    ) -> Tuple[str, str]:
        """
        构建拟人化的讨论prompt

        Args:
            topic: 讨论主题
            context: 讨论上下文
            global_context: 全局记忆上下文
            memories: 个人记忆列表

        Returns:
            (prompt, system_prompt) 元组
        """
        from src.config.prompts.template_manager import PromptTemplates

        # 获取基础prompt和系统prompt
        base_prompt = PromptTemplates.get_discussion_prompt(self.current_role, topic)
        base_system_prompt = PromptTemplates.get_system_prompt(self.current_role)

        # 构建个人背景信息
        background_info = f"""
你是{self.name}，{self.background}
年龄：{self.age}岁
经验：{self.experience}
当前角色：{self.current_role}
"""

        # 构建记忆部分
        memory_section = ""
        if memories:
            memory_section = f"""
你的个人记忆和经验：
{chr(10).join(memories)}
"""

        # 构建全局上下文部分（其他人的发言）
        context_section = ""
        if global_context and "暂无" not in global_context:
            context_section = f"""
会议中其他人的发言：
{global_context}
"""

        # 获取角色特有的说话风格
        role_style = self._get_agent_speaking_style()

        # 构建拟人化对话指导
        humanized_guidelines = f"""
你需要扮演一个能自然聊天的对话伙伴，对话需满足以下原则：

1. **记忆连贯性**：记住当前话题及历史对话内容，对之前提到的信息进行关联回应。

2. **自然对话逻辑**：避免机械问答，用"接话-延展-反问"的节奏互动：
   - 先针对别人说的话进行回应（避免使用"我觉得这个话题真的很有意思"这样的套话）
   - 然后结合自己的经验延展
   - 最后可以抛出问题或建议

3. **话题质感塑造**：加入口语化思考过程和情绪反馈，但要符合你的角色特点。

4. **个性化表达**：每个人都有不同的说话方式，避免使用相同的开场白和表达方式。

{role_style}

5. **信息缺口补充**：当话题信息不足时，主动追问细节，推动对话深入。

重要：避免使用以下同质化表达：
- "我觉得这个话题真的很有意思！"
- "嗯，我觉得..."（每个人都这样开头）
- 完全相同的思考停顿词
- 千篇一律的回应模式
"""

        # 构建完整的prompt
        full_prompt = f"""{background_info}

当前讨论主题：{topic}

{memory_section}

{context_section}

{humanized_guidelines}

{base_prompt}

重要提示：
1. 请以第一人称回答，体现你的个人经历和专业背景
2. 如果有其他人的发言，请先针对他们的话进行回应，然后再发表自己的观点
3. 展现你的情感、态度和个人观点，使用自然的口语化表达
4. 使用你熟悉的专业术语和表达方式，但要自然融入对话
5. 加入思考过程、情绪反馈和场景化联想
6. 字数控制在150-300字之间，保持对话的自然流畅"""

        # 增强系统prompt
        enhanced_system_prompt = f"""{base_system_prompt}

你现在需要进行自然的人类对话，请遵循以下原则：
1. 保持角色的一致性和个性特征
2. 使用自然的口语化表达，避免机械化回答
3. 展现真实的思考过程和情感反应
4. 对其他人的发言进行有意义的回应和互动
5. 结合个人经历和专业背景提供独特见解
"""

        return full_prompt, enhanced_system_prompt

    def _get_agent_speaking_style(self) -> str:
        """
        获取智能体独特的说话风格

        Returns:
            说话风格指导
        """
        style_guides = {
            "craftsman": """
你的说话风格特点：
- 语调沉稳，经常提到传统和经验
- 喜欢用"我记得..."、"以前..."开头分享经历
- 说话时会停顿思考，用"这个嘛..."、"让我想想..."
- 经常提到具体的工艺细节和材料
- 语气谦逊但充满自信，如"虽说我做了这么多年..."
""",
            "consumer": """
你的说话风格特点：
- 语调活泼，经常表达个人感受
- 喜欢用"我觉得..."、"感觉..."表达观点
- 会分享购物和使用体验，如"我之前买过..."
- 关注实用性，经常问"这个好用吗？"
- 语气直接但友好，如"说实话..."、"老实说..."
""",
            "manufacturer": """
你的说话风格特点：
- 语调务实，经常谈到成本和可行性
- 喜欢用数据和事实说话，如"从成本角度看..."
- 会提到生产流程和技术限制
- 思考问题比较全面，如"我们还要考虑..."
- 语气专业但平易近人，如"实际上..."、"按我的经验..."
""",
            "designer": """
你的说话风格特点：
- 语调充满创意，经常提到美学和设计理念
- 喜欢用"从设计角度..."、"视觉上..."开头
- 会描述具体的设计元素和效果
- 思维跳跃，经常有新想法，如"突然想到..."
- 语气热情但专业，如"这个想法很棒！"、"我们可以尝试..."
"""
        }

        return style_guides.get(self.current_role, "")

    def _build_reflective_role_switch_prompt(
        self,
        original_role: str,
        new_role: str,
        topic: str,
        global_context: Optional[str] = None,
        memories: Optional[List[str]] = None
    ) -> Tuple[str, str]:
        """
        构建反思式角色转换prompt

        Args:
            original_role: 原始角色
            new_role: 新角色
            topic: 讨论主题
            global_context: 全局记忆上下文
            memories: 个人记忆列表

        Returns:
            (prompt, system_prompt) 元组
        """
        from src.config.prompts.template_manager import PromptTemplates

        # 获取新角色的说话风格
        new_role_style = self._get_agent_speaking_style()

        # 构建个人背景信息
        background_info = f"""
你是{self.name}，{self.background}
年龄：{self.age}岁
经验：{self.experience}
原始角色：{original_role}
现在要转换到的角色：{new_role}
"""

        # 构建记忆部分
        memory_section = ""
        if memories:
            memory_section = f"""
你的个人记忆和经验：
{chr(10).join(memories)}
"""

        # 构建全局上下文部分（其他人的发言）
        context_section = ""
        if global_context and "暂无" not in global_context:
            context_section = f"""
会议中的发言历史：
{global_context}
"""

        # 构建反思式角色转换指导
        reflection_guidelines = f"""
现在你需要进行角色转换，这是一个反思和视角切换的过程：

1. **反思阶段**：
   - 先回顾一下自己之前作为{original_role}时的发言和观点
   - 思考其他人的发言给你带来的启发
   - 反思之前可能没有考虑到的角度

2. **视角转换**：
   - 现在从{new_role}的视角重新审视这个话题
   - 你仍然是原来的{self.name}，但现在要用{new_role}的思维方式思考
   - 结合{new_role}的专业知识和关注点

3. **新观点表达**：
   - 基于反思和新视角，提出你的新想法
   - 可以对之前的观点进行补充、修正或深化
   - 展现{new_role}特有的思考角度

{new_role_style}

请按照以下结构回答：
- 首先简单反思一下之前的讨论（1-2句话）
- 然后说明你现在从{new_role}角度的新思考
- 最后提出具体的观点和建议

注意：不要进行自我介绍，直接进入反思和新观点的表达。
"""

        # 构建完整的prompt
        full_prompt = f"""{background_info}

当前讨论主题：{topic}

{memory_section}

{context_section}

{reflection_guidelines}

重要提示：
1. 这不是全新的发言，而是基于之前讨论的反思和视角转换
2. 体现出从{original_role}到{new_role}的思维转变过程
3. 使用{new_role}特有的表达风格和关注点
4. 字数控制在200-300字之间
5. 不要重复之前已经说过的内容，要有新的思考角度"""

        # 构建系统prompt
        enhanced_system_prompt = f"""
你现在正在进行角色转换，从{original_role}转换为{new_role}。这不是扮演一个全新的角色，而是：

1. 保持你的身份和所有记忆
2. 从{new_role}的专业视角重新思考问题
3. 展现{new_role}特有的思维方式和表达风格
4. 对之前的讨论进行反思和补充

请确保：
- 不要进行自我介绍
- 体现出思维的转变过程
- 使用{new_role}的专业术语和关注点
- 保持自然的对话风格
"""

        return full_prompt, enhanced_system_prompt

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

        # 获取全局记忆上下文（会议中其他人的发言）
        global_context = None
        if self.global_memory:
            global_context = await self.global_memory.get_current_context(
                requesting_agent_id=self.id,
                max_context=8
            )

        # 获取个人记忆信息
        memories = await self._call_memory_method("get_relevant_memories", topic)

        # 构建拟人化的讨论prompt
        prompt, system_prompt = self._build_humanized_discussion_prompt(
            topic=topic,
            context=context,
            global_context=global_context,
            memories=memories
        )

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

        from src.config.prompts.template_manager import PromptTemplates
        prompt = PromptTemplates.get_keyword_extraction_prompt(content, topic)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)

        response = await self.model.generate(prompt, system_prompt)

        # 解析关键词
        try:
            # 尝试直接解析JSON
            keywords = json.loads(response)
        except:
            # 尝试提取<key_words>标签内的内容
            key_words_match = re.search(r'<key_words>(.*?)</key_words>', response, re.DOTALL)
            if key_words_match:
                keywords_str = key_words_match.group(1)
                keywords = [k.strip().strip('"\'') for k in keywords_str.split(',')]
            else:
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

        # 清理空关键词
        keywords = [kw.strip() for kw in keywords if kw.strip()]

        # 记录实际提取的关键词数量
        if len(keywords) == 0:
            self.logger.warning(f"智能体 {self.name} 未能提取到任何关键词")
        else:
            self.logger.info(f"智能体 {self.name} 提取到 {len(keywords)} 个关键词")

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

        from src.config.prompts.template_manager import PromptTemplates
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

    async def tell_story_from_description(self, image_description: str, image_path: str) -> Tuple[str, List[str]]:
        """
        基于图像描述讲故事并提取关键词（避免重复调用视觉模型）

        Args:
            image_description: 图像描述
            image_path: 图片路径（用于记录）

        Returns:
            故事内容和关键词列表
        """
        self.logger.info(f"智能体 {self.name} 正在基于图像描述讲故事")

        from src.config.prompts.template_manager import PromptTemplates
        base_prompt = PromptTemplates.get_image_story_prompt(self.current_role)
        system_prompt = PromptTemplates.get_system_prompt(self.current_role)

        # 构建基于图像描述的提示词
        prompt = f"""
        以下是一张图片的详细描述：

        {image_description}

        {base_prompt}

        请基于上述图像描述来创作你的故事，而不是直接看图片。

        你的基本信息：
        年龄：{self.age}岁
        背景：{self.background}
        经验：{self.experience}
        """

        # 生成故事
        story = await self.model.generate(prompt, system_prompt)

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
            "image_story_from_description",
            {
                "role": self.current_role,
                "story": story,
                "keywords": keywords,
                "image_path": image_path,
                "image_description": image_description
            }
        )

        self.keywords = keywords
        return story, keywords

    async def switch_role(self, new_role: str, topic: str) -> str:
        """
        转换角色 - 反思式角色转换

        Args:
            new_role: 新角色
            topic: 讨论主题

        Returns:
            角色转换后的反思和新视角发言
        """
        self.logger.info(f"智能体 {self.name} 正在从 {self.current_role} 转换为 {new_role}")

        # 保存原始角色
        original_role = self.current_role

        # 更新当前角色
        self.current_role = new_role

        # 获取全局记忆上下文（会议中其他人的发言）
        global_context = None
        if self.global_memory:
            global_context = await self.global_memory.get_current_context(
                requesting_agent_id=self.id,
                max_context=10
            )

        # 获取个人记忆信息
        memories = await self._call_memory_method("get_relevant_memories", topic)

        # 构建反思式角色转换prompt
        prompt, system_prompt = self._build_reflective_role_switch_prompt(
            original_role=original_role,
            new_role=new_role,
            topic=topic,
            global_context=global_context,
            memories=memories
        )

        # 生成角色转换后的反思和新视角发言
        response = await self.model.generate(prompt, system_prompt)

        # 将角色转换记录存入记忆
        await self._call_memory_method(
            "add_memory",
            "role_switch",
            {
                "previous_role": original_role,
                "new_role": new_role,
                "topic": topic,
                "reflection": response
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

        from src.config.prompts.template_manager import PromptTemplates
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
