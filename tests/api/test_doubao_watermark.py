#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试豆包生图模块的watermark参数
"""

import asyncio
import os
import sys
import time
import requests

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.doubao import DoubaoModel


async def test_watermark_parameter():
    """
    测试watermark参数
    """
    print("测试豆包生图模块的watermark参数...")
    
    # 初始化豆包模型
    model = DoubaoModel(
        model_name="doubao-seedream-3-0-t2i-250415",
        api_key="618fa992-0614-4819-8c68-49695100ce21",
        base_url="https://ark.cn-beijing.volces.com/api/v3"
    )
    
    # 测试提示词
    prompt = "对称的剪纸风格的中国传统蝴蝶吉祥纹样，红色背景，精细的剪纸纹理"
    
    print(f"提示词: {prompt}")
    print("正在生成图像（watermark=False）...")
    
    try:
        # 生成图像，明确设置watermark=False
        image_urls = await model.generate_image(
            prompt=prompt,
            size="1024x1024",
            n=1,
            watermark=False
        )
        
        if image_urls and not image_urls[0].startswith("生成失败"):
            image_url = image_urls[0]
            print(f"图像生成成功，URL: {image_url}")
            
            # 下载图像
            print("正在下载图像...")
            image_data = requests.get(image_url).content
            
            # 保存图像
            timestamp = int(time.time())
            file_name = f"test_watermark_false_{timestamp}.png"
            
            # 确保images目录存在
            os.makedirs("images", exist_ok=True)
            file_path = os.path.join("images", file_name)
            
            with open(file_path, "wb") as f:
                f.write(image_data)
            
            print(f"图像已保存到: {file_path}")
            
        else:
            print(f"图像生成失败: {image_urls}")
            
    except Exception as e:
        print(f"测试失败: {str(e)}")


async def test_watermark_true():
    """
    测试watermark=True的情况
    """
    print("\n测试watermark=True的情况...")
    
    # 初始化豆包模型
    model = DoubaoModel(
        model_name="doubao-seedream-3-0-t2i-250415",
        api_key="618fa992-0614-4819-8c68-49695100ce21",
        base_url="https://ark.cn-beijing.volces.com/api/v3"
    )
    
    # 测试提示词
    prompt = "对称的剪纸风格的中国传统蝴蝶吉祥纹样，蓝色背景，精细的剪纸纹理"
    
    print(f"提示词: {prompt}")
    print("正在生成图像（watermark=True）...")
    
    try:
        # 生成图像，设置watermark=True
        image_urls = await model.generate_image(
            prompt=prompt,
            size="1024x1024",
            n=1,
            watermark=True
        )
        
        if image_urls and not image_urls[0].startswith("生成失败"):
            image_url = image_urls[0]
            print(f"图像生成成功，URL: {image_url}")
            
            # 下载图像
            print("正在下载图像...")
            image_data = requests.get(image_url).content
            
            # 保存图像
            timestamp = int(time.time())
            file_name = f"test_watermark_true_{timestamp}.png"
            
            # 确保images目录存在
            os.makedirs("images", exist_ok=True)
            file_path = os.path.join("images", file_name)
            
            with open(file_path, "wb") as f:
                f.write(image_data)
            
            print(f"图像已保存到: {file_path}")
            
        else:
            print(f"图像生成失败: {image_urls}")
            
    except Exception as e:
        print(f"测试失败: {str(e)}")


async def main():
    """
    主函数
    """
    print("=== 豆包生图模块watermark参数测试 ===\n")
    
    # 测试watermark=False
    await test_watermark_parameter()
    
    # 等待一下
    await asyncio.sleep(2)
    
    # 测试watermark=True
    await test_watermark_true()
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    asyncio.run(main())
