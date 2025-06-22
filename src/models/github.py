#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Github AI模型接口模块
"""

import base64
import logging
import os
import asyncio
import aiohttp
import json
from typing import Optional, Callable
from src.models.base import BaseModel

class GithubModel(BaseModel):
    """Github AI模型接口（使用异步HTTP客户端）"""

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

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        生成文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词

        Returns:
            生成的文本
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            # 构建请求数据
            data = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": 1.0
            }

            # 构建URL
            url = f"{self.base_url.rstrip('/')}/chat/completions"

            # 发送请求，带重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url,
                            json=data,
                            headers={
                                "Content-Type": "application/json",
                                "Authorization": f"Bearer {self.api_key}",
                                "User-Agent": "TableRound/1.0"
                            },
                            timeout=aiohttp.ClientTimeout(total=60)  # 60秒超时
                        ) as response:
                            if response.status == 429:  # 速率限制
                                if attempt < max_retries - 1:
                                    wait_time = (attempt + 1) * 5  # 递增等待时间
                                    self.logger.warning(f"遇到速率限制，等待{wait_time}秒后重试...")
                                    await asyncio.sleep(wait_time)
                                    continue
                                else:
                                    return "生成失败: 超出API速率限制，请稍后再试"

                            if response.status != 200:
                                error_text = await response.text()
                                self.logger.error(f"API请求失败: {response.status}, {error_text}")
                                if attempt < max_retries - 1:
                                    await asyncio.sleep(2)  # 等待2秒后重试
                                    continue
                                else:
                                    return f"生成失败: API请求返回 {response.status}"

                            result = await response.json()

                            # 获取生成的文本
                            if "choices" in result and len(result["choices"]) > 0:
                                content = result["choices"][0]["message"]["content"]
                                return content
                            else:
                                return "生成失败: 响应格式错误"

                except asyncio.TimeoutError:
                    self.logger.warning(f"请求超时，尝试重试 ({attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2)
                        continue
                    else:
                        return "生成失败: 请求超时"
                except Exception as e:
                    self.logger.error(f"请求异常: {str(e)}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2)
                        continue
                    else:
                        return f"生成失败: {str(e)}"

            return "生成失败: 所有重试都失败了"

        except Exception as e:
            self.logger.error(f"生成文本失败: {str(e)}")
            return f"生成失败: {str(e)}"

    async def generate_with_image(self, prompt: str, system_prompt: str, image_path: str) -> str:
        """
        基于图像生成文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词
            image_path: 图像路径

        Returns:
            生成的文本
        """
        # Github AI 暂不支持 vision
        return "该模型暂不支持图像输入"

    async def generate_stream(self, prompt: str, system_prompt: str = "", callback: Callable[[str], None] = None) -> str:
        """
        流式生成文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词
            callback: 回调函数，用于处理流式输出

        Returns:
            生成的完整文本
        """
        # Github AI 暂不支持流式，直接用普通生成
        result = await self.generate(prompt, system_prompt)
        if callback:
            callback(result)
        return result

    def supports_vision(self) -> bool:
        """
        是否支持图像处理

        Returns:
            是否支持图像处理
        """
        return False