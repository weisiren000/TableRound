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
            "default_model": "gpt-4",
            "models": [
                "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo"
            ],
            "vision_models": [
                "gpt-4-vision-preview", "gpt-4-turbo", "gpt-4o"
            ]
        },
        "google": {
            "default_model": "gemini-2.5-flash-preview-04-17",
            "models": [
                "gemini-2.5-flash-preview-04-17", "gemini-pro", "gemini-pro-vision"
            ],
            "vision_models": [
                "gemini-pro-vision", "gemini-2.5-flash-preview-04-17"
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
        }
    }

    @staticmethod
    def get_default_model(provider: str) -> str:
        """
        获取默认模型

        Args:
            provider: 提供商

        Returns:
            默认模型名称
        """
        provider = provider.lower()
        if provider in ModelConfig.SUPPORTED_PROVIDERS:
            return ModelConfig.SUPPORTED_PROVIDERS[provider]["default_model"]
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
        provider = provider.lower()
        if provider in ModelConfig.SUPPORTED_PROVIDERS:
            return ModelConfig.SUPPORTED_PROVIDERS[provider]["models"]
        return []

    @staticmethod
    def get_vision_models(provider: str) -> List[str]:
        """
        获取提供商支持的视觉模型列表

        Args:
            provider: 提供商

        Returns:
            视觉模型列表
        """
        provider = provider.lower()
        if provider in ModelConfig.SUPPORTED_PROVIDERS:
            return ModelConfig.SUPPORTED_PROVIDERS[provider].get("vision_models", [])
        return []

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
        provider = provider.lower()
        if provider in ModelConfig.SUPPORTED_PROVIDERS:
            vision_models = ModelConfig.SUPPORTED_PROVIDERS[provider].get("vision_models", [])
            return model_name in vision_models
        return False

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
        provider = provider.lower()
        if provider in ModelConfig.SUPPORTED_PROVIDERS:
            thinking_models = ModelConfig.SUPPORTED_PROVIDERS[provider].get("thinking_models", [])
            return model_name in thinking_models
        return False
