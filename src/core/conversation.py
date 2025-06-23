#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
对话管理模块
"""

import logging
import random
import re
import json
import uuid
from typing import Dict, List, Any, Tuple, Optional

from src.core.agent import Agent
from src.core.global_memory import GlobalMemory
from src.core.meeting_cleaner import clean_redis_for_new_meeting, get_redis_status
from src.utils.stream import StreamHandler


class ConversationManager:
    """对话管理器"""

    def __init__(self, god_view, settings, clean_redis_on_start: Optional[bool] = None):
        """
        初始化对话管理器

        Args:
            god_view: 上帝视角
            settings: 全局设置
            clean_redis_on_start: 是否在启动时清理Redis数据（None时使用配置文件设置）
        """
        self.god_view = god_view
        self.settings = settings
        self.agents: Dict[str, Agent] = {}
        self.topic = ""
        self.stage = "init"
        self.discussion_history = []
        self.voted_keywords = []
        self.final_keywords = []
        self.stream_handler = StreamHandler(enable_ui_enhancement=True)
        self.logger = logging.getLogger("conversation")

        # 使用配置文件设置或传入参数
        self.clean_redis_on_start = (
            clean_redis_on_start if clean_redis_on_start is not None
            else getattr(settings, 'clean_redis_on_start', True)
        )

        # 创建全局记忆实例
        self.session_id = str(uuid.uuid4())
        self.global_memory = GlobalMemory(self.session_id, storage_type="auto")
        self.logger.info(f"创建会议会话: {self.session_id}")

        # 标记是否已清理Redis
        self._redis_cleaned = False

    async def prepare_for_new_meeting(self, preserve_agent_memories: bool = False) -> Dict[str, Any]:
        """
        为新会议准备Redis环境

        Args:
            preserve_agent_memories: 是否保留智能体历史记忆

        Returns:
            清理结果
        """
        if not self.clean_redis_on_start or self._redis_cleaned:
            return {"skipped": True, "reason": "清理已禁用或已执行"}

        try:
            self.logger.info("🧹 为新会议清理Redis数据...")
            await self.stream_handler.stream_output("🧹 正在为新会议清理数据...\n")

            # 获取清理前的状态
            before_status = await get_redis_status()

            # 执行清理
            clean_result = await clean_redis_for_new_meeting(
                preserve_agent_memories=preserve_agent_memories,
                backup_before_clean=True
            )

            # 获取清理后的状态
            after_status = await get_redis_status()

            if clean_result.get("success", False):
                self._redis_cleaned = True
                self.logger.info(f"✅ Redis清理完成，耗时 {clean_result.get('duration', 0)} 秒")

                # 显示清理结果
                await self.stream_handler.stream_output(
                    f"✅ 数据清理完成！\n"
                    f"   清理前: {before_status.get('total_keys', 0)} 个键\n"
                    f"   清理后: {after_status.get('total_keys', 0)} 个键\n"
                    f"   耗时: {clean_result.get('duration', 0)} 秒\n\n"
                )
            else:
                self.logger.warning(f"⚠️ Redis清理失败: {clean_result.get('error', 'Unknown error')}")
                await self.stream_handler.stream_output("⚠️ 数据清理失败，但不影响会议进行\n\n")

            return clean_result

        except Exception as e:
            self.logger.error(f"❌ Redis清理异常: {str(e)}")
            await self.stream_handler.stream_output("❌ 数据清理异常，但不影响会议进行\n\n")
            return {"success": False, "error": str(e)}

    async def add_agent(self, agent: Agent) -> None:
        """
        添加智能体

        Args:
            agent: 智能体
        """
        # 设置agent的全局记忆
        agent.global_memory = self.global_memory

        # 添加到agents字典
        self.agents[agent.id] = agent

        # 在全局记忆中注册参与者
        await self.global_memory.add_participant(
            agent_id=agent.id,
            agent_name=agent.name,
            agent_role=agent.current_role
        )

        self.logger.info(f"添加智能体: {agent.name} ({agent.type})")

    def remove_agent(self, agent_id: str) -> None:
        """
        移除智能体

        Args:
            agent_id: 智能体ID
        """
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            self.logger.info(f"移除智能体: {agent.name} ({agent.type})")

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
        获取智能体

        Args:
            agent_id: 智能体ID

        Returns:
            智能体
        """
        return self.agents.get(agent_id)

    def get_agents_by_type(self, agent_type: str) -> List[Agent]:
        """
        获取指定类型的智能体

        Args:
            agent_type: 智能体类型

        Returns:
            智能体列表
        """
        return [agent for agent in self.agents.values() if agent.type == agent_type]

    async def start_conversation(self, topic: str, image_path: str = None) -> None:
        """
        开始对话

        Args:
            topic: 讨论主题
            image_path: 可选的图片路径，用于讨论参考
        """
        # 为新会议清理Redis数据
        preserve_memories = getattr(self.settings, 'preserve_agent_memories', False)
        await self.prepare_for_new_meeting(preserve_agent_memories=preserve_memories)

        self.logger.info(f"开始对话，主题: {topic}")
        self.topic = topic
        self.stage = "introduction"
        self.discussion_history = []

        # 设置图像路径（如果提供）
        self.reference_image = image_path
        self.image_keywords = []

        # 智能体自我介绍（先进行自我介绍）
        await self.global_memory.update_stage("introduction")
        await self.introduce_agents()

        # 如果提供了图片，在自我介绍后处理图片
        if image_path:
            self.logger.info(f"使用参考图片: {image_path}")
            await self.stream_handler.stream_output(f"\n===== 使用参考图片 =====\n")
            await self.stream_handler.stream_output(f"图片路径: {image_path}\n\n")

            try:
                # 提取图片关键词
                self.image_keywords = await self.process_image(image_path)

                # 将图片关键词添加到讨论历史
                self.discussion_history.append({
                    "stage": "image_reference",
                    "image_path": image_path,
                    "keywords": self.image_keywords
                })
            except Exception as e:
                self.logger.error(f"图像处理失败: {str(e)}")
                await self.stream_handler.stream_output(f"\n图像处理失败: {str(e)}\n但仍将继续讨论\n\n")

        # 开始讨论
        self.stage = "discussion"
        await self.global_memory.update_stage("discussion")
        await self.start_discussion()

        # 提取关键词
        self.stage = "keywords"
        await self.global_memory.update_stage("keywords")
        await self.extract_keywords()

        # 投票
        self.stage = "voting"
        await self.global_memory.update_stage("voting")
        await self.vote_keywords()

        # 等待上帝输入关键词
        self.stage = "waiting"
        await self.stream_handler.stream_output(
            "\n请输入最终关键词（用逗号分隔），或直接按回车使用投票结果:\n"
        )

    async def introduce_agents(self) -> None:
        """智能体自我介绍"""
        self.logger.info("智能体自我介绍")

        # 使用美化的标题
        await self.stream_handler.stream_enhanced_output("", "introduction_header")

        for agent in self.agents.values():
            # 设置当前智能体信息
            self.stream_handler.set_current_agent(agent.name, agent.type)

            # 启动加载动画
            from src.ui_enhanced.animations import LoadingSpinner
            spinner = LoadingSpinner(f"{agent.name} 正在准备自我介绍", "spinner")
            spinner.start()

            try:
                introduction = await agent.introduce()
            finally:
                spinner.stop()

            # 使用美化的智能体介绍输出
            await self.stream_handler.stream_enhanced_output(introduction, "agent_introduction")

            # 添加到讨论历史
            self.discussion_history.append({
                "stage": "introduction",
                "agent": agent.name,
                "content": introduction
            })

    async def start_discussion(self) -> None:
        """开始讨论（增强图像关联）"""
        self.logger.info(f"开始讨论，主题: {self.topic}")
        
        # 使用美化的讨论标题
        await self.stream_handler.stream_enhanced_output("", "discussion_header")
        
        # 获取所有智能体并按特定顺序排列
        agents = []

        # 获取各类型智能体
        craftsmen = [agent for agent in self.agents.values() if agent.type == "craftsman"]
        consumers = [agent for agent in self.agents.values() if agent.type == "consumer"]
        manufacturers = [agent for agent in self.agents.values() if agent.type == "manufacturer"]
        designers = [agent for agent in self.agents.values() if agent.type == "designer"]

        # 确保有足够的消费者
        if len(consumers) >= 3:
            # 按指定顺序添加智能体
            if craftsmen:
                agents.append(craftsmen[0])
            if consumers:
                agents.append(consumers[0])
            if manufacturers:
                agents.append(manufacturers[0])
            if len(consumers) > 1:
                agents.append(consumers[1])
            if designers:
                agents.append(designers[0])
            if len(consumers) > 2:
                agents.append(consumers[2])
        else:
            # 如果消费者不足，使用所有智能体并随机排序
            agents = list(self.agents.values())
            random.shuffle(agents)
        
        # 讨论轮数
        max_turns = self.settings.max_turns
        
        for turn in range(max_turns):
            self.logger.info(f"讨论轮次: {turn + 1}/{max_turns}")
            await self.stream_handler.stream_output(f"\n----- 讨论轮次 {turn + 1}/{max_turns} -----\n")
            
            # 获取上下文
            if turn == 0:
                # 第一轮讨论，结合图像信息（如果有）
                context = f"讨论主题: {self.topic}"
                
                # 如果有图像参考，添加图像相关信息
                if hasattr(self, 'reference_image') and self.reference_image and hasattr(self, 'image_keywords') and self.image_keywords:
                    context += f"\n\n参考图像关键词: {', '.join(self.image_keywords)}\n\n"
                    context += "请在讨论中自然地融入图像中的元素和灵感。"
            else:
                # 获取上一轮的讨论内容
                prev_turn_discussions = [
                    f"{item['agent']}: {item['content']}"
                    for item in self.discussion_history
                    if item['stage'] == f"discussion_turn_{turn}"
                ]
                context = "\n".join(prev_turn_discussions)
            
            # 每个智能体发言
            for agent in agents:
                # 设置当前智能体信息
                self.stream_handler.set_current_agent(agent.name, agent.type)
                
                # 启动加载动画
                from src.ui_enhanced.animations import LoadingSpinner
                spinner = LoadingSpinner(f"{agent.name} 正在思考", "spinner")
                spinner.start()
                
                try:
                    # 增强的讨论提示，确保图像关联
                    discussion_prompt = context
                    
                    if turn == 0 and hasattr(self, 'reference_image') and self.reference_image:
                        # 为首轮讨论添加图像关联提示
                        try:
                            # 使用异步方法获取记忆
                            image_stories = await agent.memory.get_memories_by_type("image_story")
                            if image_stories and len(image_stories) > 0:
                                # 从最新的故事中提取内容
                                story_text = image_stories[0]
                                if story_text:
                                    # 提取前200个字符作为提示
                                    story_preview = story_text[:200]
                                    discussion_prompt += f"\n\n你之前基于图像创作的故事:\n{story_preview}...\n\n请在讨论中自然地融入你从图像获得的灵感和想法。"
                        except Exception as e:
                            self.logger.warning(f"获取图像故事记忆失败: {str(e)}")
                            # 继续执行，即使没有图像故事
                    
                    response = await agent.discuss(self.topic, discussion_prompt)
                except Exception as e:
                    self.logger.error(f"智能体 {agent.name} 讨论失败: {str(e)}")
                    response = f"(由于技术原因无法提供有效回应，将继续讨论)"
                finally:
                    spinner.stop()
                
                # 使用美化的讨论输出
                await self.stream_handler.stream_enhanced_output(response, "agent_discussion")
                
                # 添加到讨论历史
                self.discussion_history.append({
                    "stage": f"discussion_turn_{turn + 1}",
                    "agent": agent.name,
                    "content": response
                })

    async def extract_keywords(self) -> None:
        """提取关键词（增强图像关联）"""
        self.logger.info("提取关键词")
        await self.stream_handler.stream_output("\n===== 提取关键词 =====\n")
        
        # 获取讨论内容
        discussion_content = "\n".join([
            f"{item['agent']}: {item['content']}"
            for item in self.discussion_history
            if item['stage'].startswith("discussion_turn_")
        ])
        
        # 导入颜色支持
        from src.utils.colors import Colors
        
        # 准备图像相关上下文
        image_context = ""
        if hasattr(self, 'image_keywords') and self.image_keywords:
            image_context = f"参考图像关键词: {', '.join(self.image_keywords)}\n\n"
        
        # 每个智能体提取关键词
        for agent in self.agents.values():
            # 启动加载动画
            from src.ui_enhanced.animations import LoadingSpinner
            spinner = LoadingSpinner(f"{agent.name} 正在提取关键词", "dots")
            spinner.start()
            
            try:
                # 构建增强的关键词提取上下文
                enhanced_context = discussion_content
                if image_context:
                    enhanced_prompt = f"{self.topic}\n\n{image_context}讨论内容:\n{discussion_content}"
                    keywords = await agent.extract_keywords(enhanced_prompt, self.topic)
                else:
                    keywords = await agent.extract_keywords(discussion_content, self.topic)
            except Exception as e:
                self.logger.error(f"关键词提取失败: {str(e)}")
                keywords = ["提取失败"]
            finally:
                spinner.stop()
            
            # 使用绿色显示关键词
            colored_keywords = [Colors.green(kw) for kw in keywords]
            keywords_str = ", ".join(colored_keywords)
            
            await self.stream_handler.stream_output(f"【{agent.name}】提取的关键词:\n{keywords_str}\n\n")
            
            # 添加到讨论历史
            self.discussion_history.append({
                "stage": "keywords",
                "agent": agent.name,
                "keywords": keywords
            })

    async def vote_keywords(self) -> None:
        """投票关键词"""
        self.logger.info("投票关键词")
        await self.stream_handler.stream_output("\n===== 关键词投票 =====\n")

        # 收集所有关键词
        all_keywords = []
        for agent in self.agents.values():
            all_keywords.extend(agent.keywords)

        # 去重
        unique_keywords = list(set(all_keywords))

        # 如果关键词太少，直接使用
        if len(unique_keywords) <= self.settings.max_keywords:
            self.voted_keywords = unique_keywords
            await self.stream_handler.stream_output(f"关键词数量较少，直接使用所有关键词:\n{', '.join(unique_keywords)}\n\n")
            return

        # 使用黑箱投票机制
        from src.utils.voting import VotingSystem
        voting_system = VotingSystem(threshold=self.settings.voting_threshold)

        # 获取讨论内容作为投票上下文
        discussion_content = "\n".join([
            f"{item['agent']}: {item['content']}"
            for item in self.discussion_history
            if item['stage'] == "discussion"
        ])

        # 每个智能体进行智能投票
        agent_keywords = {}
        for agent in self.agents.values():
            # 启动加载动画
            from src.ui_enhanced.animations import LoadingSpinner
            spinner = LoadingSpinner(f"{agent.name} 正在投票", "dots")
            spinner.start()

            try:
                # 使用智能投票而不是随机投票
                vote_count = min(len(unique_keywords), 5)
                voted = await agent.intelligent_vote(unique_keywords, discussion_content, vote_count)
            finally:
                spinner.stop()

            agent_keywords[agent.id] = voted

            voted_str = ", ".join(voted)
            await self.stream_handler.stream_output(f"【{agent.name}】投票给:\n{voted_str}\n\n")

            # 添加到讨论历史
            self.discussion_history.append({
                "stage": "voting",
                "agent": agent.name,
                "voted_keywords": voted
            })

        # 使用共识投票
        voting_results = voting_system.consensus_voting(
            agent_keywords,
            max_keywords=self.settings.max_keywords
        )

        # 获取最终关键词
        self.voted_keywords = voting_system.get_final_keywords(
            voting_results,
            max_keywords=self.settings.max_keywords
        )

        # 显示投票结果
        result_str = "\n".join([f"{kw}: {votes} 票" for kw, votes in voting_results])
        await self.stream_handler.stream_output(f"投票结果:\n{result_str}\n\n")
        await self.stream_handler.stream_output(f"选出的关键词:\n{', '.join(self.voted_keywords)}\n\n")

    async def start_role_switch(self, final_keywords: List[str]) -> None:
        """
        开始角色转换阶段

        Args:
            final_keywords: 最终关键词列表
        """
        self.logger.info("开始角色转换阶段")
        self.final_keywords = final_keywords

        # 更新阶段
        self.stage = "role_switch"
        await self.stream_handler.stream_output("\n===== 视角转换阶段 =====\n")
        await self.stream_handler.stream_output("(智能体将从不同角色的视角思考问题，但保持原有身份和记忆)\n")

        # 获取所有智能体
        agents = list(self.agents.values())

        # 为每个智能体分配一个不同的角色
        roles = [agent.type for agent in agents]
        new_roles = roles.copy()
        random.shuffle(new_roles)

        # 确保每个智能体都转换为不同的角色
        while any(r1 == r2 for r1, r2 in zip(roles, new_roles)):
            random.shuffle(new_roles)

        # 角色转换
        for agent, new_role in zip(agents, new_roles):
            # 确保不转换为自己的原始角色
            if new_role == agent.type:
                # 找一个不同的角色
                available_roles = [r for r in roles if r != agent.type]
                new_role = random.choice(available_roles)

            # 执行角色转换
            self.logger.info(f"智能体 {agent.name} 从 {agent.type} 转换为 {new_role}")

            # 构建关键词字符串
            keywords_str = ", ".join(final_keywords)

            # 执行角色转换
            response = await agent.switch_role(new_role, keywords_str)
            await self.stream_handler.stream_output(f"【{agent.name}】({agent.type} → {new_role}):\n{response}\n\n")

            # 添加到讨论历史
            self.discussion_history.append({
                "stage": "role_switch",
                "agent": agent.name,
                "original_role": agent.type,
                "new_role": new_role,
                "content": response
            })

        # 更新阶段
        self.stage = "discussion_after_switch"
        await self.stream_handler.stream_output("\n(智能体将保持原有身份，但从新视角参与讨论)\n")
        await self.start_discussion_after_switch()

    async def start_discussion_after_switch(self) -> None:
        """视角转换后的讨论"""
        self.logger.info("视角转换后的讨论")
        await self.stream_handler.stream_output("\n===== 视角转换后的讨论 =====\n")

        # 获取所有智能体并按特定顺序排列
        # 对话顺序：手工艺人、消费者、制造商人、消费者、设计师、消费者
        agents = []

        # 获取各类型智能体（按当前角色）
        craftsmen = [agent for agent in self.agents.values() if agent.current_role == "craftsman"]
        consumers = [agent for agent in self.agents.values() if agent.current_role == "consumer"]
        manufacturers = [agent for agent in self.agents.values() if agent.current_role == "manufacturer"]
        designers = [agent for agent in self.agents.values() if agent.current_role == "designer"]

        # 确保有足够的消费者
        if len(consumers) >= 3:
            # 按指定顺序添加智能体
            if craftsmen:
                agents.append(craftsmen[0])
            if consumers:
                agents.append(consumers[0])
            if manufacturers:
                agents.append(manufacturers[0])
            if len(consumers) > 1:
                agents.append(consumers[1])
            if designers:
                agents.append(designers[0])
            if len(consumers) > 2:
                agents.append(consumers[2])
        else:
            # 如果消费者不足，使用所有智能体并随机排序
            agents = list(self.agents.values())
            random.shuffle(agents)

        # 构建关键词字符串
        keywords_str = ", ".join(self.final_keywords)

        # 设置剪纸研讨会场景
        from src.config.prompts.template_manager import PromptTemplates
        paper_cutting_scenario = PromptTemplates.get_paper_cutting_scenario()
        await self.stream_handler.stream_output(f"【场景设置】\n{paper_cutting_scenario}\n\n")

        # 添加场景设置到讨论历史
        self.discussion_history.append({
            "stage": "scenario_setting",
            "content": paper_cutting_scenario
        })

        # 每个智能体发言
        for agent in agents:
            # 构建讨论提示词，包含剪纸研讨会场景
            discussion_prompt = f"""
            {paper_cutting_scenario}

            请基于以下关键词，从你当前的角色（{agent.current_role}）视角参与剪纸文创产品设计讨论：
            {keywords_str}

            请提供你对剪纸文创产品设计的见解和建议，包括但不限于：
            1. 产品形式和功能
            2. 设计元素和风格
            3. 材料和工艺选择
            4. 目标用户和市场定位
            5. 文化内涵和创新点

            请确保你的发言体现你作为{agent.current_role}的专业视角和关注点。
            """

            response = await agent.discuss(keywords_str, discussion_prompt)
            await self.stream_handler.stream_output(f"【{agent.name}】({agent.current_role}):\n{response}\n\n")

            # 添加到讨论历史
            self.discussion_history.append({
                "stage": "discussion_after_switch",
                "agent": agent.name,
                "role": agent.current_role,
                "content": response
            })

        # 提取关键词
        await self.extract_keywords_after_switch()

    async def extract_keywords_after_switch(self) -> None:
        """角色转换后提取关键词"""
        self.logger.info("角色转换后提取关键词")
        await self.stream_handler.stream_output("\n===== 角色转换后提取关键词 =====\n")

        # 获取讨论内容
        discussion_content = "\n".join([
            f"{item['agent']} ({item['role']}): {item['content']}"
            for item in self.discussion_history
            if item['stage'] == "discussion_after_switch"
        ])

        # 导入颜色支持
        from src.utils.colors import Colors

        # 每个智能体提取关键词
        all_keywords = []
        for agent in self.agents.values():
            keywords = await agent.extract_keywords(discussion_content, ", ".join(self.final_keywords))
            all_keywords.extend(keywords)

            # 使用绿色显示关键词
            colored_keywords = [Colors.green(kw) for kw in keywords]
            keywords_str = ", ".join(colored_keywords)

            await self.stream_handler.stream_output(f"【{agent.name}】({agent.current_role}) 提取的关键词:\n{keywords_str}\n\n")

            # 添加到讨论历史
            self.discussion_history.append({
                "stage": "keywords_after_switch",
                "agent": agent.name,
                "role": agent.current_role,
                "keywords": keywords
            })

        # 去重
        unique_keywords = list(set(all_keywords))

        # 更新阶段
        self.stage = "waiting_for_user_input"

        # 提示用户输入
        await self.stream_handler.stream_output("\n===== 用户输入阶段 =====\n")
        await self.stream_handler.stream_output("请输入设计提示词，用于生成剪纸文创产品设计卡牌。\n")
        await self.stream_handler.stream_output(f"您可以参考以下关键词：{', '.join([Colors.green(kw) for kw in unique_keywords])}\n")
        await self.stream_handler.stream_output("输入提示词后按回车继续...\n")

        # 保存关键词供后续使用
        self.design_keywords = unique_keywords

    async def process_user_input(self, user_input: str) -> Optional[List[str]]:
        """
        处理用户输入，生成图像

        Args:
            user_input: 用户输入的设计提示词
        """
        self.logger.info(f"处理用户输入: {user_input}")

        if not user_input.strip():
            await self.stream_handler.stream_output("未输入设计提示词，使用默认提示词: 传统中国红色调，对称蝴蝶图案，吉祥如意\n")
            user_input = "传统中国红色调，对称蝴蝶图案，吉祥如意"

        # 合并用户输入和之前的关键词
        combined_keywords = self.design_keywords.copy()
        user_keywords = [kw.strip() for kw in user_input.split(",") if kw.strip()]
        combined_keywords.extend(user_keywords)

        # 去重
        combined_keywords = list(set(combined_keywords))

        # 生成图像
        from src.utils.image import ImageProcessor
        image_processor = ImageProcessor(self.settings)

        # 使用豆包API生成图像
        await self.stream_handler.stream_output("\n正在使用豆包API生成图像...\n")

        # 构建完整的提示词 - 用户输入前置以提高权重
        prompt = f"{user_input}，对称的剪纸风格的中国传统蝴蝶吉祥纹样"

        # 生成图像
        image_paths = await image_processor.generate_image(prompt, provider="doubao")

        if image_paths:
            await self.stream_handler.stream_output(f"\n成功生成 {len(image_paths)} 张图像:\n")
            for i, path in enumerate(image_paths, 1):
                await self.stream_handler.stream_output(f"  图像 {i}: {path}\n")
        else:
            await self.stream_handler.stream_output("\n图像生成失败\n")

        # 结束对话
        self.stage = "end"
        await self.stream_handler.stream_output("\n===== 对话结束 =====\n")

        return image_paths

    async def process_image(self, image_path: str) -> List[str]:
        """
        处理图片（优化版 - 无需单独的视觉模型）
        
        Args:
            image_path: 图片路径
            
        Returns:
            提取的关键词列表
        """
        self.logger.info(f"处理图片: {image_path}")
        await self.stream_handler.stream_output("\n===== 处理图片 =====\n")
        
        # 存储图像路径供智能体使用
        self.reference_image = image_path
        await self.stream_handler.stream_output(f"参考图像路径: {image_path}\n\n")
        
        # 导入颜色支持
        from src.utils.colors import Colors
        
        # 所有关键词
        all_keywords = []
        
        # 每个智能体基于图像创建故事并提取关键词
        # (在自我介绍之后进行图像故事创作)
        await self.stream_handler.stream_output("===== 基于图像的故事创作 =====\n")
        for agent in self.agents.values():
            # 启动加载动画
            from src.ui_enhanced.animations import LoadingSpinner
            spinner = LoadingSpinner(f"{agent.name} 正在创作故事", "blocks")
            spinner.start()
            
            try:
                # 直接使用tell_story_from_image方法
                story, keywords = await agent.tell_story_from_image(image_path)
            finally:
                spinner.stop()
                
            # 使用绿色显示关键词
            colored_keywords = [Colors.green(kw) for kw in keywords]
            keywords_str = ", ".join(colored_keywords)
            
            await self.stream_handler.stream_output(f"【{agent.name}】的故事:\n{story}\n\n关键词: {keywords_str}\n\n")
            all_keywords.extend(keywords)
            
        # 去重
        unique_keywords = list(set(all_keywords))
        
        # 如果关键词太多，随机选择一部分
        if len(unique_keywords) > self.settings.max_keywords:
            selected_keywords = random.sample(unique_keywords, self.settings.max_keywords)
        else:
            selected_keywords = unique_keywords
            
        # 使用绿色显示最终选择的关键词
        colored_selected_keywords = [Colors.green(kw) for kw in selected_keywords]
        selected_keywords_str = ", ".join(colored_selected_keywords)
        
        await self.stream_handler.stream_output(f"\n提取的关键词: {selected_keywords_str}\n")
        return selected_keywords

    async def design_paper_cutting(self, keywords: List[str]) -> Dict[str, str]:
        """
        设计剪纸文创产品

        Args:
            keywords: 关键词列表

        Returns:
            设计结果
        """
        self.logger.info(f"设计剪纸文创产品，关键词: {keywords}")
        await self.stream_handler.stream_output("\n===== 设计剪纸文创产品 =====\n")

        # 设计结果
        designs = {}

        # 每个智能体生成设计卡牌
        for agent in self.agents.values():
            design_card = await agent.generate_design_card(keywords)
            await self.stream_handler.stream_output(f"【{agent.name}】的设计卡牌:\n{design_card}\n\n")
            designs[agent.id] = design_card

        return designs

    def merge_keywords(self, kj_keywords: List[str], user_keywords: List[str]) -> List[str]:
        """
        合并KJ法分类结果和用户输入的关键词

        Args:
            kj_keywords: KJ法分类结果
            user_keywords: 用户输入的关键词

        Returns:
            合并后的关键词列表
        """
        # 简单合并并去重
        merged = list(set(kj_keywords + user_keywords))

        # 如果关键词太多，随机选择一部分
        if len(merged) > self.settings.max_keywords:
            return random.sample(merged, self.settings.max_keywords)

        return merged

    # 移除了_describe_image_once方法，该方法不再需要

    async def _process_role_switch(self, original_role: str, new_role: str, topic: str) -> str:
        """
        处理角色转换，获取提示词和结果

        Args:
            original_role: 原角色
            new_role: 新角色
            topic: 主题

        Returns:
            角色转换结果
        """
        from src.config.prompts.template_manager import PromptTemplates
        agent = self._get_agent_by_role(original_role)
