#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试角色扮演和用户交互功能
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 添加项目根目录到系统路径
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT_DIR))

from src.config.settings import Settings
from src.core.conversation import ConversationManager
from src.core.god_view import GodView
from src.core.agent import Agent
from src.core.memory import Memory
from src.models.mock import MockModel


async def test_role_switch():
    """测试角色转换功能"""
    print("测试角色转换功能")
    print("-" * 30)

    # 创建设置
    settings = Settings()

    # 创建模型
    model = MockModel()

    # 创建上帝视角
    god_view = GodView(settings)

    # 创建对话管理器
    conversation_manager = ConversationManager(god_view, settings)

    # 创建智能体
    agent_types = ["craftsman", "consumer", "manufacturer", "designer"]
    for i, agent_type in enumerate(agent_types):
        agent_id = f"{agent_type}_{i+1}"
        agent_name = f"测试{agent_type}{i+1}"

        # 创建记忆模块
        memory = Memory(agent_id=agent_id)

        # 创建智能体
        agent = Agent(
            agent_id=agent_id,
            agent_type=agent_type,
            name=agent_name,
            model=model,
            memory=memory
        )

        # 添加到对话管理器
        conversation_manager.add_agent(agent)

    # 测试角色转换
    print("开始角色转换测试...")

    # 获取第一个智能体
    agent = list(conversation_manager.agents.values())[0]
    original_role = agent.current_role
    new_role = "designer" if original_role != "designer" else "craftsman"

    # 执行角色转换
    response = await agent.switch_role(new_role, "测试主题")

    print(f"智能体 {agent.name} 从 {original_role} 转换为 {new_role}")
    print(f"角色转换后的自我介绍: {response}")

    # 验证角色转换
    assert agent.current_role == new_role, f"角色转换失败: {agent.current_role} != {new_role}"
    print("角色转换测试通过!")


async def test_paper_cutting_scenario():
    """测试剪纸研讨会场景设置"""
    print("\n测试剪纸研讨会场景设置")
    print("-" * 30)

    # 创建设置
    settings = Settings()

    # 创建模型
    model = MockModel()

    # 创建上帝视角
    god_view = GodView(settings)

    # 创建对话管理器
    conversation_manager = ConversationManager(god_view, settings)

    # 创建智能体
    agent_types = ["craftsman", "consumer", "manufacturer", "designer"]
    for i, agent_type in enumerate(agent_types):
        agent_id = f"{agent_type}_{i+1}"
        agent_name = f"测试{agent_type}{i+1}"

        # 创建记忆模块
        memory = Memory(agent_id=agent_id)

        # 创建智能体
        agent = Agent(
            agent_id=agent_id,
            agent_type=agent_type,
            name=agent_name,
            model=model,
            memory=memory
        )

        # 添加到对话管理器
        conversation_manager.add_agent(agent)

    # 设置对话主题和关键词
    conversation_manager.topic = "剪纸文创产品设计"
    conversation_manager.final_keywords = ["传统", "对称", "蝙蝠", "吉祥", "红色"]

    # 测试剪纸研讨会场景设置
    print("开始剪纸研讨会场景测试...")

    # 模拟流式输出处理器
    class MockStreamHandler:
        async def stream_output(self, text):
            print(text)

    conversation_manager.stream_handler = MockStreamHandler()

    # 执行角色转换后的讨论
    await conversation_manager.start_discussion_after_switch()

    # 验证讨论历史
    scenario_settings = [item for item in conversation_manager.discussion_history if item.get("stage") == "scenario_setting"]
    assert len(scenario_settings) > 0, "剪纸研讨会场景设置失败"

    discussions = [item for item in conversation_manager.discussion_history if item.get("stage") == "discussion_after_switch"]
    assert len(discussions) > 0, "角色转换后的讨论失败"

    print("剪纸研讨会场景测试通过!")


async def test_user_input():
    """测试用户输入接口"""
    print("\n测试用户输入接口")
    print("-" * 30)

    # 创建设置
    settings = Settings()

    # 创建模型
    model = MockModel()

    # 创建上帝视角
    god_view = GodView(settings)

    # 创建对话管理器
    conversation_manager = ConversationManager(god_view, settings)

    # 创建智能体
    agent_types = ["craftsman", "consumer", "manufacturer", "designer"]
    for i, agent_type in enumerate(agent_types):
        agent_id = f"{agent_type}_{i+1}"
        agent_name = f"测试{agent_type}{i+1}"

        # 创建记忆模块
        memory = Memory(agent_id=agent_id)

        # 创建智能体
        agent = Agent(
            agent_id=agent_id,
            agent_type=agent_type,
            name=agent_name,
            model=model,
            memory=memory
        )

        # 添加到对话管理器
        conversation_manager.add_agent(agent)

    # 设置对话主题和关键词
    conversation_manager.topic = "剪纸文创产品设计"
    conversation_manager.design_keywords = ["传统", "对称", "蝙蝠", "吉祥", "红色"]

    # 测试用户输入接口
    print("开始用户输入接口测试...")

    # 模拟流式输出处理器
    class MockStreamHandler:
        async def stream_output(self, text):
            print(text)

    conversation_manager.stream_handler = MockStreamHandler()

    # 执行用户输入处理
    user_input = "传统中国红色调，对称蝙蝠图案，吉祥如意"
    design_cards = await conversation_manager.process_user_input(user_input)

    # 验证设计卡牌
    assert design_cards is not None, "设计卡牌生成失败"
    assert len(design_cards) > 0, "设计卡牌为空"

    # 验证讨论历史
    design_cards_history = [item for item in conversation_manager.discussion_history if item.get("stage") == "design_card"]
    assert len(design_cards_history) > 0, "设计卡牌历史记录失败"

    print("用户输入接口测试通过!")


if __name__ == "__main__":
    # 运行测试
    print("开始测试...")
    try:
        asyncio.run(test_role_switch())
        print("角色转换测试完成")

        asyncio.run(test_paper_cutting_scenario())
        print("剪纸研讨会场景测试完成")

        asyncio.run(test_user_input())
        print("用户输入接口测试完成")

        print("\n所有测试通过!")
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
