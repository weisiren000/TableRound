#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
对话管理测试
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# 添加项目根目录到Python路径
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import asyncio
from dotenv import load_dotenv

from src.config.settings import Settings
from src.core.agent import Agent
from src.core.conversation import ConversationManager
from src.core.god_view import GodView
from src.core.memory import Memory
from src.models.openrouter import OpenRouterModel


# 加载环境变量
load_dotenv()


class TestConversation(unittest.TestCase):
    """对话管理测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 获取API密钥
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            self.skipTest("缺少OpenRouter API密钥")
        
        # 创建模型
        self.model = OpenRouterModel(
            model_name="meta-llama/llama-4-scout:free",
            api_key=self.api_key
        )
        
        # 创建设置
        self.settings = Settings()
        
        # 创建上帝视角
        self.god_view = GodView(self.settings)
        
        # 创建对话管理器
        self.conversation_manager = ConversationManager(self.god_view, self.settings)
        
        # 创建临时目录
        self.test_dir = ROOT_DIR / "tests" / "temp"
        os.makedirs(self.test_dir, exist_ok=True)
    
    def tearDown(self):
        """测试后清理"""
        # 清理临时文件
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_add_agent(self):
        """测试添加智能体"""
        # 创建记忆模块
        memory = Memory(
            agent_id="test_agent",
            storage_type="file",
            max_tokens=1000
        )
        
        # 创建智能体
        agent = Agent(
            agent_id="test_agent",
            agent_type="craftsman",
            name="测试智能体",
            model=self.model,
            memory=memory
        )
        
        # 添加智能体
        self.conversation_manager.add_agent(agent)
        
        # 验证智能体已添加
        self.assertIn("test_agent", self.conversation_manager.agents)
        self.assertEqual(self.conversation_manager.agents["test_agent"], agent)
    
    def test_get_agents_by_type(self):
        """测试按类型获取智能体"""
        # 创建并添加多个智能体
        for i, agent_type in enumerate(["craftsman", "consumer", "consumer", "manufacturer"]):
            memory = Memory(
                agent_id=f"test_agent_{i}",
                storage_type="file",
                max_tokens=1000
            )
            
            agent = Agent(
                agent_id=f"test_agent_{i}",
                agent_type=agent_type,
                name=f"测试智能体{i}",
                model=self.model,
                memory=memory
            )
            
            self.conversation_manager.add_agent(agent)
        
        # 获取消费者智能体
        consumer_agents = self.conversation_manager.get_agents_by_type("consumer")
        
        # 验证结果
        self.assertEqual(len(consumer_agents), 2)
        for agent in consumer_agents:
            self.assertEqual(agent.type, "consumer")
    
    @patch('src.core.agent.Agent.introduce')
    @patch('src.core.agent.Agent.discuss')
    @patch('src.core.agent.Agent.extract_keywords')
    @patch('src.core.agent.Agent.vote_keywords')
    @patch('src.utils.stream.StreamHandler.stream_output')
    async def test_start_conversation(self, mock_stream, mock_vote, mock_extract, mock_discuss, mock_introduce):
        """测试开始对话"""
        # 设置模拟返回值
        mock_introduce.return_value = "这是自我介绍"
        mock_discuss.return_value = "这是讨论内容"
        mock_extract.return_value = ["关键词1", "关键词2", "关键词3"]
        mock_vote.return_value = ["关键词1", "关键词2"]
        mock_stream.return_value = None
        
        # 创建并添加智能体
        for i, agent_type in enumerate(["craftsman", "consumer", "manufacturer", "designer"]):
            memory = Memory(
                agent_id=f"test_agent_{i}",
                storage_type="file",
                max_tokens=1000
            )
            
            agent = Agent(
                agent_id=f"test_agent_{i}",
                agent_type=agent_type,
                name=f"测试智能体{i}",
                model=self.model,
                memory=memory
            )
            
            self.conversation_manager.add_agent(agent)
        
        # 模拟上帝视角总结
        self.god_view.summarize_stage = AsyncMock()
        
        # 开始对话
        await self.conversation_manager.start_conversation("测试主题")
        
        # 验证方法调用
        self.assertTrue(mock_introduce.called)
        self.assertTrue(mock_discuss.called)
        self.assertTrue(mock_extract.called)
        self.assertTrue(mock_vote.called)
        self.assertTrue(mock_stream.called)
        self.assertTrue(self.god_view.summarize_stage.called)
        
        # 验证对话状态
        self.assertEqual(self.conversation_manager.topic, "测试主题")
        self.assertEqual(self.conversation_manager.stage, "waiting")
        self.assertTrue(len(self.conversation_manager.discussion_history) > 0)
        self.assertTrue(len(self.conversation_manager.all_keywords) > 0)
        self.assertTrue(len(self.conversation_manager.voted_keywords) > 0)
    
    @patch('src.core.agent.Agent.switch_role')
    @patch('src.core.agent.Agent.discuss')
    @patch('src.core.agent.Agent.extract_keywords')
    @patch('src.core.agent.Agent.vote_keywords')
    @patch('src.utils.stream.StreamHandler.stream_output')
    async def test_start_role_switch(self, mock_stream, mock_vote, mock_extract, mock_discuss, mock_switch):
        """测试角色转换"""
        # 设置模拟返回值
        mock_switch.return_value = "角色转换成功"
        mock_discuss.return_value = "这是角色转换后的讨论内容"
        mock_extract.return_value = ["新关键词1", "新关键词2", "新关键词3"]
        mock_vote.return_value = ["新关键词1", "新关键词2"]
        mock_stream.return_value = None
        
        # 创建并添加智能体
        for i, agent_type in enumerate(["craftsman", "consumer", "manufacturer", "designer"]):
            memory = Memory(
                agent_id=f"test_agent_{i}",
                storage_type="file",
                max_tokens=1000
            )
            
            agent = Agent(
                agent_id=f"test_agent_{i}",
                agent_type=agent_type,
                name=f"测试智能体{i}",
                model=self.model,
                memory=memory
            )
            
            self.conversation_manager.add_agent(agent)
        
        # 模拟上帝视角总结
        self.god_view.summarize_stage = AsyncMock()
        
        # 设置初始状态
        self.conversation_manager.topic = "测试主题"
        self.conversation_manager.discussion_history = [{"stage": "introduction", "content": "自我介绍"}]
        
        # 开始角色转换
        await self.conversation_manager.start_role_switch(["最终关键词1", "最终关键词2"])
        
        # 验证方法调用
        self.assertTrue(mock_switch.called)
        self.assertTrue(mock_discuss.called)
        self.assertTrue(mock_extract.called)
        self.assertTrue(mock_vote.called)
        self.assertTrue(mock_stream.called)
        self.assertTrue(self.god_view.summarize_stage.called)
        
        # 验证对话状态
        self.assertEqual(self.conversation_manager.stage, "waiting")
        self.assertEqual(self.conversation_manager.final_keywords, ["最终关键词1", "最终关键词2"])


if __name__ == "__main__":
    unittest.main()
