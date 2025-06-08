#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
记忆模块测试
"""

import os
import sys
import unittest
import json
import time
from pathlib import Path

# 添加项目根目录到Python路径
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from dotenv import load_dotenv

from src.config.settings import Settings
from src.core.memory import Memory


# 加载环境变量
load_dotenv()


class TestMemory(unittest.TestCase):
    """记忆模块测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建设置
        self.settings = Settings()
        
        # 创建临时目录
        self.test_dir = ROOT_DIR / "tests" / "temp"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # 设置临时记忆目录
        self.settings.MEMORY_DIR = self.test_dir / "memories"
        os.makedirs(self.settings.MEMORY_DIR, exist_ok=True)
        
        # 创建记忆模块
        self.memory = Memory(
            agent_id="test_agent",
            storage_type="file",
            max_tokens=1000,
            settings=self.settings
        )
    
    def tearDown(self):
        """测试后清理"""
        # 清理临时文件
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_add_memory(self):
        """测试添加记忆"""
        # 添加记忆
        self.memory.add_memory(
            "introduction",
            {"role": "craftsman", "content": "我是一名手工艺人"}
        )
        
        # 验证内存中的记忆
        self.assertEqual(len(self.memory.memories), 1)
        self.assertEqual(self.memory.memories[0]["type"], "introduction")
        self.assertEqual(self.memory.memories[0]["content"]["role"], "craftsman")
        
        # 验证文件存储
        memory_files = list(self.memory.memory_dir.glob("*.json"))
        self.assertEqual(len(memory_files), 1)
        
        # 读取文件内容
        with open(memory_files[0], "r", encoding="utf-8") as f:
            memory_data = json.load(f)
        
        self.assertEqual(memory_data["type"], "introduction")
        self.assertEqual(memory_data["content"]["role"], "craftsman")
    
    def test_get_memories_by_type(self):
        """测试按类型获取记忆"""
        # 添加不同类型的记忆
        self.memory.add_memory(
            "introduction",
            {"role": "craftsman", "content": "我是一名手工艺人"}
        )
        
        self.memory.add_memory(
            "discussion",
            {"role": "craftsman", "topic": "传统工艺", "content": "传统工艺很重要"}
        )
        
        self.memory.add_memory(
            "discussion",
            {"role": "craftsman", "topic": "现代设计", "content": "现代设计也很重要"}
        )
        
        # 获取讨论类型的记忆
        discussion_memories = self.memory.get_memories_by_type("discussion")
        
        # 验证结果
        self.assertEqual(len(discussion_memories), 2)
        for memory in discussion_memories:
            self.assertEqual(memory["type"], "discussion")
    
    def test_get_recent_memories(self):
        """测试获取最近的记忆"""
        # 添加记忆，并控制时间戳
        for i in range(5):
            memory = {
                "type": f"memory_{i}",
                "timestamp": int(time.time()) - (5 - i),  # 越新的记忆时间戳越大
                "content": {"data": f"内容{i}"}
            }
            self.memory.memories.append(memory)
        
        # 获取最近的3条记忆
        recent_memories = self.memory.get_recent_memories(3)
        
        # 验证结果
        self.assertEqual(len(recent_memories), 3)
        self.assertEqual(recent_memories[0]["type"], "memory_4")  # 最新的记忆
        self.assertEqual(recent_memories[1]["type"], "memory_3")
        self.assertEqual(recent_memories[2]["type"], "memory_2")
    
    def test_get_relevant_memories(self):
        """测试获取相关记忆"""
        # 添加记忆
        self.memory.add_memory(
            "introduction",
            {"role": "craftsman", "content": "我是一名手工艺人，专注于传统工艺"}
        )
        
        self.memory.add_memory(
            "discussion",
            {"role": "craftsman", "topic": "传统工艺", "content": "传统工艺在现代社会仍然有重要价值"}
        )
        
        self.memory.add_memory(
            "discussion",
            {"role": "craftsman", "topic": "现代设计", "content": "现代设计可以融合传统元素"}
        )
        
        self.memory.add_memory(
            "keywords",
            {"role": "craftsman", "topic": "传统工艺", "keywords": ["传承", "创新", "价值"]}
        )
        
        # 获取与"传统工艺"相关的记忆
        relevant_memories = self.memory.get_relevant_memories("传统工艺")
        
        # 验证结果
        self.assertTrue(len(relevant_memories) > 0)
        for memory in relevant_memories:
            self.assertIn("传统工艺", memory)
    
    def test_format_memory_as_text(self):
        """测试将记忆格式化为文本"""
        # 测试不同类型的记忆格式化
        memory_types = {
            "introduction": {
                "role": "craftsman",
                "content": "我是一名手工艺人"
            },
            "discussion": {
                "role": "craftsman",
                "topic": "传统工艺",
                "content": "传统工艺很重要"
            },
            "keywords": {
                "role": "craftsman",
                "topic": "传统工艺",
                "keywords": ["传承", "创新", "价值"]
            },
            "voting": {
                "role": "craftsman",
                "topic": "传统工艺",
                "voted_keywords": ["传承", "创新"]
            },
            "role_switch": {
                "previous_role": "craftsman",
                "new_role": "designer"
            },
            "image_story": {
                "role": "craftsman",
                "story": "这是一个关于图片的故事",
                "keywords": ["故事", "图片"]
            },
            "design": {
                "role": "designer",
                "design": "这是一个设计方案",
                "keywords": ["设计", "方案"]
            }
        }
        
        for memory_type, content in memory_types.items():
            memory = {
                "type": memory_type,
                "timestamp": int(time.time()),
                "content": content
            }
            
            # 格式化记忆
            formatted_text = self.memory._format_memory_as_text(memory)
            
            # 验证结果
            self.assertIsInstance(formatted_text, str)
            self.assertTrue(len(formatted_text) > 0)
            
            # 验证特定类型的格式化
            if memory_type == "introduction":
                self.assertIn("自我介绍", formatted_text)
            elif memory_type == "discussion":
                self.assertIn("讨论", formatted_text)
            elif memory_type == "keywords":
                self.assertIn("关键词", formatted_text)
                self.assertIn("传承, 创新, 价值", formatted_text)
            elif memory_type == "voting":
                self.assertIn("投票", formatted_text)
                self.assertIn("传承, 创新", formatted_text)
            elif memory_type == "role_switch":
                self.assertIn("角色转换", formatted_text)
                self.assertIn("craftsman", formatted_text)
                self.assertIn("designer", formatted_text)
            elif memory_type == "image_story":
                self.assertIn("图片故事", formatted_text)
                self.assertIn("故事, 图片", formatted_text)
            elif memory_type == "design":
                self.assertIn("设计方案", formatted_text)
                self.assertIn("设计, 方案", formatted_text)
    
    def test_clear_memories(self):
        """测试清除记忆"""
        # 添加记忆
        self.memory.add_memory(
            "introduction",
            {"role": "craftsman", "content": "我是一名手工艺人"}
        )
        
        self.memory.add_memory(
            "discussion",
            {"role": "craftsman", "topic": "传统工艺", "content": "传统工艺很重要"}
        )
        
        # 验证记忆已添加
        self.assertEqual(len(self.memory.memories), 2)
        memory_files = list(self.memory.memory_dir.glob("*.json"))
        self.assertEqual(len(memory_files), 2)
        
        # 清除记忆
        self.memory.clear_memories()
        
        # 验证记忆已清除
        self.assertEqual(len(self.memory.memories), 0)
        memory_files = list(self.memory.memory_dir.glob("*.json"))
        self.assertEqual(len(memory_files), 0)


if __name__ == "__main__":
    unittest.main()
