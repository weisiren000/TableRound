#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenAI模型接口模块
"""

import base64
import logging
import os
from typing import Optional, Dict, Any, List, Callable

import openai
from openai import AsyncOpenAI

from src.models.base import BaseModel


class OpenAIModel(BaseModel):
    """OpenAI模型接口"""

    def __init__(
        self,
        model_name: str = "gpt-4",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        """
        初始化OpenAI模型

        Args:
            model_name: 模型名称
            api_key: API密钥
            base_url: API基础URL
            **kwargs: 其他参数
        """
        super().__init__(model_name, **kwargs)
        
        # 设置API密钥
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API密钥未提供")
        
        # 创建客户端
        client_kwargs = {"api_key": self.api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        
        self.client = AsyncOpenAI(**client_kwargs)
        
        # 设置默认参数
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 2000)
        
        # 检查是否支持图像
        self.vision_supported = "vision" in model_name or model_name in [
            "gpt-4-vision-preview", "gpt-4-turbo", "gpt-4o", "gpt-4"
        ]
        
        self.logger = logging.getLogger(f"model.openai.{model_name}")

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
            
            # 调用API
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # 获取生成的文本
            return response.choices[0].message.content
        
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
            
            # 调用API
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # 获取生成的文本
            return response.choices[0].message.content
        
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
            
            # 调用API
            stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            # 处理流式输出
            full_text = ""
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_text += content
                    if callback:
                        callback(content)
            
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
