#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
调试图像路径传递问题
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到系统路径
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT_DIR))

from src.models.openrouter import OpenRouterModel


async def test_image_path_debug():
    """调试图像路径传递"""
    
    # 设置日志级别
    logging.basicConfig(level=logging.INFO)
    
    # 检查API密钥
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("错误：未设置OPENROUTER_API_KEY环境变量")
        return
    
    print("=== 图像路径传递调试 ===\n")
    
    # 创建OpenRouter模型实例
    model = OpenRouterModel(
        model_name="deepseek/deepseek-r1-0528:free",
        api_key=api_key
    )
    
    # 测试用户实际输入的图像路径
    user_image_path = "d:\\codee\\tableround\\data\\images\\design_1749387656.png"
    
    print(f"用户输入的图像路径: {user_image_path}")
    print(f"文件是否存在: {os.path.exists(user_image_path)}")
    
    if not os.path.exists(user_image_path):
        print("错误：用户输入的图像文件不存在")
        return
    
    # 测试图像压缩
    print("\n--- 测试图像压缩 ---")
    compressed_path = model.image_compressor.compress_for_api(user_image_path)
    print(f"压缩后路径: {compressed_path}")
    print(f"压缩文件是否存在: {os.path.exists(compressed_path)}")
    
    # 测试模型调用
    print("\n--- 测试模型调用 ---")
    prompt = "请简单描述这张图片"
    system_prompt = "你是一个图像分析专家"
    
    try:
        # 直接调用视觉模型描述方法
        print("调用视觉模型描述图像...")
        image_description = await model._describe_image_with_vision_model(prompt, system_prompt, user_image_path)
        print(f"图像描述长度: {len(image_description)}")
        print(f"图像描述前100字符: {image_description[:100]}...")
        
    except Exception as e:
        print(f"模型调用失败: {str(e)}")
    
    # 清理压缩文件
    if compressed_path != user_image_path and os.path.exists(compressed_path):
        os.remove(compressed_path)
        print(f"\n✅ 已清理压缩文件: {compressed_path}")


async def test_different_images():
    """测试不同的图像文件"""
    
    print("\n=== 测试不同图像文件 ===\n")
    
    # 检查API密钥
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("错误：未设置OPENROUTER_API_KEY环境变量")
        return
    
    # 创建模型实例
    model = OpenRouterModel(
        model_name="deepseek/deepseek-r1-0528:free",
        api_key=api_key
    )
    
    # 测试多个图像文件
    test_images = [
        "d:\\codee\\tableround\\data\\images\\design_1749387656.png",
        "images/test_watermark_false_1749402117.png",
        "images/test_watermark_true_1749402123.png"
    ]
    
    for image_path in test_images:
        print(f"测试图像: {image_path}")
        print(f"文件存在: {os.path.exists(image_path)}")
        
        if os.path.exists(image_path):
            # 测试压缩
            compressed_path = model.image_compressor.compress_for_api(image_path)
            print(f"压缩后: {compressed_path}")
            
            # 清理
            if compressed_path != image_path and os.path.exists(compressed_path):
                os.remove(compressed_path)
        
        print()


async def main():
    """主函数"""
    print("TableRound 图像路径传递调试\n")
    
    # 测试图像路径传递
    await test_image_path_debug()
    
    # 测试不同图像
    await test_different_images()
    
    print("=== 调试完成 ===")


if __name__ == "__main__":
    asyncio.run(main())
