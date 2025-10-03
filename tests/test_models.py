#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
模型接口测试
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

from src.models.openai import OpenAIModel
from src.models.google import GoogleModel
from src.models.anthropic import AnthropicModel
from src.models.deepseek import DeepSeekModel
from src.models.openrouter import OpenRouterModel


# 加载环境变量
load_dotenv()


class TestModels(unittest.TestCase):
    """模型接口测试类"""

    def setUp(self):
        """测试前准备"""
        # 获取API密钥
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        # 测试提示词
        self.test_prompt = "你好，请简单介绍一下自己。"
        self.test_system_prompt = "你是一个友好的助手。"

    def test_openai_model(self):
        """测试OpenAI模型"""
        if not self.openai_api_key:
            self.skipTest("缺少OpenAI API密钥")

        # 创建模型
        model = OpenAIModel(
            model_name="gpt-3.5-turbo",
            api_key=self.openai_api_key
        )

        # 测试生成文本
        response = asyncio.run(model.generate(
            prompt=self.test_prompt,
            system_prompt=self.test_system_prompt
        ))

        # 验证响应
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        print(f"OpenAI响应: {response[:100]}...")

    def test_google_model(self):
        """测试Google模型"""
        if not self.google_api_key:
            self.skipTest("缺少Google API密钥")

        # 创建模型
        model = GoogleModel(
            model_name="gemini-2.5-flash-preview-04-17",
            api_key=self.google_api_key
        )

        # 测试生成文本
        response = asyncio.run(model.generate(
            prompt=self.test_prompt,
            system_prompt=self.test_system_prompt
        ))

        # 验证响应
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        print(f"Google响应: {response[:100]}...")

        # 关闭客户端
        asyncio.run(model.close())

    def test_anthropic_model(self):
        """测试Anthropic模型"""
        if not self.anthropic_api_key:
            self.skipTest("缺少Anthropic API密钥")

        # 创建模型
        model = AnthropicModel(
            model_name="claude-3-haiku-20240307",
            api_key=self.anthropic_api_key
        )

        # 测试生成文本
        response = asyncio.run(model.generate(
            prompt=self.test_prompt,
            system_prompt=self.test_system_prompt
        ))

        # 验证响应
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        print(f"Anthropic响应: {response[:100]}...")

    def test_deepseek_model(self):
        """测试DeepSeek模型"""
        if not self.deepseek_api_key:
            self.skipTest("缺少DeepSeek API密钥")

        # 创建模型
        model = DeepSeekModel(
            model_name="deepseek-chat",
            api_key=self.deepseek_api_key
        )

        # 测试生成文本
        response = asyncio.run(model.generate(
            prompt=self.test_prompt,
            system_prompt=self.test_system_prompt
        ))

        # 验证响应
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        print(f"DeepSeek响应: {response[:100]}...")

    def test_openrouter_model(self):
        """测试OpenRouter模型"""
        if not self.openrouter_api_key:
            self.skipTest("缺少OpenRouter API密钥")

        # 创建模型
        model = OpenRouterModel(
            model_name="meta-llama/llama-4-scout:free",
            api_key=self.openrouter_api_key
        )

        # 测试生成文本
        response = asyncio.run(model.generate(
            prompt=self.test_prompt,
            system_prompt=self.test_system_prompt
        ))

        # 验证响应
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        print(f"OpenRouter响应: {response[:100]}...")


if __name__ == "__main__":
    unittest.main()
