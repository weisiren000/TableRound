#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
命令行界面模块
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

from src.config.settings import Settings
from src.core.agent import Agent
from src.core.conversation import ConversationManager
from src.core.memory import Memory
from src.models.openai import OpenAIModel


async def start_cli(conversation_manager: ConversationManager, settings: Settings):
    """
    启动命令行界面

    Args:
        conversation_manager: 对话管理器
        settings: 全局设置
    """
    logger = logging.getLogger("cli")
    logger.info("启动命令行界面")

    print("\n" + "=" * 50)
    print("欢迎使用圆桌会议系统")
    print("=" * 50 + "\n")

    # 创建智能体
    await create_agents(conversation_manager, settings)

    while True:
        print("\n请选择操作:")
        print("1. 开始新对话")
        print("2. 处理图片")
        print("3. 设计剪纸文创产品")
        print("4. 退出")

        choice = input("\n请输入选项编号: ")

        if choice == "1":
            await start_conversation(conversation_manager)
        elif choice == "2":
            await process_image(conversation_manager)
        elif choice == "3":
            await design_paper_cutting(conversation_manager)
        elif choice == "4":
            print("\n感谢使用圆桌会议系统，再见！")
            break
        else:
            print("\n无效选项，请重新选择")


async def create_agents(conversation_manager: ConversationManager, settings: Settings):
    """
    创建智能体

    Args:
        conversation_manager: 对话管理器
        settings: 全局设置
    """
    logger = logging.getLogger("cli.create_agents")
    logger.info("创建智能体")

    try:
        # 创建模型
        model = settings.get_model_instance()
    except ValueError as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

    # 智能体类型映射
    agent_types = {
        "craftsman": "手工艺人",
        "consumer": "消费者",
        "manufacturer": "制造商人",
        "designer": "设计师"
    }

    # 创建智能体
    for agent_type, count in settings.agent_counts.items():
        for i in range(count):
            agent_id = f"{agent_type}_{i+1}"
            agent_name = f"{agent_types.get(agent_type, agent_type)}{i+1}"

            # 创建记忆模块（使用MemoryAdapter支持Redis）
            from src.core.memory_adapter import MemoryAdapter
            memory = MemoryAdapter(
                agent_id=agent_id,
                storage_type="auto",  # 自动选择最佳存储方式
                max_tokens=settings.memory_max_tokens,
                settings=settings
            )

            # 根据智能体类型创建不同的智能体
            if agent_type == "craftsman":
                from src.agents.craftsman import Craftsman
                agent = Craftsman(
                    agent_id=agent_id,
                    name=agent_name,
                    model=model,
                    memory=memory
                )
            elif agent_type == "consumer":
                from src.agents.consumer import Consumer
                agent = Consumer(
                    agent_id=agent_id,
                    name=agent_name,
                    model=model,
                    memory=memory
                )
            elif agent_type == "manufacturer":
                from src.agents.manufacturer import Manufacturer
                agent = Manufacturer(
                    agent_id=agent_id,
                    name=agent_name,
                    model=model,
                    memory=memory
                )
            elif agent_type == "designer":
                from src.agents.designer import Designer
                agent = Designer(
                    agent_id=agent_id,
                    name=agent_name,
                    model=model,
                    memory=memory
                )
            else:
                # 默认使用基类
                agent = Agent(
                    agent_id=agent_id,
                    agent_type=agent_type,
                    name=agent_name,
                    model=model,
                    memory=memory
                )

            # 添加到对话管理器
            await conversation_manager.add_agent(agent)

            logger.info(f"创建了智能体: {agent_name} ({agent_type})")

    # 统计各类型智能体数量
    craftsmen_count = sum(1 for agent in conversation_manager.agents.values() if agent.type == "craftsman")
    consumers_count = sum(1 for agent in conversation_manager.agents.values() if agent.type == "consumer")
    manufacturers_count = sum(1 for agent in conversation_manager.agents.values() if agent.type == "manufacturer")
    designers_count = sum(1 for agent in conversation_manager.agents.values() if agent.type == "designer")

    print(f"\n已创建 {len(conversation_manager.agents)} 个智能体:")
    print(f"- 手工艺人: {craftsmen_count}个")
    print(f"- 消费者: {consumers_count}个")
    print(f"- 制造商人: {manufacturers_count}个")
    print(f"- 设计师: {designers_count}个")


async def start_conversation(conversation_manager: ConversationManager):
    """
    开始新对话

    Args:
        conversation_manager: 对话管理器
    """
    logger = logging.getLogger("cli.start_conversation")

    print("\n" + "-" * 50)
    print("开始新对话")
    print("-" * 50 + "\n")

    # 输入主题
    topic = input("请输入讨论主题: ")
    if not topic:
        print("主题不能为空")
        return

    # 询问是否上传图片
    print("\n是否上传图片作为讨论参考? (y/n): ")
    upload_image = input().lower().strip() in ['y', 'yes']

    image_path = None
    if upload_image:
        image_path = input("请输入图片路径: ")
        if not os.path.exists(image_path):
            print(f"错误: 图片 {image_path} 不存在")
            image_path = None
        else:
            print(f"已选择图片: {image_path}")

    logger.info(f"开始新对话，主题: {topic}")

    # 开始对话
    print("\n正在开始对话...\n")
    await conversation_manager.start_conversation(topic, image_path)

    # 等待上帝输入关键词
    print("\n请输入最终关键词（用逗号分隔）:")
    final_keywords_input = input()
    final_keywords = [kw.strip() for kw in final_keywords_input.split(",") if kw.strip()]

    if not final_keywords:
        print("未输入关键词，使用投票结果")
        final_keywords = conversation_manager.voted_keywords

    # 开始角色转换阶段
    print("\n开始角色转换阶段...\n")
    await conversation_manager.start_role_switch(final_keywords)

    # 等待用户输入设计提示词
    if conversation_manager.stage == "waiting_for_user_input":
        print("\n请输入设计提示词（用逗号分隔）:")
        design_prompt = input()

        # 处理用户输入，生成图像
        await conversation_manager.process_user_input(design_prompt)

    print("\n对话结束")


async def process_image(conversation_manager: ConversationManager):
    """
    处理图片

    Args:
        conversation_manager: 对话管理器
    """
    logger = logging.getLogger("cli.process_image")

    print("\n" + "-" * 50)
    print("处理图片")
    print("-" * 50 + "\n")

    # 输入图片路径
    image_path = input("请输入图片路径: ")
    if not os.path.exists(image_path):
        print(f"错误: 图片 {image_path} 不存在")
        return

    logger.info(f"处理图片: {image_path}")

    # 处理图片
    print("\n正在处理图片...\n")
    keywords = await conversation_manager.process_image(image_path)

    print(f"\n提取的关键词: {', '.join(keywords)}")


async def design_paper_cutting(conversation_manager: ConversationManager):
    """
    设计剪纸文创产品

    Args:
        conversation_manager: 对话管理器
    """
    logger = logging.getLogger("cli.design_paper_cutting")

    print("\n" + "-" * 50)
    print("设计剪纸文创产品")
    print("-" * 50 + "\n")

    # 输入关键词
    keywords_input = input("请输入关键词（用逗号分隔）: ")
    keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]

    if not keywords:
        print("未输入关键词")
        return

    logger.info(f"设计剪纸文创产品，关键词: {keywords}")

    # 设计剪纸产品
    print("\n正在设计剪纸文创产品...\n")
    designs = await conversation_manager.design_paper_cutting(keywords)

    # 输入设计提示词
    print("\n请输入设计提示词（用于生成图像）:")
    design_prompt = input()
    if not design_prompt:
        print("未输入设计提示词，使用默认提示词")
        design_prompt = "传统中国红色调，对称蝙蝠图案，吉祥如意"

    # 生成设计图
    print("\n正在生成设计图...")
    from src.utils.image import ImageProcessor
    image_processor = ImageProcessor(conversation_manager.settings)

    # 选择图像生成提供商
    print("\n请选择图像生成提供商:")
    print("1. OpenAI (DALL-E)")
    print("2. 豆包 (Doubao)")
    provider_choice = input("请输入选择 (默认: 2): ")

    provider = "doubao"
    if provider_choice == "1":
        provider = "openai"

    # 生成图像
    image_path = await image_processor.generate_image(design_prompt, provider=provider)

    if image_path:
        print(f"\n设计图已生成: {image_path}")
    else:
        print("\n设计图生成失败")
        return

    # 用户上传原型
    print("\n请输入您的原型设计图片路径（留空跳过）:")
    user_prototype_path = input()

    if user_prototype_path and os.path.exists(user_prototype_path):
        print("\n您想要如何处理原型图片?")
        print("1. 合并两张图片")
        print("2. 基于原型图片生成新图片")
        process_choice = input("请输入选择 (默认: 1): ")

        if process_choice == "2":
            print("\n正在基于原型图片生成新图片...")
            print("请输入提示词（留空使用默认提示词）:")
            variation_prompt = input()
            if not variation_prompt:
                variation_prompt = "基于参考图像，生成对称的剪纸风格的中国传统蝙蝠吉祥纹样，保持原图的风格和元素"

            # 基于原型图片生成新图片
            variation_image_path = await image_processor.generate_image_from_image(
                user_prototype_path, variation_prompt, provider="doubao"
            )

            if variation_image_path:
                print(f"\n基于原型的新设计已生成: {variation_image_path}")

                # 合并原始设计和基于原型的新设计
                print("\n正在合并设计...")
                merged_image_path = image_processor.merge_images(image_path, variation_image_path)

                if merged_image_path:
                    print(f"\n最终设计已生成: {merged_image_path}")
                else:
                    print("\n最终设计合并失败")
            else:
                print("\n基于原型的新设计生成失败")
        else:
            # 直接合并两张图片
            print("\n正在合并原型设计...")
            merged_image_path = image_processor.merge_images(image_path, user_prototype_path)

            if merged_image_path:
                print(f"\n最终设计已生成: {merged_image_path}")
            else:
                print("\n最终设计生成失败")

    print("\n设计流程完成")


if __name__ == "__main__":
    # 直接运行此文件时的测试代码
    from src.config.settings import Settings
    from src.core.conversation import ConversationManager
    from src.core.god_view import GodView
    from src.utils.logger import setup_logger

    # 设置日志
    setup_logger(logging.INFO)

    # 加载设置
    settings = Settings()

    # 创建上帝视角
    god_view = GodView(settings)

    # 创建对话管理器
    conversation_manager = ConversationManager(god_view, settings)

    # 启动命令行界面
    asyncio.run(start_cli(conversation_manager, settings))
