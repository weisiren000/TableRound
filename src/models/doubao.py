#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
豆包API模型接口模块
"""

import base64
import logging
import os
import json
import time
from typing import Optional, Dict, Any, List, AsyncGenerator

import aiohttp
import requests

from src.models.base import BaseModel


class DoubaoModel(BaseModel):
    """豆包API模型接口"""

    def __init__(
        self,
        model_name: str = "doubao-seedream-3-0-t2i-250415",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        """
        初始化豆包模型

        Args:
            model_name: 模型名称
            api_key: API密钥
            base_url: API基础URL
            **kwargs: 其他参数
        """
        super().__init__(model_name, **kwargs)

        # 设置API密钥
        self.api_key = api_key or os.environ.get("DOUBAO_API_KEY")
        if not self.api_key:
            raise ValueError("豆包API密钥未提供")

        # 设置API基础URL
        self.base_url = base_url or os.environ.get("DOUBAO_BASE_URL") or "https://ark.cn-beijing.volces.com/api/v3"

        # 设置默认参数
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 2000)

        # 检查是否支持图像生成
        self.image_generation_supported = "seedream" in model_name.lower() or model_name in [
            "doubao-seedream-3.0-t2i", "doubao-seedream-3-0-t2i-250415"
        ]

        # 如果是图像生成模型，确保使用正确的模型名称
        if self.image_generation_supported and model_name == "doubao-seedream-3-0-t2i-250415":
            self.model_name = "doubao-seedream-3.0-t2i"

        # 检查是否支持图像理解
        self.vision_supported = "vision" in model_name.lower() or model_name in [
            "doubao-1.5-vision-pro", "doubao-1.5-vision-lite"
        ]

        self.logger = logging.getLogger(f"model.doubao.{model_name}")

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
            # 构建消息
            messages = []

            # 添加系统提示词
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # 添加用户提示词
            messages.append({"role": "user", "content": prompt})

            # 构建请求数据
            data = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }

            # 构建URL
            url = f"{self.base_url.rstrip('/')}/chat/completions"

            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"API请求失败: {response.status}, {error_text}")
                        return f"生成失败: API请求返回 {response.status}"

                    result = await response.json()

                    # 获取生成的文本
                    return result["choices"][0]["message"]["content"]

        except Exception as e:
            self.logger.error(f"生成文本失败: {str(e)}")
            return f"生成失败: {str(e)}"

    async def generate_stream(self, prompt: str, system_prompt: str = "") -> AsyncGenerator[str, None]:
        """
        流式生成文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词

        Yields:
            生成的文本片段
        """
        try:
            # 构建消息
            messages = []

            # 添加系统提示词
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # 添加用户提示词
            messages.append({"role": "user", "content": prompt})

            # 构建请求数据
            data = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": True
            }

            # 构建URL
            url = f"{self.base_url.rstrip('/')}/chat/completions"

            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"API请求失败: {response.status}, {error_text}")
                        yield f"生成失败: API请求返回 {response.status}"
                        return

                    # 处理流式响应
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if line.startswith('data: ') and line != 'data: [DONE]':
                            data = json.loads(line[6:])
                            content = data["choices"][0]["delta"].get("content", "")
                            if content:
                                yield content

        except Exception as e:
            self.logger.error(f"流式生成文本失败: {str(e)}")
            yield f"生成失败: {str(e)}"

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
        if not self.supports_vision():
            return "该模型不支持图像处理"

        try:
            # 读取图像
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            # 构建消息
            messages = []

            # 添加系统提示词
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # 添加用户提示词和图像
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            })

            # 构建请求数据
            data = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }

            # 构建URL
            url = f"{self.base_url.rstrip('/')}/chat/completions"

            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"API请求失败: {response.status}, {error_text}")
                        return f"生成失败: API请求返回 {response.status}"

                    result = await response.json()

                    # 获取生成的文本
                    return result["choices"][0]["message"]["content"]

        except Exception as e:
            self.logger.error(f"基于图像生成文本失败: {str(e)}")
            return f"生成失败: {str(e)}"

    async def generate_image(self, prompt: str, size: str = "1024x1024", n: int = 1, watermark: bool = False) -> List[str]:
        """
        生成图像

        Args:
            prompt: 提示词
            size: 图像尺寸
            n: 生成图像数量
            watermark: 是否包含水印，默认为False

        Returns:
            生成的图像URL列表
        """
        if not self.supports_image_generation():
            return ["该模型不支持图像生成"]

        try:
            # 构建请求数据
            data = {
                "model": "doubao-seedream-3-0-t2i-250415",  # 使用官方文档中的模型ID
                "prompt": prompt,
                "size": size,
                "n": n,
                "watermark": watermark
            }

            # 构建URL
            url = f"{self.base_url.rstrip('/')}/images/generations"

            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"API请求失败: {response.status}, {error_text}")
                        return [f"生成失败: API请求返回 {response.status}"]

                    result = await response.json()

                    # 获取生成的图像URL
                    return [item["url"] for item in result["data"]]

        except Exception as e:
            self.logger.error(f"生成图像失败: {str(e)}")
            return [f"生成失败: {str(e)}"]

    def supports_vision(self) -> bool:
        """
        是否支持视觉

        Returns:
            是否支持视觉
        """
        return self.vision_supported

    def supports_image_generation(self) -> bool:
        """
        是否支持图像生成

        Returns:
            是否支持图像生成
        """
        return self.image_generation_supported
