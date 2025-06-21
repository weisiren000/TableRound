#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图像处理模块
"""

import os
import base64
import logging
import time
import requests
from typing import Optional, Dict, Any, List


class ImageProcessor:
    """图像处理类"""

    def __init__(self, settings):
        """
        初始化图像处理器

        Args:
            settings: 全局设置
        """
        self.settings = settings
        self.logger = logging.getLogger("image_processor")
        self.client = None  # 初始化时不创建客户端，延迟到需要时创建

    def prepare_image_for_api(self, image_path: str) -> Optional[str]:
        """
        准备图片用于API调用

        Args:
            image_path: 图片路径

        Returns:
            Base64编码的图片数据
        """
        try:
            # 支持的图片格式
            supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

            # 检查文件格式
            file_ext = os.path.splitext(image_path)[1].lower()
            if file_ext not in supported_formats:
                self.logger.error(f"不支持的图片格式: {file_ext}")
                return None

            # 读取图片
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        except Exception as e:
            self.logger.error(f"图片处理失败: {str(e)}")
            return None

    def optimize_image_prompt(self, user_prompt: str) -> str:
        """
        优化图像生成提示词

        Args:
            user_prompt: 用户输入的提示词

        Returns:
            优化后的提示词
        """
        # 基础提示词，确保生成的图像符合要求
        base_prompt = "对称的剪纸风格的中国传统蝙蝠吉祥纹样，"

        # 添加细节描述
        details = "精细的剪纸纹理，传统中国红色调，对称构图，"

        # 添加风格描述
        style = "中国传统民间艺术风格，平面设计，简洁清晰的线条，"

        # 组合提示词
        optimized_prompt = f"{base_prompt}{details}{style}{user_prompt}"

        return optimized_prompt

    async def generate_image(self, prompt: str, size: str = "1024x1024", provider: str = None) -> Optional[str]:
        """
        生成图像

        Args:
            prompt: 提示词
            size: 图像尺寸
            provider: 提供商，默认使用配置中的提供商

        Returns:
            生成的图像路径
        """
        try:
            # 优化提示词
            optimized_prompt = self.optimize_image_prompt(prompt)

            # 确定使用的提供商
            provider = provider or self.settings.provider

            # 根据提供商选择不同的实现
            if provider.lower() == "doubao":
                return await self._generate_image_doubao(optimized_prompt, size)
            else:
                return await self._generate_image_openai(optimized_prompt, size)

        except Exception as e:
            self.logger.error(f"生成图像失败: {str(e)}")
            return None

    async def _generate_image_openai(self, prompt: str, size: str = "1024x1024") -> Optional[str]:
        """
        使用OpenAI生成图像

        Args:
            prompt: 提示词
            size: 图像尺寸

        Returns:
            生成的图像路径
        """
        try:
            # 初始化客户端（如果需要）
            if self.client is None:
                import openai
                self.client = openai.AsyncOpenAI(
                    api_key=self.settings.get_api_key("openai"),
                    base_url=self.settings.get_base_url("openai")
                )

            # 调用图像生成API
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
            )

            # 获取图像URL
            image_url = response.data[0].url

            # 下载图像
            image_data = requests.get(image_url).content

            # 生成文件名
            timestamp = int(time.time())
            file_name = f"design_{timestamp}.png"
            file_path = os.path.join(self.settings.IMAGE_DIR, file_name)

            # 保存图像
            with open(file_path, "wb") as f:
                f.write(image_data)

            return file_path

        except Exception as e:
            self.logger.error(f"OpenAI图像生成失败: {str(e)}")
            return None

    async def _generate_image_doubao(self, prompt: str, size: str = "1024x1024") -> Optional[str]:
        """
        使用豆包API生成图像

        Args:
            prompt: 提示词
            size: 图像尺寸

        Returns:
            生成的图像路径
        """
        try:
            # 获取豆包模型实例
            from src.models.doubao import DoubaoModel
            model = DoubaoModel(
                model_name="doubao-seedream-3-0-t2i-250415",
                api_key=self.settings.get_api_key("doubao"),
                base_url=self.settings.get_base_url("doubao")
            )

            # 调用图像生成API，设置watermark=False
            image_urls = await model.generate_image(prompt, size, watermark=False)

            if not image_urls or not image_urls[0] or image_urls[0].startswith("生成失败"):
                self.logger.error(f"豆包API生成图像失败: {image_urls}")
                return None

            # 获取图像URL
            image_url = image_urls[0]

            # 下载图像
            image_data = requests.get(image_url).content

            # 生成文件名
            timestamp = int(time.time())
            file_name = f"design_{timestamp}.png"
            file_path = os.path.join(self.settings.IMAGE_DIR, file_name)

            # 保存图像
            with open(file_path, "wb") as f:
                f.write(image_data)

            return file_path

        except Exception as e:
            self.logger.error(f"图像生成失败: {str(e)}")
            return None

    def merge_images(self, image1_path: str, image2_path: str) -> Optional[str]:
        """
        合并两张图像

        Args:
            image1_path: 第一张图像路径
            image2_path: 第二张图像路径

        Returns:
            合并后的图像路径
        """
        try:
            from PIL import Image

            # 打开图像
            image1 = Image.open(image1_path)
            image2 = Image.open(image2_path)

            # 调整图像大小
            max_width = max(image1.width, image2.width)
            max_height = image1.height + image2.height

            # 创建新图像
            merged_image = Image.new("RGB", (max_width, max_height), (255, 255, 255))

            # 粘贴图像
            merged_image.paste(image1, (0, 0))
            merged_image.paste(image2, (0, image1.height))

            # 生成文件名
            timestamp = int(time.time())
            file_name = f"merged_{timestamp}.png"
            file_path = os.path.join(self.settings.IMAGE_DIR, file_name)

            # 保存图像
            merged_image.save(file_path)

            return file_path

        except Exception as e:
            self.logger.error(f"图像合并失败: {str(e)}")
            return None

    async def generate_image_from_image(self, image_path: str, prompt: str, provider: str = None) -> Optional[str]:
        """
        基于参考图像生成新图像

        Args:
            image_path: 参考图像路径
            prompt: 提示词
            provider: 提供商，默认使用配置中的提供商

        Returns:
            生成的图像路径
        """
        try:
            # 优化提示词
            optimized_prompt = self.optimize_image_prompt(prompt)

            # 确定使用的提供商
            provider = provider or self.settings.provider

            # 根据提供商选择不同的实现
            if provider.lower() == "doubao":
                return await self._generate_image_from_image_doubao(image_path, optimized_prompt)
            else:
                # 目前OpenAI不支持图生图，使用豆包API
                self.logger.warning("OpenAI不支持图生图功能，将使用豆包API")
                return await self._generate_image_from_image_doubao(image_path, optimized_prompt)

        except Exception as e:
            self.logger.error(f"基于图像生成图像失败: {str(e)}")
            return None

    async def _generate_image_from_image_doubao(self, image_path: str, prompt: str) -> Optional[str]:
        """
        使用豆包API基于参考图像生成新图像

        Args:
            image_path: 参考图像路径
            prompt: 提示词

        Returns:
            生成的图像路径
        """
        try:
            # 读取图像
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            # 构建请求数据
            data = {
                "model": "doubao-seedream-3-0-t2i-250415",
                "prompt": prompt,
                "image": f"data:image/jpeg;base64,{base64_image}",
                "strength": 0.7  # 控制参考图像的影响程度，0.0-1.0
            }

            # 构建URL
            url = f"{self.settings.get_base_url('doubao').rstrip('/')}/images/variations"

            # 发送请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.get_api_key('doubao')}"
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code != 200:
                self.logger.error(f"豆包API请求失败: {response.status_code}, {response.text}")
                return None

            result = response.json()

            # 获取图像URL
            image_url = result["data"][0]["url"]

            # 下载图像
            image_data = requests.get(image_url).content

            # 生成文件名
            timestamp = int(time.time())
            file_name = f"variation_{timestamp}.png"
            file_path = os.path.join(self.settings.IMAGE_DIR, file_name)

            # 保存图像
            with open(file_path, "wb") as f:
                f.write(image_data)

            return file_path

        except Exception as e:
            self.logger.error(f"基于图像生成图像失败: {str(e)}")
            return None
