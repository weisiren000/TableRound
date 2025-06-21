#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
全局设置模块
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

from src.config.models import ModelConfig


class Settings:
    """全局设置类"""

    def __init__(self, env_file: str = ".env"):
        """
        初始化全局设置

        Args:
            env_file: 环境变量文件路径
        """
        # 加载环境变量
        load_dotenv(env_file)

        # 项目根目录
        self.ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        # 数据目录
        self.DATA_DIR = os.path.join(self.ROOT_DIR, "data")
        os.makedirs(self.DATA_DIR, exist_ok=True)

        # 记忆目录
        self.MEMORY_DIR = os.path.join(self.DATA_DIR, "memories")
        os.makedirs(self.MEMORY_DIR, exist_ok=True)

        # 图片目录
        self.IMAGE_DIR = os.path.join(self.DATA_DIR, "images")
        os.makedirs(self.IMAGE_DIR, exist_ok=True)

        # 关键词目录
        self.KEYWORD_DIR = os.path.join(self.DATA_DIR, "keywords")
        os.makedirs(self.KEYWORD_DIR, exist_ok=True)

        # 日志目录
        self.LOG_DIR = os.path.join(self.ROOT_DIR, "logs")
        os.makedirs(self.LOG_DIR, exist_ok=True)

        # AI模型设置
        self.provider = os.getenv("AI_PROVIDER", "openai")
        self.model_config = ModelConfig()
        self.model = os.getenv("AI_MODEL", self.model_config.get_default_model(self.provider))

        # 记忆设置
        self.memory_storage_type = os.getenv("MEMORY_STORAGE_TYPE", "memory")
        self.memory_max_tokens = int(os.getenv("MEMORY_MAX_TOKENS", "4000"))

        # 投票设置
        self.voting_threshold = float(os.getenv("VOTING_THRESHOLD", "0.6"))

        # 智能体设置
        self.agent_counts = {
            "craftsman": int(os.getenv("CRAFTSMAN_COUNT", "1")),
            "consumer": int(os.getenv("CONSUMER_COUNT", "1")),
            "manufacturer": int(os.getenv("MANUFACTURER_COUNT", "1")),
            "designer": int(os.getenv("DESIGNER_COUNT", "1"))
        }

        # 对话设置
        self.max_turns = int(os.getenv("MAX_TURNS", "10"))
        self.max_keywords = int(os.getenv("MAX_KEYWORDS", "10"))

        # 日志设置
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_to_file = os.getenv("LOG_TO_FILE", "true").lower() == "true"

        # API设置
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))

        # 其他设置
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

    def get_api_key(self, provider: str) -> Optional[str]:
        """
        获取API密钥

        Args:
            provider: 提供商

        Returns:
            API密钥
        """
        provider = provider.upper()
        return os.getenv(f"{provider}_API_KEY")

    def get_base_url(self, provider: str) -> Optional[str]:
        """
        获取API基础URL

        Args:
            provider: 提供商

        Returns:
            API基础URL
        """
        provider = provider.upper()
        return os.getenv(f"{provider}_BASE_URL")

    def get_model_instance(self, provider: Optional[str] = None, model_name: Optional[str] = None) -> Any:
        """
        获取模型实例

        Args:
            provider: 提供商，默认使用配置中的提供商
            model_name: 模型名称，默认使用配置中的模型名称

        Returns:
            模型实例
        """
        provider = provider or self.provider
        model_name = model_name or self.model

        # 获取API密钥
        api_key = self.get_api_key(provider)
        if not api_key:
            raise ValueError(f"未找到 {provider} 的API密钥")

        # 获取API基础URL
        base_url = self.get_base_url(provider)

        # 根据提供商创建不同的模型实例
        if provider.lower() == "openai":
            from src.models import OpenAIModel
            return OpenAIModel(model_name=model_name, api_key=api_key, base_url=base_url)

        elif provider.lower() == "google":
            from src.models import GoogleModel
            return GoogleModel(model_name=model_name, api_key=api_key, base_url=base_url)

        elif provider.lower() == "doubao":
            from src.models import DoubaoModel
            return DoubaoModel(model_name=model_name, api_key=api_key, base_url=base_url)

        elif provider.lower() == "anthropic":
            from src.models import AnthropicModel
            return AnthropicModel(model_name=model_name, api_key=api_key, base_url=base_url)

        elif provider.lower() == "deepseek":
            from src.models import DeepSeekModel
            return DeepSeekModel(model_name=model_name, api_key=api_key, base_url=base_url)

        elif provider.lower() == "openrouter":
            from src.models import OpenRouterModel
            return OpenRouterModel(model_name=model_name, api_key=api_key, base_url=base_url)

        else:
            raise ValueError(f"不支持的提供商: {provider}")

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典

        Returns:
            设置字典
        """
        return {
            "provider": self.provider,
            "model": self.model,
            "memory_storage_type": self.memory_storage_type,
            "memory_max_tokens": self.memory_max_tokens,
            "agent_counts": self.agent_counts,
            "max_turns": self.max_turns,
            "max_keywords": self.max_keywords,
            "voting_threshold": self.voting_threshold,
            "log_level": self.log_level,
            "log_to_file": self.log_to_file,
            "api_host": self.api_host,
            "api_port": self.api_port,
            "debug": self.debug
        }

    def save(self, file_path: str) -> None:
        """
        保存设置到文件

        Args:
            file_path: 文件路径
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, file_path: str) -> "Settings":
        """
        从文件加载设置

        Args:
            file_path: 文件路径

        Returns:
            设置对象
        """
        settings = cls()

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                for key, value in data.items():
                    if hasattr(settings, key):
                        setattr(settings, key, value)

        return settings
