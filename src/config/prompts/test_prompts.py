#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
提示词系统测试文件
用于验证新的模块化提示词管理系统
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from src.config.prompts import (
    PromptTemplates,  # 向后兼容接口
    prompt_manager,   # 新的管理器
    CraftsmanPrompts,
    ConsumerPrompts,
    ManufacturerPrompts,
    DesignerPrompts,
    KeywordExtractionPrompts,
    RoleSwitchPrompts,
    ScenarioPrompts,
    ImageStoryPrompts
)


def test_backward_compatibility():
    """测试向后兼容性"""
    print("=== 测试向后兼容性 ===")
    
    # 测试原有接口
    system_prompt = PromptTemplates.get_system_prompt("craftsman")
    print(f"系统提示词长度: {len(system_prompt)}")
    
    intro_prompt = PromptTemplates.get_introduction_prompt("consumer")
    print(f"自我介绍提示词长度: {len(intro_prompt)}")
    
    discussion_prompt = PromptTemplates.get_discussion_prompt("designer", "剪纸设计")
    print(f"讨论提示词长度: {len(discussion_prompt)}")
    
    keyword_prompt = PromptTemplates.get_keyword_extraction_prompt("测试内容", "测试主题")
    print(f"关键词提取提示词长度: {len(keyword_prompt)}")
    
    print("✅ 向后兼容性测试通过\n")


def test_new_manager():
    """测试新的管理器"""
    print("=== 测试新的管理器 ===")
    
    # 测试基础功能
    roles = prompt_manager.get_available_roles()
    print(f"可用角色: {roles}")
    
    # 测试高级关键词提取
    multilingual_prompt = prompt_manager.get_keyword_extraction_prompt(
        "测试内容 test content", "测试主题", extraction_type="multilingual"
    )
    print(f"多语言关键词提取提示词长度: {len(multilingual_prompt)}")
    
    # 测试场景提示词
    scenario_prompt = prompt_manager.get_scenario_prompt("paper_cutting_workshop")
    print(f"剪纸研讨会场景提示词长度: {len(scenario_prompt)}")
    
    print("✅ 新管理器测试通过\n")


def test_agent_prompts():
    """测试智能体专用提示词"""
    print("=== 测试智能体专用提示词 ===")
    
    # 测试手工艺人提示词
    craftsman_skills = CraftsmanPrompts.get_skills()
    print(f"手工艺人技能: {craftsman_skills}")
    
    design_eval = CraftsmanPrompts.get_design_evaluation_prompt("测试设计方案")
    print(f"设计评估提示词长度: {len(design_eval)}")
    
    # 测试消费者提示词
    consumer_types = ConsumerPrompts.get_consumer_types()
    print(f"消费者类型数量: {len(consumer_types)}")
    
    product_eval = ConsumerPrompts.get_product_evaluation_prompt("测试产品")
    print(f"产品评估提示词长度: {len(product_eval)}")
    
    # 测试制造商提示词
    manufacturer_skills = ManufacturerPrompts.get_skills()
    print(f"制造商技能: {manufacturer_skills}")
    
    feasibility = ManufacturerPrompts.get_production_feasibility_prompt("测试设计")
    print(f"生产可行性提示词长度: {len(feasibility)}")
    
    # 测试设计师提示词
    designer_skills = DesignerPrompts.get_skills()
    print(f"设计师技能: {designer_skills}")
    
    design_creation = DesignerPrompts.get_design_creation_prompt("测试需求", "测试主题")
    print(f"设计创作提示词长度: {len(design_creation)}")
    
    print("✅ 智能体专用提示词测试通过\n")


def test_function_prompts():
    """测试功能提示词"""
    print("=== 测试功能提示词 ===")
    
    # 测试关键词提取
    basic_extraction = KeywordExtractionPrompts.get_basic_extraction_prompt("内容", "主题")
    print(f"基础关键词提取提示词长度: {len(basic_extraction)}")
    
    hierarchical_extraction = KeywordExtractionPrompts.get_hierarchical_prompt("内容", "主题")
    print(f"层次化关键词提取提示词长度: {len(hierarchical_extraction)}")
    
    # 测试角色转换
    role_switch = RoleSwitchPrompts.get_basic_role_switch_prompt("craftsman", "designer", "主题")
    print(f"角色转换提示词长度: {len(role_switch)}")
    
    memory_preservation = RoleSwitchPrompts.get_memory_preservation_prompt("craftsman", "designer", "主题")
    print(f"记忆保持提示词长度: {len(memory_preservation)}")
    
    # 测试场景设置
    workshop_scenario = ScenarioPrompts.get_paper_cutting_workshop_scenario()
    print(f"研讨会场景提示词长度: {len(workshop_scenario)}")
    
    # 测试图片故事
    basic_story = ImageStoryPrompts.get_basic_image_story_prompt("craftsman", "角色描述")
    print(f"基础图片故事提示词长度: {len(basic_story)}")
    
    professional_story = ImageStoryPrompts.get_professional_image_story_prompt("designer")
    print(f"专业图片故事提示词长度: {len(professional_story)}")
    
    print("✅ 功能提示词测试通过\n")


def test_integration():
    """测试集成功能"""
    print("=== 测试集成功能 ===")
    
    # 测试完整的工作流程
    print("1. 获取系统提示词")
    system_prompt = prompt_manager.get_system_prompt("craftsman")
    print(f"   系统提示词: {system_prompt[:100]}...")
    
    print("2. 获取场景设置")
    scenario = prompt_manager.get_scenario_prompt("paper_cutting_workshop")
    print(f"   场景设置: {scenario[:100]}...")
    
    print("3. 获取讨论提示词")
    discussion = prompt_manager.get_discussion_prompt("craftsman", "剪纸文创产品设计")
    print(f"   讨论提示词: {discussion[:100]}...")
    
    print("4. 获取关键词提取提示词")
    keyword_extraction = prompt_manager.get_keyword_extraction_prompt(
        "讨论内容示例", "剪纸文创产品设计", extraction_type="hierarchical"
    )
    print(f"   关键词提取: {keyword_extraction[:100]}...")
    
    print("5. 获取角色转换提示词")
    role_switch = prompt_manager.get_role_switch_prompt("craftsman", "consumer", "剪纸文创产品设计")
    print(f"   角色转换: {role_switch[:100]}...")
    
    print("6. 获取图片故事提示词")
    image_story = prompt_manager.get_image_story_prompt("designer")
    print(f"   图片故事: {image_story[:100]}...")
    
    print("✅ 集成功能测试通过\n")


def main():
    """主测试函数"""
    print("🚀 开始测试TableRound提示词管理系统 v2.0\n")
    
    try:
        test_backward_compatibility()
        test_new_manager()
        test_agent_prompts()
        test_function_prompts()
        test_integration()
        
        print("🎉 所有测试通过！新的模块化提示词管理系统工作正常。")
        print("\n📊 系统统计:")
        print(f"   - 支持的智能体角色: {len(prompt_manager.get_available_roles())}")
        print(f"   - 智能体提示词模块: 4个 (craftsman, consumer, manufacturer, designer)")
        print(f"   - 功能提示词模块: 4个 (keyword_extraction, role_switch, scenario, image_story)")
        print(f"   - 关键词提取类型: 5种 (basic, domain, multilingual, hierarchical, sentiment)")
        print(f"   - 角色转换类型: 6种 (basic, professional, contextual, gradual, multi_dimensional, memory)")
        print(f"   - 场景类型: 7种 (workshop, launch, review, research, innovation, crisis, collaboration)")
        print(f"   - 图片故事类型: 7种 (basic, professional, emotional, cultural, creative, educational, multi_perspective)")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()