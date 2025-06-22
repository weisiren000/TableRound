#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
命令行界面模块 - 美化版本
"""

import asyncio
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

from src.config.settings import Settings
from src.core.agent import Agent
from src.core.conversation import ConversationManager
from src.models.openai import OpenAIModel

# 导入UI美化组件
from src.ui_enhanced import (
    EnhancedColors, Icons, ASCIIArt, Decorations,
    UIComponents, Panel, ProgressBar, Menu, StatusIndicator, AgentCard,
    Animations, LoadingSpinner, ProgressTracker,
    ThemeManager, theme_manager, primary, secondary, success, warning, error, info, text, muted, accent
)


async def start_cli(conversation_manager: ConversationManager, settings: Settings):
    """
    启动命令行界面 - 美化版本

    Args:
        conversation_manager: 对话管理器
        settings: 全局设置
    """
    logger = logging.getLogger("cli")
    logger.info("启动命令行界面")

    # 显示欢迎界面
    show_welcome_screen()

    # 创建智能体（带进度显示）
    await create_agents_with_progress(conversation_manager, settings)

    # 主菜单循环
    while True:
        show_main_menu()
        choice = get_user_choice()

        if choice == "1":
            await start_conversation(conversation_manager)
        elif choice == "2":
            await process_image(conversation_manager)
        elif choice == "3":
            await design_paper_cutting(conversation_manager)
        elif choice == "4":
            show_goodbye_screen()
            break
        elif choice == "t":
            show_theme_selector()
        elif choice == "s":
            await show_special_effects_demo()
        else:
            show_invalid_choice()


def show_welcome_screen():
    """显示增强版欢迎界面"""
    UIComponents.clear_screen()

    # 显示完整Logo（渐变色）
    logo_text = ASCIIArt.TABLEROUND_LOGO
    colored_logo = EnhancedColors.gradient_text(
        logo_text,
        (0, 150, 255),  # 蓝色
        (255, 100, 150)  # 粉色
    )
    print(colored_logo)

    # 装饰性分隔线
    separator = EnhancedColors.rainbow_text(Decorations.create_separator(60, "═"))
    print(separator)
    print()

    # 欢迎信息面板
    welcome_panel = Panel("欢迎使用圆桌会议智能体系统", 60)
    welcome_panel.add_line(f"{Icons.STAR} {primary('多智能体协作讨论平台')}")
    welcome_panel.add_line(f"{Icons.CRAFTSMAN} {secondary('支持手工艺人、消费者、制造商、设计师')}")
    welcome_panel.add_line(f"{Icons.DESIGNER} {info('智能图像处理与创意设计')}")
    welcome_panel.add_line(f"{Icons.DIAMOND} {accent('基于Redis的统一内存架构')}")
    welcome_panel.add_line(f"{Icons.HEART} {success('全新美化界面体验')}")

    print(welcome_panel.render())
    print()

    # 打字机效果初始化提示
    Animations.typewriter_effect(
        primary("正在初始化增强版UI系统..."),
        delay=0.03
    )


def show_main_menu():
    """显示增强版主菜单"""
    # 创建装饰性分隔线
    separator = EnhancedColors.rainbow_text(Decorations.create_separator(60, "═"))
    print(separator)
    print()

    # 使用装饰性标题框
    title_box = Decorations.create_title_box("🎯 TableRound 主菜单", 50)
    colored_title_box = EnhancedColors.bright_cyan(title_box)
    print(colored_title_box)
    print()

    # 增强版菜单选项
    menu_options = [
        (f"{Icons.CRAFTSMAN} [1]", "开始新对话", "启动多智能体圆桌讨论", primary),
        (f"{Icons.DESIGNER} [2]", "处理图片", "上传图片进行智能分析", secondary),
        (f"{Icons.STAR} [3]", "设计剪纸文创", "基于关键词设计文创产品", accent),
        (f"{Icons.HEART} [t]", "切换主题", "更改界面主题风格", warning),
        (f"{Icons.DIAMOND} [s]", "特效演示", "查看所有美化特效", info),
        (f"{Icons.ARROW_RIGHT} [4]", "退出系统", "安全退出程序", error)
    ]

    for icon_key, title, desc, color_func in menu_options:
        print(f"  {color_func(icon_key)} {color_func(title)}")
        print(f"    {muted(desc)}")
        print()

    # 底部装饰线
    bottom_separator = EnhancedColors.bright_blue(Decorations.create_separator(60, "─"))
    print(bottom_separator)


def get_user_choice() -> str:
    """获取用户选择"""
    prompt = primary("请输入选项编号: ")
    return input(prompt).strip()


def show_invalid_choice():
    """显示无效选择提示"""
    print()
    print(StatusIndicator.warning("无效选项，请重新选择"))
    time.sleep(1)


async def show_special_effects_demo():
    """显示特效演示"""
    UIComponents.clear_screen()

    print(EnhancedColors.rainbow_text("🌈 特效演示中心"))
    print(EnhancedColors.bright_cyan(Decorations.create_separator(50, "=")))
    print()

    # 1. 加载动画演示
    print(primary("1. 加载动画效果:"))
    for i in range(20):
        frame = ASCIIArt.get_loading_frame(i)
        colored_frame = EnhancedColors.bright_cyan(frame)
        print(f"\r{colored_frame} 特效加载中...", end="", flush=True)
        await asyncio.sleep(0.1)
    print("\r" + success("✓ 加载完成") + " " * 15)
    print()

    # 2. 进度条演示
    print(primary("2. 进度条效果:"))
    for style in ["classic", "dots", "blocks"]:
        print(f"  {style.capitalize()}:")
        bar = ASCIIArt.create_progress_bar(0.75, 25, style)
        colored_bar = EnhancedColors.bright_green(bar)
        print(f"    [{colored_bar}] 75%")
    print()

    # 3. 文字特效演示
    print(primary("3. 文字特效:"))
    print("  波浪效果:")
    Animations.wave_text("🌊 TableRound 🌊", waves=1, delay=0.1)

    print("  弹跳效果:")
    Animations.bounce_text("⚡ 智能体系统 ⚡", bounces=1, delay=0.15)
    print()

    # 4. 装饰元素演示
    print(primary("4. 装饰元素:"))
    decorative_content = f"{Icons.STAR} 精美边框\n{Icons.HEART} 丰富图标\n{Icons.DIAMOND} 多彩文字"
    decorative_panel = Decorations.create_panel(decorative_content, "装饰展示", 30)
    print(EnhancedColors.bright_yellow(decorative_panel))
    print()

    UIComponents.wait_for_input("按回车键返回主菜单...")


def show_goodbye_screen():
    """显示告别界面"""
    UIComponents.clear_screen()

    # 使用装饰性标题框
    goodbye_title = Decorations.create_title_box("感谢使用 TableRound 系统", 50)
    print(EnhancedColors.bright_magenta(goodbye_title))
    print()

    goodbye_panel = Panel("再见", 40)
    goodbye_panel.add_line(f"{Icons.STAR} {success('感谢使用圆桌会议系统!')}")
    goodbye_panel.add_line(f"{Icons.HEART} {muted('期待下次再见')} 👋")
    goodbye_panel.add_line(f"{Icons.DIAMOND} {muted('系统正在安全退出...')}")

    print(goodbye_panel.render())
    print()

    # 退出动画
    Animations.fade_in_text(accent("再见！👋"), steps=5, delay=0.2)


def show_theme_selector():
    """显示主题选择器"""
    UIComponents.clear_screen()

    themes = theme_manager.list_themes()
    current_theme = theme_manager.current_theme.name

    theme_panel = Panel("🎭 主题选择", 50)
    theme_panel.add_line(f"当前主题: {primary(current_theme)}")
    theme_panel.add_separator()

    for i, theme_name in enumerate(themes, 1):
        if theme_name == current_theme:
            theme_panel.add_line(f"{i}. {success(theme_name)} {accent('(当前)')}")
        else:
            theme_panel.add_line(f"{i}. {text(theme_name)}")

    print(theme_panel.render())
    print()

    try:
        choice = input(primary("请选择主题编号 (回车返回): ")).strip()
        if choice and choice.isdigit():
            theme_index = int(choice) - 1
            if 0 <= theme_index < len(themes):
                theme_name = themes[theme_index]
                if theme_manager.set_theme(theme_name):
                    print(StatusIndicator.success(f"已切换到 {theme_name} 主题"))
                    time.sleep(1)
                else:
                    print(StatusIndicator.error("主题切换失败"))
                    time.sleep(1)
    except ValueError:
        pass


async def create_agents_with_progress(conversation_manager: ConversationManager, settings: Settings):
    """
    创建智能体（带进度显示）

    Args:
        conversation_manager: 对话管理器
        settings: 全局设置
    """
    logger = logging.getLogger("cli.create_agents")
    logger.info("创建智能体")

    try:
        # 创建模型
        print(StatusIndicator.info("正在初始化AI模型..."))
        model = settings.get_model_instance()
        print(StatusIndicator.success("AI模型初始化完成"))
    except ValueError as e:
        print(StatusIndicator.error(f"模型初始化失败: {str(e)}"))
        sys.exit(1)

    # 智能体类型映射
    agent_types = {
        "craftsman": "手工艺人",
        "consumer": "消费者",
        "manufacturer": "制造商人",
        "designer": "设计师"
    }

    # 计算总数
    total_agents = sum(settings.agent_counts.values())

    # 显示创建工厂面板
    factory_panel = Decorations.create_panel(
        "正在创建智能体团队...\n使用最新AI技术构建专业团队",
        "🤖 智能体工厂",
        55
    )
    print(EnhancedColors.bright_blue(factory_panel))
    print()

    progress_tracker = ProgressTracker(total_agents, "创建智能体", 40)

    created_count = 0
    agent_cards = []

    # 创建智能体
    for agent_type, count in settings.agent_counts.items():
        for i in range(count):
            agent_id = f"{agent_type}_{i+1}"
            agent_name = f"{agent_types.get(agent_type, agent_type)}{i+1}"

            progress_tracker.update(created_count, f"创建 {agent_name}")

            # 创建记忆模块（使用Redis统一存储）
            from src.core.memory_adapter import MemoryAdapter
            memory = MemoryAdapter(
                agent_id=agent_id,
                storage_type="redis",  # 统一使用Redis存储
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

            # 创建智能体卡片
            card = AgentCard(agent_name, agent_type, "ready")
            agent_cards.append(card)

            logger.info(f"创建了智能体: {agent_name} ({agent_type})")

            # 显示创建成功信息
            icon = Icons.get_agent_icon(agent_type)
            print(f"\r{' ' * 60}\r{success('✓')} {icon} {agent_name} 创建成功")

            created_count += 1

    progress_tracker.finish("智能体团队创建完成")
    print()

    # 显示智能体总览
    show_agents_summary(conversation_manager, agent_cards)


def show_agents_summary(conversation_manager: ConversationManager, agent_cards: List[AgentCard]):
    """显示增强版智能体总览"""

    # 统计各类型智能体数量
    craftsmen_count = sum(1 for agent in conversation_manager.agents.values() if agent.type == "craftsman")
    consumers_count = sum(1 for agent in conversation_manager.agents.values() if agent.type == "consumer")
    manufacturers_count = sum(1 for agent in conversation_manager.agents.values() if agent.type == "manufacturer")
    designers_count = sum(1 for agent in conversation_manager.agents.values() if agent.type == "designer")

    # 使用装饰性面板
    team_summary = f"""{Icons.CRAFTSMAN} 手工艺人: {success(str(craftsmen_count))}个
{Icons.CONSUMER} 消费者: {info(str(consumers_count))}个
{Icons.MANUFACTURER} 制造商: {warning(str(manufacturers_count))}个
{Icons.DESIGNER} 设计师: {accent(str(designers_count))}个

{Icons.STAR} {primary('总计:')} {success(str(len(conversation_manager.agents)))} {primary('个专业智能体')}"""

    summary_panel = Decorations.create_panel(team_summary, "🎯 团队配置", 50)
    print(EnhancedColors.bright_white(summary_panel))
    print()

    # 装饰性分隔线
    separator = EnhancedColors.bright_green(Decorations.create_separator(50, "─"))
    print(separator)

    # 等待用户确认
    UIComponents.wait_for_input(f"{Icons.ARROW_RIGHT} 智能体团队已就绪，按回车键继续...")


async def create_agents(conversation_manager: ConversationManager, settings: Settings):
    """
    创建智能体（兼容性保留）
    """
    await create_agents_with_progress(conversation_manager, settings)


async def start_conversation(conversation_manager: ConversationManager):
    """
    开始新对话

    Args:
        conversation_manager: 对话管理器
    """
    logger = logging.getLogger("cli.start_conversation")

    UIComponents.print_header("💬 开始新对话", "多智能体圆桌讨论")

    # 输入主题
    topic_panel = Panel("📝 讨论主题设置", 60)
    topic_panel.add_line("请输入您想要讨论的主题：")
    print(topic_panel.render())
    print()

    topic = input(primary("主题: ")).strip()
    if not topic:
        print(StatusIndicator.error("主题不能为空"))
        UIComponents.wait_for_input()
        return

    print(StatusIndicator.success(f"主题已设置: {topic}"))

    # 询问是否上传图片
    print()
    image_panel = Panel("🖼️ 图片参考（可选）", 60)
    image_panel.add_line("您可以上传图片作为讨论的参考资料")
    print(image_panel.render())
    print()

    upload_choice = input(primary("是否上传图片? (y/n): ")).lower().strip()
    upload_image = upload_choice in ['y', 'yes', '是']

    image_path = None
    if upload_image:
        image_path = input(secondary("请输入图片路径: ")).strip()
        if not os.path.exists(image_path):
            print(StatusIndicator.error(f"图片文件不存在: {image_path}"))
            image_path = None
        else:
            print(StatusIndicator.success(f"已选择图片: {image_path}"))

    logger.info(f"开始新对话，主题: {topic}")

    # 开始对话
    print()
    conversation_panel = Panel("🎯 圆桌讨论进行中", 60)
    conversation_panel.add_line("智能体们正在热烈讨论中...")
    conversation_panel.add_line("请耐心等待讨论结果")
    print(conversation_panel.render())
    print()

    # 不使用加载动画，避免干扰流式输出
    await conversation_manager.start_conversation(topic, image_path)

    print()
    print(StatusIndicator.success("讨论阶段完成"))

    # 等待上帝输入关键词
    print()
    keywords_panel = Panel("🔑 关键词确认", 60)
    keywords_panel.add_line("请输入最终关键词（用逗号分隔）：")
    keywords_panel.add_line(muted("留空将使用智能体投票结果"))
    print(keywords_panel.render())
    print()

    final_keywords_input = input(primary("关键词: ")).strip()
    final_keywords = [kw.strip() for kw in final_keywords_input.split(",") if kw.strip()]

    if not final_keywords:
        print(StatusIndicator.info("使用智能体投票结果"))
        final_keywords = conversation_manager.voted_keywords
    else:
        print(StatusIndicator.success(f"已设置关键词: {', '.join(final_keywords)}"))

    # 开始角色转换阶段
    print()
    role_switch_panel = Panel("🔄 角色转换阶段", 60)
    role_switch_panel.add_line("智能体们正在切换到专业角色...")
    print(role_switch_panel.render())
    print()

    # 不使用加载动画，避免干扰流式输出
    await conversation_manager.start_role_switch(final_keywords)

    print()
    print(StatusIndicator.success("角色转换完成"))

    # 等待用户输入设计提示词
    if conversation_manager.stage == "waiting_for_user_input":
        print()
        design_panel = Panel("🎨 设计提示词", 60)
        design_panel.add_line("请输入设计提示词来生成最终作品：")
        print(design_panel.render())
        print()

        design_prompt = input(primary("设计提示词: ")).strip()

        if design_prompt:
            # 处理用户输入，生成图像
            print()
            print(StatusIndicator.info("正在生成设计..."))

            await conversation_manager.process_user_input(design_prompt)

            print()
            print(StatusIndicator.success("设计生成完成"))

    print()
    completion_panel = Panel("✅ 对话完成", 50)
    completion_panel.add_line(success("圆桌讨论已成功完成！"))
    completion_panel.add_line(muted("感谢您的参与"))
    print(completion_panel.render())

    UIComponents.wait_for_input()


async def process_image(conversation_manager: ConversationManager):
    """
    处理图片

    Args:
        conversation_manager: 对话管理器
    """
    logger = logging.getLogger("cli.process_image")

    UIComponents.print_header("🖼️ 图片智能分析", "AI图像识别与关键词提取")

    # 输入图片路径
    input_panel = Panel("📁 选择图片文件", 60)
    input_panel.add_line("请输入要分析的图片文件路径：")
    input_panel.add_line(muted("支持 JPG、PNG、GIF 等常见格式"))
    print(input_panel.render())
    print()

    image_path = input(primary("图片路径: ")).strip()
    if not os.path.exists(image_path):
        print(StatusIndicator.error(f"图片文件不存在: {image_path}"))
        UIComponents.wait_for_input()
        return

    print(StatusIndicator.success(f"已选择图片: {image_path}"))
    logger.info(f"处理图片: {image_path}")

    # 处理图片
    print()
    process_panel = Panel("🔍 AI分析进行中", 60)
    process_panel.add_line("正在使用AI技术分析图片内容...")
    process_panel.add_line("提取关键特征和语义信息...")
    print(process_panel.render())

    spinner = LoadingSpinner("图片分析中", "spinner")
    spinner.start()

    try:
        keywords = await conversation_manager.process_image(image_path)
    finally:
        spinner.stop()

    # 显示结果
    print()
    result_panel = Panel("✨ 分析结果", 60)
    result_panel.add_line(f"提取的关键词: {success(', '.join(keywords))}")
    result_panel.add_line(f"关键词数量: {info(str(len(keywords)))}")
    print(result_panel.render())

    UIComponents.wait_for_input()


async def design_paper_cutting(conversation_manager: ConversationManager):
    """
    设计剪纸文创产品

    Args:
        conversation_manager: 对话管理器
    """
    logger = logging.getLogger("cli.design_paper_cutting")

    UIComponents.print_header("🎨 剪纸文创设计", "AI驱动的传统文化创新")

    # 输入关键词
    keywords_panel = Panel("🔑 设计关键词", 60)
    keywords_panel.add_line("请输入设计关键词来指导创作方向：")
    keywords_panel.add_line(muted("多个关键词请用逗号分隔，如：蝙蝠,吉祥,红色"))
    print(keywords_panel.render())
    print()

    keywords_input = input(primary("关键词: ")).strip()
    keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]

    if not keywords:
        print(StatusIndicator.error("关键词不能为空"))
        UIComponents.wait_for_input()
        return

    print(StatusIndicator.success(f"设计关键词: {', '.join(keywords)}"))
    logger.info(f"设计剪纸文创产品，关键词: {keywords}")

    # 设计剪纸产品
    print()
    design_panel = Panel("🎯 创意设计阶段", 60)
    design_panel.add_line("AI正在基于关键词进行创意设计...")
    design_panel.add_line("融合传统剪纸工艺与现代美学")
    print(design_panel.render())
    print()

    # 不使用加载动画，避免干扰流式输出
    designs = await conversation_manager.design_paper_cutting(keywords)

    print()
    print(StatusIndicator.success("创意设计完成"))

    # 输入设计提示词
    print()
    prompt_panel = Panel("✨ 图像生成提示词", 60)
    prompt_panel.add_line("请输入详细的设计提示词来生成图像：")
    prompt_panel.add_line(muted("留空将使用默认的传统剪纸风格"))
    print(prompt_panel.render())
    print()

    design_prompt = input(primary("设计提示词: ")).strip()
    if not design_prompt:
        design_prompt = "传统中国红色调，对称蝙蝠图案，吉祥如意"
        print(StatusIndicator.info(f"使用默认提示词: {design_prompt}"))

    # 选择图像生成提供商
    print()
    provider_menu = Menu("🤖 选择AI图像生成服务", 50)
    provider_menu.add_option("1", "OpenAI DALL-E", "高质量图像生成", "🎨")
    provider_menu.add_option("2", "豆包 Doubao", "本土化AI服务", "🇨🇳")
    print(provider_menu.render())
    print()

    provider_choice = input(primary("请选择服务 (默认: 2): ")).strip()
    provider = "openai" if provider_choice == "1" else "doubao"

    provider_name = "OpenAI DALL-E" if provider == "openai" else "豆包 Doubao"
    print(StatusIndicator.info(f"已选择: {provider_name}"))

    # 生成图像
    print()
    generation_panel = Panel("🎨 图像生成中", 60)
    generation_panel.add_line(f"使用 {provider_name} 生成设计图...")
    generation_panel.add_line("请耐心等待，AI正在创作中...")
    print(generation_panel.render())

    from src.utils.image import ImageProcessor
    image_processor = ImageProcessor(conversation_manager.settings)

    spinner = LoadingSpinner("图像生成中", "spinner")
    spinner.start()

    try:
        image_path = await image_processor.generate_image(design_prompt, provider=provider)
    finally:
        spinner.stop()

    if image_path:
        print(StatusIndicator.success(f"设计图已生成: {image_path}"))
    else:
        print(StatusIndicator.error("设计图生成失败"))
        UIComponents.wait_for_input()
        return

    # 用户上传原型
    print()
    prototype_panel = Panel("📎 原型图片处理（可选）", 60)
    prototype_panel.add_line("您可以上传自己的原型图片进行进一步处理：")
    prototype_panel.add_line(muted("留空跳过此步骤"))
    print(prototype_panel.render())
    print()

    user_prototype_path = input(secondary("原型图片路径: ")).strip()

    if user_prototype_path and os.path.exists(user_prototype_path):
        print(StatusIndicator.success(f"已选择原型图片: {user_prototype_path}"))

        # 处理选项
        print()
        process_menu = Menu("🔧 原型处理方式", 50)
        process_menu.add_option("1", "直接合并", "将原型与生成图直接合并", "🔗")
        process_menu.add_option("2", "AI重新生成", "基于原型生成新的设计", "🎨")
        print(process_menu.render())
        print()

        process_choice = input(primary("请选择处理方式 (默认: 1): ")).strip()

        if process_choice == "2":
            # AI重新生成
            print()
            variation_panel = Panel("🎨 基于原型重新生成", 60)
            variation_panel.add_line("请输入新的提示词来指导AI重新创作：")
            print(variation_panel.render())
            print()

            variation_prompt = input(primary("新提示词: ")).strip()
            if not variation_prompt:
                variation_prompt = "基于参考图像，生成对称的剪纸风格的中国传统蝙蝠吉祥纹样，保持原图的风格和元素"
                print(StatusIndicator.info("使用默认提示词"))

            # 基于原型图片生成新图片
            spinner = LoadingSpinner("基于原型生成中", "dots")
            spinner.start()

            try:
                variation_image_path = await image_processor.generate_image_from_image(
                    user_prototype_path, variation_prompt, provider="doubao"
                )
            finally:
                spinner.stop()

            if variation_image_path:
                print(StatusIndicator.success(f"基于原型的新设计已生成: {variation_image_path}"))

                # 合并原始设计和基于原型的新设计
                print()
                print(StatusIndicator.info("正在合并最终设计..."))

                spinner = LoadingSpinner("合并设计中", "blocks")
                spinner.start()

                try:
                    merged_image_path = image_processor.merge_images(image_path, variation_image_path)
                finally:
                    spinner.stop()

                if merged_image_path:
                    print(StatusIndicator.success(f"最终设计已生成: {merged_image_path}"))
                else:
                    print(StatusIndicator.error("最终设计合并失败"))
            else:
                print(StatusIndicator.error("基于原型的新设计生成失败"))
        else:
            # 直接合并两张图片
            print()
            print(StatusIndicator.info("正在合并原型设计..."))

            spinner = LoadingSpinner("合并图片中", "bars")
            spinner.start()

            try:
                merged_image_path = image_processor.merge_images(image_path, user_prototype_path)
            finally:
                spinner.stop()

            if merged_image_path:
                print(StatusIndicator.success(f"最终设计已生成: {merged_image_path}"))
            else:
                print(StatusIndicator.error("最终设计生成失败"))
    elif user_prototype_path:
        print(StatusIndicator.warning("原型图片文件不存在，跳过此步骤"))

    # 完成提示
    print()
    completion_panel = Panel("🎉 设计流程完成", 50)
    completion_panel.add_line(success("剪纸文创设计已完成！"))
    completion_panel.add_line(muted("感谢您使用我们的设计服务"))
    print(completion_panel.render())

    UIComponents.wait_for_input()


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
