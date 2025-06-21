#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图像压缩工具模块
"""

import os
import logging
from typing import Tuple, Optional
from PIL import Image, ImageOps
import io


class ImageCompressor:
    """图像压缩工具类"""
    
    def __init__(
        self,
        max_width: int = 1024,
        max_height: int = 1024,
        max_file_size_mb: float = 2.0,
        quality: int = 85,
        format: str = "JPEG"
    ):
        """
        初始化图像压缩器
        
        Args:
            max_width: 最大宽度
            max_height: 最大高度
            max_file_size_mb: 最大文件大小(MB)
            quality: JPEG质量(1-100)
            format: 输出格式
        """
        self.max_width = max_width
        self.max_height = max_height
        self.max_file_size_bytes = int(max_file_size_mb * 1024 * 1024)
        self.quality = quality
        self.format = format
        self.logger = logging.getLogger("image_compressor")
    
    def get_image_info(self, image_path: str) -> dict:
        """
        获取图像信息
        
        Args:
            image_path: 图像路径
            
        Returns:
            图像信息字典
        """
        try:
            with Image.open(image_path) as img:
                file_size = os.path.getsize(image_path)
                return {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode,
                    "file_size": file_size,
                    "file_size_mb": file_size / (1024 * 1024)
                }
        except Exception as e:
            self.logger.error(f"获取图像信息失败: {str(e)}")
            return {}
    
    def needs_compression(self, image_path: str) -> bool:
        """
        判断是否需要压缩
        
        Args:
            image_path: 图像路径
            
        Returns:
            是否需要压缩
        """
        info = self.get_image_info(image_path)
        if not info:
            return False
        
        # 检查文件大小
        if info["file_size"] > self.max_file_size_bytes:
            return True
        
        # 检查图像尺寸
        if info["width"] > self.max_width or info["height"] > self.max_height:
            return True
        
        return False
    
    def calculate_new_size(self, width: int, height: int) -> Tuple[int, int]:
        """
        计算新的图像尺寸，保持宽高比
        
        Args:
            width: 原始宽度
            height: 原始高度
            
        Returns:
            新的宽度和高度
        """
        # 计算缩放比例
        width_ratio = self.max_width / width
        height_ratio = self.max_height / height
        ratio = min(width_ratio, height_ratio, 1.0)  # 不放大图像
        
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        return new_width, new_height
    
    def compress_image(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        压缩图像
        
        Args:
            input_path: 输入图像路径
            output_path: 输出图像路径，如果为None则覆盖原文件
            
        Returns:
            压缩后的图像路径
        """
        try:
            # 获取原始图像信息
            original_info = self.get_image_info(input_path)
            self.logger.info(f"原始图像信息: {original_info}")
            
            # 如果不需要压缩，直接返回原路径
            if not self.needs_compression(input_path):
                self.logger.info("图像无需压缩")
                return input_path
            
            # 设置输出路径
            if output_path is None:
                name, ext = os.path.splitext(input_path)
                output_path = f"{name}_compressed{ext}"
            
            # 打开并处理图像
            with Image.open(input_path) as img:
                # 转换为RGB模式（JPEG不支持透明度）
                if img.mode in ('RGBA', 'LA', 'P'):
                    # 创建白色背景
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 自动旋转图像（根据EXIF信息）
                img = ImageOps.exif_transpose(img)
                
                # 计算新尺寸
                new_width, new_height = self.calculate_new_size(img.width, img.height)
                
                # 调整图像尺寸
                if new_width != img.width or new_height != img.height:
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    self.logger.info(f"图像尺寸调整: {img.width}x{img.height} -> {new_width}x{new_height}")
                
                # 动态调整质量以满足文件大小要求
                quality = self.quality
                while quality > 10:
                    # 保存到内存缓冲区测试文件大小
                    buffer = io.BytesIO()
                    img.save(buffer, format=self.format, quality=quality, optimize=True)
                    
                    if buffer.tell() <= self.max_file_size_bytes:
                        break
                    
                    quality -= 10
                    self.logger.debug(f"调整质量到 {quality}")
                
                # 保存最终图像
                img.save(output_path, format=self.format, quality=quality, optimize=True)
            
            # 获取压缩后的图像信息
            compressed_info = self.get_image_info(output_path)
            self.logger.info(f"压缩后图像信息: {compressed_info}")
            
            # 计算压缩比
            if original_info and compressed_info:
                compression_ratio = compressed_info["file_size"] / original_info["file_size"]
                self.logger.info(f"压缩比: {compression_ratio:.2%}, 节省: {(1-compression_ratio)*100:.1f}%")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"图像压缩失败: {str(e)}")
            # 如果压缩失败，返回原文件路径
            return input_path
    
    def compress_for_api(self, image_path: str) -> str:
        """
        为API调用优化的图像压缩
        
        Args:
            image_path: 图像路径
            
        Returns:
            压缩后的图像路径
        """
        # 为API调用使用更严格的限制
        original_max_width = self.max_width
        original_max_height = self.max_height
        original_max_file_size = self.max_file_size_bytes
        
        # API优化设置
        self.max_width = 800  # 更小的尺寸
        self.max_height = 800
        self.max_file_size_bytes = int(1.5 * 1024 * 1024)  # 1.5MB
        
        try:
            # 生成API专用的压缩文件名
            name, ext = os.path.splitext(image_path)
            api_compressed_path = f"{name}_api_compressed{ext}"
            
            result = self.compress_image(image_path, api_compressed_path)
            
            return result
            
        finally:
            # 恢复原始设置
            self.max_width = original_max_width
            self.max_height = original_max_height
            self.max_file_size_bytes = original_max_file_size
