#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Anthropic模型接口模块
"""

import base64
import logging
import os
from typing import Optional, Dict, Any, List, Callable

import aiohttp

from src.models.base import BaseModel


class AnthropicModel(BaseModel):
    """Anthropic模型接口"""

    def __init__(
        self,
        model_name: str = "claude-3-opus-20240229",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        """
        初始化Anthropic模型

        Args:
            model_name: 模型名称
            api_key: API密钥
            base_url: API基础URL
            **kwargs: 其他参数
        """
        super().__init__(model_name, **kwargs)
        
        # 设置API密钥
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API密钥未提供")
        
        # 设置API基础URL
        self.base_url = base_url or os.environ.get("ANTHROPIC_BASE_URL") or "https://api.anthropic.com/v1"
        
        # 设置默认参数
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 2000)
        
        # 检查是否支持图像
        self.vision_supported = "vision" in model_name.lower() or model_name in [
            "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
        ]
        
        self.logger = logging.getLogger(f"model.anthropic.{model_name}")

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
            messages = [{"role": "user", "content": prompt}]
            
            # 构建请求数据
            data = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            # 添加系统提示词
            if system_prompt:
                data["system"] = system_prompt
            
            # 构建URL
            url = f"{self.base_url.rstrip('/')}/messages"
            
            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=data,
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"API请求失败: {response.status}, {error_text}")
                        return f"生成失败: API请求返回 {response.status}"
                    
                    result = await response.json()
                    
                    # 获取生成的文本
                    return result["content"][0]["text"]
        
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
            
            # 构建消息
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ]
            
            # 构建请求数据
            data = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            # 添加系统提示词
            if system_prompt:
                data["system"] = system_prompt
            
            # 构建URL
            url = f"{self.base_url.rstrip('/')}/messages"
            
            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=data,
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"API请求失败: {response.status}, {error_text}")
                        return f"生成失败: API请求返回 {response.status}"
                    
                    result = await response.json()
                    
                    # 获取生成的文本
                    return result["content"][0]["text"]
        
        except Exception as e:
            self.logger.error(f"基于图像生成文本失败: {str(e)}")
            return f"生成失败: {str(e)}"

    async def generate_stream(
        self, 
        prompt: str, 
        system_prompt: str = "", 
        callback: Callable[[str], None] = None
    ) -> str:
        """
        流式生成文本

        Args:
            prompt: 提示词
            system_prompt: 系统提示词
            callback: 回调函数，用于处理流式输出

        Returns:
            生成的完整文本
        """
        try:
            # 构建消息
            messages = [{"role": "user", "content": prompt}]
            
            # 构建请求数据
            data = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "stream": True
            }
            
            # 添加系统提示词
            if system_prompt:
                data["system"] = system_prompt
            
            # 构建URL
            url = f"{self.base_url.rstrip('/')}/messages"
            
            # 发送请求
            full_text = ""
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=data,
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"API请求失败: {response.status}, {error_text}")
                        error_message = f"生成失败: API请求返回 {response.status}"
                        if callback:
                            callback(error_message)
                        return error_message
                    
                    # 处理流式响应
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if line.startswith('data: ') and line != 'data: [DONE]':
                            data_str = line[6:]  # 去掉 'data: ' 前缀
                            try:
                                import json
                                data = json.loads(data_str)
                                if 'type' in data and data['type'] == 'content_block_delta':
                                    delta = data.get('delta', {})
                                    if 'text' in delta:
                                        content = delta['text']
                                        full_text += content
                                        if callback:
                                            callback(content)
                            except Exception as e:
                                self.logger.error(f"解析流式响应失败: {str(e)}")
            
            return full_text
        
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
