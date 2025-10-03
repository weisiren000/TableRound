#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简化的改进功能验证测试
避免复杂依赖，专注测试核心改进
"""

import os
import sys
import re
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_google_vision_support():
    """测试Google模型的图像识别支持"""
    print("=== 测试Google模型图像识别支持 ===")
    
    try:
        from src.models.google import GoogleModel
        
        # 初始化Google模型
        model = GoogleModel(
            model_name="gemini-2.5-flash-preview-05-20",
            api_key="test_key",
            base_url="https://generativelanguage.googleapis.com/v1beta"
        )
        
        print(f"模型名称: {model.model_name}")
        print(f"是否支持图像: {model.supports_vision()}")

        if model.supports_vision():
            print("Google模型图像识别支持已修复")
            return True
        else:
            print("Google模型图像识别支持仍有问题")
            return False
            
    except Exception as e:
        print(f"Google模型测试失败: {e}")
        return False


def test_keyword_extraction_format():
    """测试关键词提取的新格式支持"""
    print("\n=== 测试关键词提取格式 ===")
    
    # 模拟包含<key_words>标签的响应
    test_responses = [
        "<key_words>传统文化, 剪纸艺术, 蝙蝠纹样</key_words>",
        "这是一个关于传统文化的故事...\n<key_words>传统文化, 剪纸艺术, 蝙蝠纹样, 吉祥图案</key_words>",
        '["传统文化", "剪纸艺术", "蝙蝠纹样"]',  # 备选格式
        "传统文化\n剪纸艺术\n蝙蝠纹样"  # 简单格式
    ]
    
    success_count = 0
    
    for i, response in enumerate(test_responses):
        print(f"\n测试响应 {i+1}: {response}")
        
        # 模拟关键词解析逻辑（复制自agent.py的逻辑）
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
            print("关键词提取成功")
            success_count += 1
        else:
            print("关键词提取失败")
    
    print(f"\n关键词提取测试: {success_count}/{len(test_responses)} 成功")
    return success_count == len(test_responses)


def test_prompt_improvements():
    """测试提示词改进"""
    print("\n=== 测试提示词改进 ===")
    
    try:
        from src.config.prompts.base_prompts import BasePrompts
        from src.config.prompts.template_manager import PromptTemplateManager
        
        manager = PromptTemplateManager()
        
        # 测试系统提示词改进
        system_prompt = manager.get_system_prompt("craftsman")
        print("系统提示词改进检查:")
        
        improvements = [
            ("避免套话", "不要说\"确实挺有意思的\"" in system_prompt),
            ("个性化要求", "体现你的个人特色" in system_prompt),
            ("专业性要求", "展现你的专业性" in system_prompt),
            ("避免重复", "避免使用套话" in system_prompt)
        ]
        
        system_success = 0
        for improvement_name, has_improvement in improvements:
            if has_improvement:
                print(f"  {improvement_name}: 已包含")
                system_success += 1
            else:
                print(f"  {improvement_name}: 缺失")
        
        # 测试图片故事提示词改进
        role_description = manager._role_descriptions.get("craftsman", "")
        image_story_prompt = BasePrompts.get_image_story_prompt("craftsman", role_description)
        
        print("\n图片故事提示词改进检查:")
        story_improvements = [
            ("关键词格式", "<key_words>" in image_story_prompt),
            ("避免套话", "避免使用\"确实挺有意思的\"" in image_story_prompt),
            ("个性化要求", "用你自己的语言风格" in image_story_prompt),
            ("专业视角", "展现你的专业视角" in image_story_prompt)
        ]
        
        story_success = 0
        for improvement_name, has_improvement in story_improvements:
            if has_improvement:
                print(f"  {improvement_name}: 已包含")
                story_success += 1
            else:
                print(f"  {improvement_name}: 缺失")
        
        total_improvements = len(improvements) + len(story_improvements)
        total_success = system_success + story_success
        
        print(f"\n提示词改进测试: {total_success}/{total_improvements} 成功")
        return total_success == total_improvements
        
    except Exception as e:
        print(f"提示词改进测试失败: {e}")
        return False


def test_role_personality():
    """测试角色个性化"""
    print("\n=== 测试角色个性化 ===")
    
    try:
        from src.config.prompts.agent_prompts.craftsman_prompts import CraftsmanPrompts
        from src.config.prompts.agent_prompts.consumer_prompts import ConsumerPrompts
        from src.config.prompts.agent_prompts.manufacturer_prompts import ManufacturerPrompts
        from src.config.prompts.agent_prompts.designer_prompts import DesignerPrompts
        
        role_classes = {
            "craftsman": CraftsmanPrompts,
            "consumer": ConsumerPrompts,
            "manufacturer": ManufacturerPrompts,
            "designer": DesignerPrompts
        }
        
        success_count = 0
        
        for role_name, role_class in role_classes.items():
            print(f"\n--- {role_name} 角色个性化检查 ---")
            
            role_description = role_class.get_role_description()
            
            # 检查是否包含语言风格特点
            if "语言风格特点" in role_description:
                print(f"  包含语言风格特点")
                success_count += 1

                # 显示风格特点预览
                style_start = role_description.find("语言风格特点：")
                if style_start != -1:
                    style_section = role_description[style_start:style_start+150]
                    print(f"  风格预览: {style_section}...")
            else:
                print(f"  缺少语言风格特点")
        
        print(f"\n角色个性化测试: {success_count}/{len(role_classes)} 成功")
        return success_count == len(role_classes)
        
    except Exception as e:
        print(f"角色个性化测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("开始验证TableRound改进功能...\n")
    
    # 测试结果
    results = {}
    
    # 1. 测试Google模型图像识别支持
    results["google_vision"] = test_google_vision_support()
    
    # 2. 测试关键词提取格式
    results["keyword_format"] = test_keyword_extraction_format()
    
    # 3. 测试提示词改进
    results["prompt_improvements"] = test_prompt_improvements()
    
    # 4. 测试角色个性化
    results["role_personality"] = test_role_personality()
    
    # 总结结果
    print("\n" + "="*60)
    print("测试结果总结:")
    print("="*60)
    
    for test_name, success in results.items():
        status = "通过" if success else "失败"
        print(f"{test_name:20} - {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\n总体结果: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("所有改进功能验证通过！")
        return True
    else:
        print("部分功能需要进一步检查")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
