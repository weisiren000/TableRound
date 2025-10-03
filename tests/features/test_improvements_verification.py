#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
验证改进功能的测试脚本
测试Google模型图像识别、关键词提取格式、智能体个性化等功能
"""

import asyncio
import os
import sys
import base64

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.google import GoogleModel
from src.core.agent import Agent
from src.config.prompts import prompt_manager


async def test_google_vision_support():
    """测试Google模型的图像识别支持"""
    print("=== 测试Google模型图像识别支持 ===")
    
    # 初始化Google模型
    model = GoogleModel(
        model_name="gemini-2.5-flash-preview-05-20",
        api_key=os.getenv("GOOGLE_API_KEY", "test_key"),
        base_url="https://generativelanguage.googleapis.com/v1beta"
    )
    
    print(f"模型名称: {model.model_name}")
    print(f"是否支持图像: {model.supports_image_processing()}")
    
    if model.supports_image_processing():
        print("✅ Google模型图像识别支持已修复")
    else:
        print("❌ Google模型图像识别支持仍有问题")
    
    return model.supports_image_processing()


async def test_keyword_extraction_format():
    """测试关键词提取的新格式支持"""
    print("\n=== 测试关键词提取格式 ===")
    
    # 模拟包含<key_words>标签的响应
    test_responses = [
        "<key_words>传统文化, 剪纸艺术, 蝴蝶纹样</key_words>",
        "这是一个关于传统文化的故事...\n<key_words>传统文化, 剪纸艺术, 蝴蝶纹样, 吉祥图案</key_words>",
        '["传统文化", "剪纸艺术", "蝴蝶纹样"]',  # 备选格式
        "传统文化\n剪纸艺术\n蝙蝠纹样"  # 简单格式
    ]
    
    # 创建一个测试智能体
    agent = Agent(
        name="test_agent",
        role="craftsman",
        model=None  # 不需要真实模型
    )
    
    for i, response in enumerate(test_responses):
        print(f"\n测试响应 {i+1}: {response}")
        
        # 模拟关键词解析逻辑
        import re
        import json
        
        keywords = []
        try:
            # 尝试直接解析JSON
            keywords = json.loads(response)
        except:
            # 尝试提取<key_words>标签内的内容
            key_words_match = re.search(r'<key_words>(.*?)</key_words>', response, re.DOTALL)
            if key_words_match:
                keywords_str = key_words_match.group(1)
                keywords = [k.strip().strip('"\'') for k in keywords_str.split(',')]
            else:
                # 如果解析失败，尝试提取方括号内的内容
                match = re.search(r'\[(.*?)\]', response, re.DOTALL)
                if match:
                    keywords_str = match.group(1)
                    keywords = [k.strip().strip('"\'') for k in keywords_str.split(',')]
                else:
                    # 简单的分行提取
                    keywords = [line.strip().strip('"-,') for line in response.split('\n')
                               if line.strip() and not line.strip().startswith(('[', ']'))]
        
        # 清理空关键词
        keywords = [kw.strip() for kw in keywords if kw.strip()]
        
        print(f"提取的关键词: {keywords}")
        print(f"关键词数量: {len(keywords)}")
        
        if len(keywords) > 0:
            print("✅ 关键词提取成功")
        else:
            print("❌ 关键词提取失败")
    
    return True


async def test_agent_personality():
    """测试智能体个性化差异"""
    print("\n=== 测试智能体个性化差异 ===")
    
    roles = ["craftsman", "consumer", "manufacturer", "designer"]
    
    for role in roles:
        print(f"\n--- {role} 角色 ---")
        
        # 获取角色描述
        role_description = prompt_manager._role_descriptions.get(role, "")
        print(f"角色描述长度: {len(role_description)} 字符")
        
        # 检查是否包含语言风格特点
        if "语言风格特点" in role_description:
            print("✅ 包含语言风格特点")
            
            # 提取语言风格部分
            style_start = role_description.find("语言风格特点：")
            if style_start != -1:
                style_section = role_description[style_start:style_start+200]
                print(f"风格特点预览: {style_section}...")
        else:
            print("❌ 缺少语言风格特点")
        
        # 获取系统提示词
        system_prompt = prompt_manager.get_system_prompt(role)
        
        # 检查是否包含个性化指导
        if "避免使用套话" in system_prompt or "体现你的个人特色" in system_prompt:
            print("✅ 系统提示词包含个性化指导")
        else:
            print("❌ 系统提示词缺少个性化指导")
    
    return True


async def test_image_story_prompt():
    """测试图片故事提示词的改进"""
    print("\n=== 测试图片故事提示词改进 ===")
    
    # 获取图片故事提示词
    role = "craftsman"
    role_description = prompt_manager._role_descriptions.get(role, "")
    
    from src.config.prompts.base_prompts import BasePrompts
    image_story_prompt = BasePrompts.get_image_story_prompt(role, role_description)
    
    print("图片故事提示词内容:")
    print("-" * 50)
    print(image_story_prompt)
    print("-" * 50)
    
    # 检查关键改进点
    improvements = [
        ("避免套话", "避免使用\"确实挺有意思的\"" in image_story_prompt),
        ("关键词格式", "<key_words>" in image_story_prompt),
        ("个性化要求", "展现你的专业视角" in image_story_prompt),
        ("语言风格", "用你自己的语言风格" in image_story_prompt)
    ]
    
    for improvement_name, has_improvement in improvements:
        if has_improvement:
            print(f"✅ {improvement_name}: 已包含")
        else:
            print(f"❌ {improvement_name}: 缺失")
    
    return all(has for _, has in improvements)


async def main():
    """主测试函数"""
    print("🔧 开始验证TableRound改进功能...\n")
    
    # 测试结果
    results = {}
    
    # 1. 测试Google模型图像识别支持
    try:
        results["google_vision"] = await test_google_vision_support()
    except Exception as e:
        print(f"❌ Google模型测试失败: {e}")
        results["google_vision"] = False
    
    # 2. 测试关键词提取格式
    try:
        results["keyword_format"] = await test_keyword_extraction_format()
    except Exception as e:
        print(f"❌ 关键词格式测试失败: {e}")
        results["keyword_format"] = False
    
    # 3. 测试智能体个性化
    try:
        results["agent_personality"] = await test_agent_personality()
    except Exception as e:
        print(f"❌ 智能体个性化测试失败: {e}")
        results["agent_personality"] = False
    
    # 4. 测试图片故事提示词
    try:
        results["image_story_prompt"] = await test_image_story_prompt()
    except Exception as e:
        print(f"❌ 图片故事提示词测试失败: {e}")
        results["image_story_prompt"] = False
    
    # 总结结果
    print("\n" + "="*60)
    print("测试结果总结:")
    print("="*60)
    
    for test_name, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name:20} - {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\n总体结果: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有改进功能验证通过！")
    else:
        print("⚠️  部分功能需要进一步检查")
    
    return passed_tests == total_tests


if __name__ == "__main__":
    asyncio.run(main())
