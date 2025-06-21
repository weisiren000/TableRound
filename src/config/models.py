#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
模型配置模块
"""

from typing import Dict, List, Any, Optional


class ModelConfig:
    """模型配置类"""

    # 支持的模型提供商
    SUPPORTED_PROVIDERS = {
        "openai": {
            "default_model": "gpt-4o",
            "models": [
                "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo"
            ],
            "vision_models": [
                "gpt-4-turbo", "gpt-4o"
            ]
        },
        "google": {
            "default_model": "gemini-2.5-flash",
            "models": [
                "gemini-2.5-flash", "gemini-2.5-flash-lite-preview-06-17", "gemini-pro"
            ],
            "vision_models": [
                "gemini-2.5-flash", "gemini-2.5-flash-lite-preview-06-17"
            ]
        },
        "anthropic": {
            "default_model": "claude-3-opus-20240229",
            "models": [
                "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
            ],
            "vision_models": [
                "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
            ]
        },
        "deepseek": {
            "default_model": "deepseek-chat-v3-0324",
            "models": [
                "deepseek-chat-v3-0324", "deepseek-r1", "deepseek-vision-v1"
            ],
            "vision_models": [
                "deepseek-vision-v1"
            ]
        },
        "openrouter": {
            "default_model": "meta-llama/llama-4-maverick:free",
            "models": [
                "meta-llama/llama-4-maverick:free",
                "meta-llama/llama-4-scout:free",
                "qwen/qwen3-235b-a22b:free",
                "microsoft/phi-4-reasoning-plus:free",
                "deepseek/deepseek-chat-v3-0324:free",
                "moonshotai/kimi-vl-a3b-thinking:free",
                "deepseek/deepseek-r1-0528:free"
            ],
            "vision_models": [
                "moonshotai/kimi-vl-a3b-thinking:free"
            ],
            "thinking_models": [
                "moonshotai/kimi-vl-a3b-thinking:free"
            ]
        },
        "github": {
            "default_model": "openai/gpt-4.1",
            "models": [
                "openai/gpt-4.1",
                "openai/gpt-4o",
                "deepseek/DeepSeek-V3-0324",
                "openai/gpt-4o-mini",
                "openai/gpt-4.1-mini",
                "openai/gpt-4.1-nano"
            ],
            "vision_models": []
        }
    }

    @staticmethod
    def _get_provider_config(provider: str) -> Optional[Dict[str, Any]]:
        """获取提供商配置（内部使用）"""
        return ModelConfig.SUPPORTED_PROVIDERS.get(provider.lower())

    @staticmethod
    def get_default_model(provider: str) -> str:
        """
        获取默认模型

        Args:
            provider: 提供商

        Returns:
            默认模型名称
        """
        config = ModelConfig._get_provider_config(provider)
        if config:
            return config.get("default_model", "gpt-4")
        return "gpt-4"

    @staticmethod
    def get_models(provider: str) -> List[str]:
        """
        获取提供商支持的模型列表

        Args:
            provider: 提供商

        Returns:
            模型列表
        """
        config = ModelConfig._get_provider_config(provider)
        return config.get("models", []) if config else []

    @staticmethod
    def get_vision_models(provider: str) -> List[str]:
        """
        获取提供商支持的视觉模型列表

        Args:
            provider: 提供商

        Returns:
            视觉模型列表
        """
        config = ModelConfig._get_provider_config(provider)
        return config.get("vision_models", []) if config else []

    @staticmethod
    def supports_vision(provider: str, model_name: str) -> bool:
        """
        检查模型是否支持视觉

        Args:
            provider: 提供商
            model_name: 模型名称

        Returns:
            是否支持视觉
        """
        vision_models = ModelConfig.get_vision_models(provider)
        return model_name in vision_models

    @staticmethod
    def supports_thinking(provider: str, model_name: str) -> bool:
        """
        检查模型是否支持思维模型

        Args:
            provider: 提供商
            model_name: 模型名称

        Returns:
            是否支持思维模型
        """
        config = ModelConfig._get_provider_config(provider)
        if config:
            thinking_models = config.get("thinking_models", [])
            return model_name in thinking_models
        return False
