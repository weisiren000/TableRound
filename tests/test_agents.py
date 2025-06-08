#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
智能体测试
"""

import os
import sys
import unittest
from pathlib import Path

# 添加项目根目录到Python路径
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import asyncio
from dotenv import load_dotenv

from src.agents.craftsman import Craftsman
from src.agents.consumer import Consumer
from src.agents.manufacturer import Manufacturer
from src.agents.designer import Designer
from src.core.memory import Memory
from src.models.openrouter import OpenRouterModel


# 加载环境变量
load_dotenv()


class TestAgents(unittest.TestCase):
    """智能体测试类"""
    
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
        
        # 创建临时目录
        self.test_dir = ROOT_DIR / "tests" / "temp"
        os.makedirs(self.test_dir, exist_ok=True)
    
    def tearDown(self):
        """测试后清理"""
        # 清理临时文件
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_craftsman(self):
        """测试手工艺人智能体"""
        # 创建记忆模块
        memory = Memory(
            agent_id="test_craftsman",
            storage_type="file",
            max_tokens=1000
        )
        
        # 创建手工艺人智能体
        craftsman = Craftsman(
            agent_id="test_craftsman",
            name="测试手工艺人",
            model=self.model,
            memory=memory,
            crafts=["剪纸", "木雕"],
            experience_years=15
        )
        
        # 测试自我介绍
        introduction = asyncio.run(craftsman.introduce())
        self.assertIsInstance(introduction, str)
        self.assertTrue(len(introduction) > 0)
        print(f"手工艺人自我介绍: {introduction[:100]}...")
        
        # 测试讨论
        discussion = asyncio.run(craftsman.discuss("传统工艺在现代社会的价值"))
        self.assertIsInstance(discussion, str)
        self.assertTrue(len(discussion) > 0)
        print(f"手工艺人讨论: {discussion[:100]}...")
    
    def test_consumer(self):
        """测试消费者智能体"""
        # 创建记忆模块
        memory = Memory(
            agent_id="test_consumer",
            storage_type="file",
            max_tokens=1000
        )
        
        # 创建消费者智能体
        consumer = Consumer(
            agent_id="test_consumer",
            name="测试消费者",
            model=self.model,
            memory=memory,
            age=30,
            gender="女",
            interests=["文化", "收藏"]
        )
        
        # 测试自我介绍
        introduction = asyncio.run(consumer.introduce())
        self.assertIsInstance(introduction, str)
        self.assertTrue(len(introduction) > 0)
        print(f"消费者自我介绍: {introduction[:100]}...")
        
        # 测试讨论
        discussion = asyncio.run(consumer.discuss("文创产品的实用性与艺术性"))
        self.assertIsInstance(discussion, str)
        self.assertTrue(len(discussion) > 0)
        print(f"消费者讨论: {discussion[:100]}...")
    
    def test_manufacturer(self):
        """测试制造商人智能体"""
        # 创建记忆模块
        memory = Memory(
            agent_id="test_manufacturer",
            storage_type="file",
            max_tokens=1000
        )
        
        # 创建制造商人智能体
        manufacturer = Manufacturer(
            agent_id="test_manufacturer",
            name="测试制造商人",
            model=self.model,
            memory=memory,
            company_size="中型",
            production_capacity=3000
        )
        
        # 测试自我介绍
        introduction = asyncio.run(manufacturer.introduce())
        self.assertIsInstance(introduction, str)
        self.assertTrue(len(introduction) > 0)
        print(f"制造商人自我介绍: {introduction[:100]}...")
        
        # 测试讨论
        discussion = asyncio.run(manufacturer.discuss("文创产品的规模化生产"))
        self.assertIsInstance(discussion, str)
        self.assertTrue(len(discussion) > 0)
        print(f"制造商人讨论: {discussion[:100]}...")
    
    def test_designer(self):
        """测试设计师智能体"""
        # 创建记忆模块
        memory = Memory(
            agent_id="test_designer",
            storage_type="file",
            max_tokens=1000
        )
        
        # 创建设计师智能体
        designer = Designer(
            agent_id="test_designer",
            name="测试设计师",
            model=self.model,
            memory=memory,
            design_style="现代简约",
            experience_years=8
        )
        
        # 测试自我介绍
        introduction = asyncio.run(designer.introduce())
        self.assertIsInstance(introduction, str)
        self.assertTrue(len(introduction) > 0)
        print(f"设计师自我介绍: {introduction[:100]}...")
        
        # 测试讨论
        discussion = asyncio.run(designer.discuss("传统元素在现代设计中的应用"))
        self.assertIsInstance(discussion, str)
        self.assertTrue(len(discussion) > 0)
        print(f"设计师讨论: {discussion[:100]}...")


if __name__ == "__main__":
    unittest.main()
