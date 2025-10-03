#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试图像压缩与两阶段模型调用的集成
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
from src.utils.image_compressor import ImageCompressor


async def test_compression_integration():
    """测试图像压缩与模型调用的集成"""
    
    # 设置日志级别
    logging.basicConfig(level=logging.INFO)
    
    # 检查API密钥
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("错误：未设置OPENROUTER_API_KEY环境变量")
        return
    
    print("=== 图像压缩与两阶段模型调用集成测试 ===\n")
    
    # 创建OpenRouter模型实例
    model = OpenRouterModel(
        model_name="deepseek/deepseek-r1-0528:free",
        api_key=api_key
    )
    
    print(f"主模型: {model.model_name}")
    print(f"视觉模型: {model.vision_model}")
    print(f"对话模型: {model.chat_model}")
    print(f"图像压缩器配置: 最大尺寸{model.image_compressor.max_width}x{model.image_compressor.max_height}, "
          f"最大文件大小{model.image_compressor.max_file_size_bytes/(1024*1024):.1f}MB\n")
    
    # 测试图像路径
    test_image_path = "images/test_watermark_false_1749402117.png"
    
    if not os.path.exists(test_image_path):
        print(f"错误：测试图像不存在: {test_image_path}")
        return
    
    # 获取原始图像信息
    compressor = ImageCompressor()
    original_info = compressor.get_image_info(test_image_path)
    print(f"原始图像信息:")
    print(f"  尺寸: {original_info['width']}x{original_info['height']}")
    print(f"  文件大小: {original_info['file_size_mb']:.2f}MB")
    print(f"  格式: {original_info['format']}\n")
    
    # 测试压缩功能
    print("--- 测试图像压缩 ---")
    compressed_path = model.image_compressor.compress_for_api(test_image_path)
    
    if compressed_path != test_image_path:
        compressed_info = compressor.get_image_info(compressed_path)
        print(f"压缩后图像信息:")
        print(f"  尺寸: {compressed_info['width']}x{compressed_info['height']}")
        print(f"  文件大小: {compressed_info['file_size_mb']:.2f}MB")
        print(f"  压缩比: {compressed_info['file_size']/original_info['file_size']:.2%}")
        print(f"  节省空间: {(1-compressed_info['file_size']/original_info['file_size'])*100:.1f}%\n")
    else:
        print("图像无需压缩\n")
    
    # 测试两阶段模型调用（使用压缩后的图像）
    print("--- 测试两阶段模型调用 ---")
    prompt = "请根据这张图片讲一个简短的故事，并提取3-5个关键词"
    system_prompt = "你是一个富有创意的故事讲述者。"
    
    try:
        print("开始调用两阶段模型...")
        result = await model.generate_with_image(prompt, system_prompt, test_image_path)
        
        print("=== 模型调用结果 ===")
        print(f"结果长度: {len(result)}字符")
        print(f"结果内容: {result[:200]}...")
        
    except Exception as e:
        print(f"模型调用失败: {str(e)}")
    
    # 清理压缩文件
    if compressed_path != test_image_path and os.path.exists(compressed_path):
        os.remove(compressed_path)
        print(f"\n✅ 已清理压缩文件: {compressed_path}")


async def test_compression_performance():
    """测试压缩性能对比"""
    
    print("\n=== 压缩性能对比测试 ===\n")
    
    test_image_path = "images/test_watermark_false_1749402117.png"
    
    if not os.path.exists(test_image_path):
        print(f"错误：测试图像不存在: {test_image_path}")
        return
    
    # 测试不同压缩设置的性能
    compression_configs = [
        {"max_width": 1024, "max_height": 1024, "quality": 95, "name": "高质量"},
        {"max_width": 800, "max_height": 800, "quality": 85, "name": "标准质量"},
        {"max_width": 600, "max_height": 600, "quality": 75, "name": "压缩优化"},
        {"max_width": 400, "max_height": 400, "quality": 65, "name": "高压缩"}
    ]
    
    original_compressor = ImageCompressor()
    original_info = original_compressor.get_image_info(test_image_path)
    
    print(f"原始图像: {original_info['width']}x{original_info['height']}, {original_info['file_size_mb']:.2f}MB\n")
    
    for config in compression_configs:
        compressor = ImageCompressor(
            max_width=config["max_width"],
            max_height=config["max_height"],
            quality=config["quality"]
        )
        
        compressed_path = compressor.compress_image(test_image_path)
        
        if compressed_path != test_image_path:
            compressed_info = compressor.get_image_info(compressed_path)
            compression_ratio = compressed_info['file_size'] / original_info['file_size']
            
            print(f"{config['name']}:")
            print(f"  尺寸: {compressed_info['width']}x{compressed_info['height']}")
            print(f"  文件大小: {compressed_info['file_size_mb']:.2f}MB")
            print(f"  压缩比: {compression_ratio:.2%}")
            print(f"  Base64大小估算: {compressed_info['file_size'] * 1.33 / (1024*1024):.2f}MB")
            
            # 清理测试文件
            if os.path.exists(compressed_path):
                os.remove(compressed_path)
        else:
            print(f"{config['name']}: 无需压缩")
        
        print()


async def main():
    """主函数"""
    print("TableRound 图像压缩集成测试\n")
    
    # 测试压缩集成
    await test_compression_integration()
    
    # 测试压缩性能
    await test_compression_performance()
    
    print("=== 测试完成 ===")


if __name__ == "__main__":
    asyncio.run(main())
