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
import json
import time
import re
import importlib
from datetime import datetime, timedelta
from collections import deque

import requests

# 确保aiohttp可用
try:
    import aiohttp
except ImportError:
    aiohttp = None

from src.models.base import BaseModel

# 速率限制器类
class RateLimiter:
    """速率限制器，控制API请求频率"""
    
    def __init__(self, rpm_limit: int = 15, tpm_limit: int = 250000):
        """
        初始化速率限制器
        
        Args:
            rpm_limit: 每分钟请求数限制
            tpm_limit: 每分钟令牌数限制
        """
        self.rpm_limit = rpm_limit
        self.tpm_limit = tpm_limit
        
        # 请求时间窗口（保存最近1分钟的请求时间）
        self.request_times = deque(maxlen=rpm_limit)
        
        # 令牌使用窗口（保存最近1分钟的令牌使用量）
        self.token_usage = deque(maxlen=100)  # 最多记录100条令牌使用记录
        
        # 日志
        self.logger = logging.getLogger("rate_limiter")
    
    async def wait_if_needed(self, estimated_tokens: int = 1000) -> None:
        """
        检查是否需要等待以遵守速率限制
        
        Args:
            estimated_tokens: 估计的令牌使用量
        """
        # 清理过期记录（1分钟前的）
        current_time = datetime.now()
        one_minute_ago = current_time - timedelta(minutes=1)
        
        # 清理过期的请求时间记录
        while self.request_times and self.request_times[0] < one_minute_ago:
            self.request_times.popleft()
        
        # 清理过期的令牌使用记录
        while self.token_usage and self.token_usage[0]["time"] < one_minute_ago:
            self.token_usage.popleft()
        
        # 计算当前请求数和令牌使用量
        current_rpm = len(self.request_times)
        current_tpm = sum(item["tokens"] for item in self.token_usage)
        
        # 检查是否超出限制
        if current_rpm >= self.rpm_limit or current_tpm + estimated_tokens > self.tpm_limit:
            # 计算需要等待的时间
            if current_rpm > 0:
                # 等待最早的请求过期
                wait_seconds = (self.request_times[0] - one_minute_ago).total_seconds()
                wait_seconds = max(0, wait_seconds)
                
                self.logger.warning(f"达到速率限制 (RPM: {current_rpm}/{self.rpm_limit}, TPM: {current_tpm}/{self.tpm_limit})，等待 {wait_seconds:.2f} 秒")
                await asyncio.sleep(wait_seconds)
                
                # 递归检查，确保等待后仍然符合限制
                return await self.wait_if_needed(estimated_tokens)
        
        # 记录本次请求
        self.request_times.append(current_time)
        self.token_usage.append({
            "time": current_time,
            "tokens": estimated_tokens
        })
    
    def update_token_usage(self, actual_tokens: int) -> None:
        """
        更新实际的令牌使用量
        
        Args:
            actual_tokens: 实际使用的令牌数
        """
        if self.token_usage:
            # 更新最近一次请求的令牌使用量
            self.token_usage[-1]["tokens"] = actual_tokens


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
        self.api_base = base_url or os.environ.get("GOOGLE_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
        
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
        
        # 创建速率限制器
        # 根据模型设置不同的速率限制
        if "flash-lite-preview" in model_name.lower():
            self.rate_limiter = RateLimiter(rpm_limit=15, tpm_limit=250000)
        else:
            # 默认使用Gemini 2.5 Flash的限制
            self.rate_limiter = RateLimiter(rpm_limit=10, tpm_limit=250000)

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
            # 估计令牌数量（简单估计，每4个字符约1个令牌）
            estimated_tokens = (len(prompt) + len(system_prompt)) // 4
            
            # 应用速率限制
            await self.rate_limiter.wait_if_needed(estimated_tokens)
            
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
            url = f"{self.api_base.rstrip('/')}/chat/completions"

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
                        # 更新实际的令牌使用量
                        if "usage" in result:
                            total_tokens = result["usage"].get("total_tokens", estimated_tokens)
                            self.rate_limiter.update_token_usage(total_tokens)
                        
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
        self.logger.info(f"正在发送请求到: {self.api_base}")
        
        # 检查aiohttp是否可用
        if aiohttp is None:
            try:
                globals()['aiohttp'] = importlib.import_module('aiohttp')
                self.logger.info("成功导入aiohttp库")
            except ImportError as e:
                self.logger.error(f"无法导入aiohttp库: {str(e)}")
                raise ImportError("无法导入aiohttp库，请使用 'pip install aiohttp' 安装")
        
        # 估计令牌数量（图像请求通常消耗更多令牌）
        estimated_tokens = (len(prompt) + len(system_prompt)) // 4 + 1000  # 图像额外添加1000令牌估计
        
        # 应用速率限制
        await self.rate_limiter.wait_if_needed(estimated_tokens)
        
        # 设置超时和重试参数
        max_retries = 3
        timeout = aiohttp.ClientTimeout(total=30, connect=10, sock_read=20)
        
        for attempt in range(max_retries):
            try:
                # 读取图片并编码为base64
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode("utf-8")
                
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
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                })
                
                # 构建请求数据
                data = {
                    "model": self.model_name,
                    "messages": messages,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature
                }
                
                # 使用同步requests库，在异步函数中运行（避免aiohttp的潜在问题）
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        requests.post,
                        f"{self.api_base.rstrip('/')}/chat/completions",
                        json=data,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {self.api_key}"
                        },
                        timeout=30
                    )
                    
                    # 添加超时处理
                    try:
                        response = future.result()
                    except concurrent.futures.TimeoutError:
                        if attempt < max_retries - 1:
                            self.logger.warning(f"请求超时，正在重试... (尝试 {attempt + 1}/{max_retries})")
                            await asyncio.sleep(5)
                            continue
                        return "生成失败: 请求超时"
                
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
                
                # 更新实际的令牌使用量
                if "usage" in result:
                    total_tokens = result["usage"].get("total_tokens", estimated_tokens)
                    self.rate_limiter.update_token_usage(total_tokens)
                
                # 提取生成的文本
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    self.logger.error(f"无效的API响应: {result}")
                    return f"无效的API响应: {result}"
            
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    self.logger.warning(f"请求超时，正在重试... (尝试 {attempt + 1}/{max_retries})")
                    await asyncio.sleep(5)
                    continue
                return "生成失败: 请求超时"
            except Exception as e:
                self.logger.error(f"基于图像生成文本失败: {str(e)}")
                if attempt < max_retries - 1:
                    self.logger.warning(f"请求失败: {e}，正在重试... (尝试 {attempt + 1}/{max_retries})")
                    await asyncio.sleep(2)
                    continue
                return f"生成失败: {str(e)}"
        
        # 如果所有重试都失败
        return "生成失败: 多次尝试后仍无法获取响应"

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
