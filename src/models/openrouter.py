#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenRouter模型接口模块
"""

import base64
import logging
import os
import re
from typing import Optional, Dict, Any, List, Callable

import aiohttp

from src.models.base import BaseModel


class OpenRouterModel(BaseModel):
    """OpenRouter模型接口"""

    def __init__(
        self,
        model_name: str = "meta-llama/llama-4-maverick:free",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        """
        初始化OpenRouter模型

        Args:
            model_name: 模型名称
            api_key: API密钥
            base_url: API基础URL
            **kwargs: 其他参数
        """
        super().__init__(model_name, **kwargs)
        
        # 设置API密钥
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API密钥未提供")
        
        # 设置API基础URL
        self.base_url = base_url or os.environ.get("OPENROUTER_BASE_URL") or "https://openrouter.ai/api/v1"
        
        # 设置默认参数
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 2000)
        
        # 检查是否支持图像
        self.vision_supported = "vision" in model_name.lower() or model_name in [
            "moonshotai/kimi-vl-a3b-thinking:free"
        ]
        
        # 检查是否支持思维模型
        self.thinking_supported = "thinking" in model_name.lower() or model_name in [
            "moonshotai/kimi-vl-a3b-thinking:free"
        ]
        
        self.logger = logging.getLogger(f"model.openrouter.{model_name}")

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
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "https://tableround.example.com",
                        "X-Title": "TableRound"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"API请求失败: {response.status}, {error_text}")
                        return f"生成失败: API请求返回 {response.status}"
                    
                    result = await response.json()
                    
                    # 获取生成的文本
                    content = result["choices"][0]["message"]["content"]
                    
                    # 处理思维模型输出
                    if self.thinking_supported:
                        # 移除思维内容
                        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
                    
                    return content
        
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
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "https://tableround.example.com",
                        "X-Title": "TableRound"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"API请求失败: {response.status}, {error_text}")
                        return f"生成失败: API请求返回 {response.status}"
                    
                    result = await response.json()
                    
                    # 获取生成的文本
                    content = result["choices"][0]["message"]["content"]
                    
                    # 处理思维模型输出
                    if self.thinking_supported:
                        # 移除思维内容
                        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
                    
                    return content
        
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
            full_text = ""
            thinking_buffer = ""
            in_thinking = False
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "https://tableround.example.com",
                        "X-Title": "TableRound"
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
                                if 'choices' in data and data['choices'] and 'delta' in data['choices'][0]:
                                    delta = data['choices'][0]['delta']
                                    if 'content' in delta and delta['content']:
                                        content = delta['content']
                                        
                                        # 处理思维模型输出
                                        if self.thinking_supported:
                                            # 检查是否进入思维模式
                                            if '<think>' in content:
                                                in_thinking = True
                                                thinking_start_index = content.find('<think>')
                                                visible_content = content[:thinking_start_index]
                                                thinking_buffer += content[thinking_start_index:]
                                                content = visible_content
                                            
                                            # 检查是否退出思维模式
                                            elif '</think>' in content and in_thinking:
                                                thinking_end_index = content.find('</think>') + 8  # 8 是 '</think>' 的长度
                                                thinking_buffer += content[:thinking_end_index]
                                                visible_content = content[thinking_end_index:]
                                                content = visible_content
                                                in_thinking = False
                                                thinking_buffer = ""
                                            
                                            # 如果在思维模式中
                                            elif in_thinking:
                                                thinking_buffer += content
                                                content = ""
                                        
                                        if content:
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
