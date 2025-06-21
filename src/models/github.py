#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Github AI模型接口模块
"""

import base64
import logging
import os
from typing import Optional, Callable
from openai import OpenAI
from src.models.base import BaseModel

class GithubModel(BaseModel):
    """Github AI模型接口（兼容 openai SDK）"""

    def __init__(
        self,
        model_name: str = "openai/gpt-4.1",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        super().__init__(model_name, **kwargs)
        self.api_key = api_key or os.environ.get("GITHUB_API_KEY") or os.environ.get("GITHUB_TOKEN")
        if not self.api_key:
            raise ValueError("Github AI API密钥未提供（GITHUB_API_KEY 或 GITHUB_TOKEN）")
        self.base_url = base_url or os.environ.get("GITHUB_BASE_URL") or "https://models.github.ai/inference"
        self.temperature = kwargs.get("temperature", 1.0)
        self.max_tokens = kwargs.get("max_tokens", 2000)
        self.logger = logging.getLogger(f"model.github.{model_name}")
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            # openai SDK 不支持异步，需线程池包装
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    messages=messages,
                    temperature=self.temperature,
                    top_p=1.0,
                    model=self.model_name
                )
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"生成文本失败: {str(e)}")
            return f"生成失败: {str(e)}"

    async def generate_with_image(self, prompt: str, system_prompt: str, image_path: str) -> str:
        # Github AI 暂不支持 vision，直接报错
        return "该模型暂不支持图像输入"

    async def generate_stream(self, prompt: str, system_prompt: str = "", callback: Callable[[str], None] = None) -> str:
        # Github AI 暂不支持流式，直接用普通生成
        return await self.generate(prompt, system_prompt)

    def supports_vision(self) -> bool:
        return False 