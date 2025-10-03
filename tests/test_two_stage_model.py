#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试两阶段模型调用机制
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到系统路径
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT_DIR))

from src.models.openrouter import OpenRouterModel


async def test_two_stage_model():
    """测试两阶段模型调用机制"""
    
    # 检查API密钥
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("错误：未设置OPENROUTER_API_KEY环境变量")
        return
    
    print("=== 两阶段模型调用机制测试 ===\n")
    
    # 创建OpenRouter模型实例
    model = OpenRouterModel(
        model_name="deepseek/deepseek-r1-0528:free",  # 主模型（对话阶段使用）
        api_key=api_key
    )
    
    print(f"主模型: {model.model_name}")
    print(f"视觉模型: {model.vision_model}")
    print(f"对话模型: {model.chat_model}")
    print(f"支持图像处理: {model.supports_vision()}\n")
    
    # 测试图像路径
    test_image_path = "images/test_watermark_false_1749402117.png"
    
    if not os.path.exists(test_image_path):
        print(f"错误：测试图像不存在: {test_image_path}")
        print("请确保images目录下有测试图像文件")
        return
    
    print(f"使用测试图像: {test_image_path}\n")
    
    # 测试提示词
    prompt = "请根据这张图片讲一个有趣的故事，并提取5-10个关键词"
    system_prompt = "你是一个富有创意的故事讲述者，善于从图像中发现有趣的元素并编织成引人入胜的故事。"
    
    print("=== 开始两阶段处理 ===\n")
    
    try:
        # 调用两阶段模型处理
        result = await model.generate_with_image(prompt, system_prompt, test_image_path)
        
        print("=== 最终结果 ===")
        print(result)
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"测试失败: {str(e)}")


async def test_individual_stages():
    """测试各个阶段的独立功能"""
    
    # 检查API密钥
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("错误：未设置OPENROUTER_API_KEY环境变量")
        return
    
    print("\n=== 独立阶段测试 ===\n")
    
    # 创建OpenRouter模型实例
    model = OpenRouterModel(
        model_name="deepseek/deepseek-r1-0528:free",
        api_key=api_key
    )
    
    # 测试图像路径
    test_image_path = "images/test_watermark_false_1749402117.png"
    
    if not os.path.exists(test_image_path):
        print(f"错误：测试图像不存在: {test_image_path}")
        return
    
    prompt = "请根据这张图片讲一个有趣的故事"
    system_prompt = "你是一个富有创意的故事讲述者。"
    
    try:
        print("--- 第一阶段：视觉模型图像描述 ---")
        image_description = await model._describe_image_with_vision_model(prompt, system_prompt, test_image_path)
        print(f"图像描述长度: {len(image_description)}")
        print(f"图像描述内容: {image_description[:200]}...")
        
        print("\n--- 第二阶段：对话模型生成回答 ---")
        final_result = await model._generate_with_chat_model(prompt, system_prompt, image_description)
        print(f"最终回答长度: {len(final_result)}")
        print(f"最终回答: {final_result}")
        
    except Exception as e:
        print(f"独立阶段测试失败: {str(e)}")


async def main():
    """主函数"""
    print("TableRound 两阶段模型调用机制测试\n")
    
    # 测试两阶段模型调用
    await test_two_stage_model()
    
    # 测试独立阶段
    await test_individual_stages()


if __name__ == "__main__":
    asyncio.run(main())
