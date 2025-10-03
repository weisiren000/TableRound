#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试图像压缩功能
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到系统路径
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT_DIR))

from src.utils.image_compressor import ImageCompressor


def test_image_compression():
    """测试图像压缩功能"""
    
    print("=== 图像压缩功能测试 ===\n")
    
    # 创建图像压缩器
    compressor = ImageCompressor(
        max_width=800,
        max_height=800,
        max_file_size_mb=1.5,
        quality=85
    )
    
    # 测试图像路径
    test_images = [
        "images/test_watermark_false_1749402117.png",
        "data/images/design_1749387656.png",
        "data/images/design_1749387769.png"
    ]
    
    for image_path in test_images:
        if not os.path.exists(image_path):
            print(f"⚠️  测试图像不存在: {image_path}")
            continue
        
        print(f"📸 测试图像: {image_path}")
        
        # 获取原始图像信息
        original_info = compressor.get_image_info(image_path)
        print(f"   原始信息: {original_info['width']}x{original_info['height']}, "
              f"{original_info['file_size_mb']:.2f}MB, {original_info['format']}")
        
        # 检查是否需要压缩
        needs_compression = compressor.needs_compression(image_path)
        print(f"   需要压缩: {'是' if needs_compression else '否'}")
        
        if needs_compression:
            # 执行压缩
            compressed_path = compressor.compress_image(image_path)
            
            if compressed_path != image_path:
                # 获取压缩后的信息
                compressed_info = compressor.get_image_info(compressed_path)
                print(f"   压缩后: {compressed_info['width']}x{compressed_info['height']}, "
                      f"{compressed_info['file_size_mb']:.2f}MB")
                
                # 计算压缩比
                compression_ratio = compressed_info['file_size'] / original_info['file_size']
                print(f"   压缩比: {compression_ratio:.2%}, 节省: {(1-compression_ratio)*100:.1f}%")
                
                # 清理测试文件
                if os.path.exists(compressed_path):
                    os.remove(compressed_path)
                    print(f"   ✅ 已清理测试文件: {compressed_path}")
            else:
                print("   ✅ 图像无需压缩")
        
        print()


def test_api_compression():
    """测试API专用压缩"""
    
    print("=== API专用压缩测试 ===\n")
    
    # 创建图像压缩器
    compressor = ImageCompressor()
    
    # 测试图像路径
    test_image = "images/test_watermark_false_1749402117.png"
    
    if not os.path.exists(test_image):
        print(f"⚠️  测试图像不存在: {test_image}")
        return
    
    print(f"📸 测试图像: {test_image}")
    
    # 获取原始图像信息
    original_info = compressor.get_image_info(test_image)
    print(f"   原始信息: {original_info['width']}x{original_info['height']}, "
          f"{original_info['file_size_mb']:.2f}MB")
    
    # 执行API专用压缩
    api_compressed_path = compressor.compress_for_api(test_image)
    
    if api_compressed_path != test_image:
        # 获取压缩后的信息
        compressed_info = compressor.get_image_info(api_compressed_path)
        print(f"   API压缩后: {compressed_info['width']}x{compressed_info['height']}, "
              f"{compressed_info['file_size_mb']:.2f}MB")
        
        # 计算压缩比
        compression_ratio = compressed_info['file_size'] / original_info['file_size']
        print(f"   压缩比: {compression_ratio:.2%}, 节省: {(1-compression_ratio)*100:.1f}%")
        
        # 验证是否满足API要求
        api_requirements_met = (
            compressed_info['width'] <= 800 and 
            compressed_info['height'] <= 800 and 
            compressed_info['file_size_mb'] <= 1.5
        )
        print(f"   满足API要求: {'✅ 是' if api_requirements_met else '❌ 否'}")
        
        # 清理测试文件
        if os.path.exists(api_compressed_path):
            os.remove(api_compressed_path)
            print(f"   ✅ 已清理测试文件: {api_compressed_path}")
    else:
        print("   ✅ 图像已满足API要求，无需压缩")


def test_compression_quality():
    """测试不同压缩质量"""
    
    print("=== 压缩质量测试 ===\n")
    
    test_image = "images/test_watermark_false_1749402117.png"
    
    if not os.path.exists(test_image):
        print(f"⚠️  测试图像不存在: {test_image}")
        return
    
    print(f"📸 测试图像: {test_image}")
    
    # 测试不同质量设置
    qualities = [95, 85, 75, 65, 55]
    
    for quality in qualities:
        compressor = ImageCompressor(
            max_width=800,
            max_height=800,
            max_file_size_mb=5.0,  # 较大的限制，主要测试质量
            quality=quality
        )
        
        # 获取原始信息
        original_info = compressor.get_image_info(test_image)
        
        # 压缩
        compressed_path = compressor.compress_image(test_image)
        
        if compressed_path != test_image:
            compressed_info = compressor.get_image_info(compressed_path)
            compression_ratio = compressed_info['file_size'] / original_info['file_size']
            
            print(f"   质量 {quality}: {compressed_info['file_size_mb']:.2f}MB, "
                  f"压缩比 {compression_ratio:.2%}")
            
            # 清理测试文件
            if os.path.exists(compressed_path):
                os.remove(compressed_path)


def main():
    """主函数"""
    print("TableRound 图像压缩功能测试\n")
    
    # 基础压缩测试
    test_image_compression()
    
    # API专用压缩测试
    test_api_compression()
    
    # 压缩质量测试
    test_compression_quality()
    
    print("=== 测试完成 ===")


if __name__ == "__main__":
    main()
