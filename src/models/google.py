#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Google模型接口模块
"""

import base64
import logging
import os
import asyncio
from typing import Optional, Dict, Any, List, Callable

import requests

from src.models.base import BaseModel

# 移除新SDK的导入，只使用传统API调用


class GoogleModel(BaseModel):
    """Google模型接口"""

    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        """
        初始化Google模型

        Args:
            model_name: 模型名称
            api_key: API密钥
            base_url: API基础URL
            **kwargs: 其他参数
        """
        super().__init__(model_name, **kwargs)
        
        # 设置API密钥
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API密钥未提供")
        
        # 设置API基础URL
        self.base_url = base_url or os.environ.get("GOOGLE_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
        
        # 设置默认参数
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 2000)
        
        # 检查是否支持图像
        self.vision_supported = (
            "vision" in model_name.lower() or
            "gemini" in model_name.lower() or  # Gemini系列模型都支持视觉
            model_name in [
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite-preview-06-17",
                "gemini-pro-vision"
            ]
        )
        
        self.logger = logging.getLogger(f"model.google.{model_name}")

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

            # 添加系统提示词
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # 添加用户提示词
            messages.append({"role": "user", "content": prompt})

            # 构建请求数据 - 使用OpenAI兼容格式
            data = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }

            # 构建URL - 使用OpenAI兼容端点
            url = f"{self.base_url.rstrip('/')}/chat/completions"

            # 构建请求头
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            # 发送请求，带重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.logger.info(f"正在发送请求到: {url}")

                    # 使用同步requests库，在异步函数中运行
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(
                            requests.post,
                            url,
                            json=data,
                            headers=headers,
                            timeout=30
                        )
                        response = future.result()

                    if response.status_code == 429:  # 速率限制
                        if attempt < max_retries - 1:
                            wait_time = (attempt + 1) * 5  # 递增等待时间
                            self.logger.warning(f"遇到速率限制，等待{wait_time}秒后重试...")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            return "生成失败: 超出API速率限制，请稍后再试"

                    if response.status_code != 200:
                        error_text = response.text
                        self.logger.error(f"API请求失败: {response.status_code}, {error_text}")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(2)  # 短暂等待后重试
                            continue
                        return f"生成失败: API请求返回 {response.status_code}"

                    result = response.json()

                    # 获取生成的文本 - OpenAI格式
                    if "choices" in result and result["choices"]:
                        return result["choices"][0]["message"]["content"]

                    return "生成失败: 无法解析响应"

                except requests.exceptions.Timeout:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"请求超时，正在重试... (尝试 {attempt + 1}/{max_retries})")
                        await asyncio.sleep(5)
                        continue
                    return "生成失败: 请求超时"
                except Exception as e:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"请求失败: {e}，正在重试... (尝试 {attempt + 1}/{max_retries})")
                        await asyncio.sleep(2)
                        continue
                    raise e

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
        if not self.supports_vision():
            return "该模型不支持图像处理"

        try:
            # 读取图像
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            # 构建请求数据 - 使用Google Gemini API格式
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_prompt}\n\n{prompt}" if system_prompt else prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": base64_image
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": self.temperature,
                    "maxOutputTokens": 2048  # 增加token限制以避免思考过程中用完
                }
            }

            # 构建URL - 使用正确的Google Gemini API端点
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

            # 发送请求，带重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # 创建连接器，设置更宽松的超时
                    connector = aiohttp.TCPConnector(
                        limit=100,
                        limit_per_host=30,
                        ttl_dns_cache=300,
                        use_dns_cache=True,
                    )

                    timeout = aiohttp.ClientTimeout(
                        total=120,  # 总超时时间120秒
                        connect=30,  # 连接超时30秒
                        sock_read=60  # 读取超时60秒
                    )

                    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                        self.logger.info(f"正在发送图像请求到: {url}")
                        async with session.post(
                            url,
                            json=data,
                            headers={
                                "Content-Type": "application/json"
                            },
                            params={
                                "key": self.api_key
                            } if self.api_key else None
                        ) as response:
                            if response.status == 429:  # 速率限制
                                if attempt < max_retries - 1:
                                    wait_time = (attempt + 1) * 10  # 递增等待时间
                                    self.logger.warning(f"遇到速率限制，等待{wait_time}秒后重试...")
                                    await asyncio.sleep(wait_time)
                                    continue
                                else:
                                    return "生成失败: 超出API速率限制，请稍后再试"

                            if response.status != 200:
                                error_text = await response.text()
                                self.logger.error(f"API请求失败: {response.status}, {error_text}")
                                if attempt < max_retries - 1:
                                    await asyncio.sleep(2)  # 短暂等待后重试
                                    continue
                                return f"生成失败: API请求返回 {response.status}"

                            result = await response.json()

                            # 获取生成的文本
                            if "candidates" in result and result["candidates"]:
                                candidate = result["candidates"][0]
                                if "content" in candidate and "parts" in candidate["content"]:
                                    parts = candidate["content"]["parts"]
                                    if parts and "text" in parts[0]:
                                        return parts[0]["text"]

                                # 检查是否因为token限制而失败
                                if candidate.get("finishReason") == "MAX_TOKENS":
                                    return "生成失败: 响应被截断（达到最大token限制）"

                            return "生成失败: 无法解析响应"

                except asyncio.TimeoutError:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"请求超时，正在重试... (尝试 {attempt + 1}/{max_retries})")
                        await asyncio.sleep(5)
                        continue
                    return "生成失败: 请求超时"
                except Exception as e:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"请求失败: {e}，正在重试... (尝试 {attempt + 1}/{max_retries})")
                        await asyncio.sleep(2)
                        continue
                    raise e

        except Exception as e:
            self.logger.error(f"基于图像生成文本失败: {str(e)}")
            return f"生成失败: {str(e)}"



    async def generate_stream(
        self,
        prompt: str,
        system_prompt: str = "",
        callback: Optional[Callable[[str], None]] = None
    ) -> str:
        """
        流式生成文本 - 注意：Google Gemini API不支持流式输出，这里使用普通生成然后模拟流式输出

        Args:
            prompt: 提示词
            system_prompt: 系统提示词
            callback: 回调函数，用于处理流式输出

        Returns:
            生成的完整文本
        """
        try:
            # Google Gemini API不支持流式输出，使用普通生成
            result = await self.generate(prompt, system_prompt)

            # 如果有回调函数，模拟流式输出
            if callback and result:
                # 将结果分块输出，模拟流式效果
                chunk_size = 10  # 每次输出10个字符
                for i in range(0, len(result), chunk_size):
                    chunk = result[i:i+chunk_size]
                    callback(chunk)
                    await asyncio.sleep(0.05)  # 短暂延迟模拟流式效果

            return result

        except Exception as e:
            self.logger.error(f"流式生成文本失败: {str(e)}")
            error_message = f"生成失败: {str(e)}"
            if callback:
                callback(error_message)
            return error_message

    def supports_vision(self) -> bool:
        """
        是否支持图像处理

        Returns:
            是否支持图像处理
        """
        return self.vision_supported
