#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI美化组件测试
"""

import sys
import time
import asyncio
from pathlib import Path

# 添加项目根目录到系统路径
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.ui_enhanced import (
    EnhancedColors, Icons, ASCIIArt, Decorations,
    UIComponents, Panel, ProgressBar, Menu, StatusIndicator, AgentCard,
    Animations, LoadingSpinner, ProgressTracker,
    ThemeManager, theme_manager, primary, secondary, success, warning, error, info, text, muted, accent
)


def test_colors():
    """测试颜色系统"""
    print("=== 颜色系统测试 ===")
    print(EnhancedColors.bright_green("✓ 亮绿色文本"))
    print(EnhancedColors.bright_red("✗ 亮红色文本"))
    print(EnhancedColors.bright_yellow("⚠ 亮黄色文本"))
    print(EnhancedColors.bright_blue("ℹ 亮蓝色文本"))
    print(EnhancedColors.rainbow_text("🌈 彩虹色文本效果"))
    print(EnhancedColors.gradient_text("渐变色文本", (255, 0, 0), (0, 0, 255)))
    print()


def test_icons():
    """测试图标系统"""
    print("=== 图标系统测试 ===")
    print(f"{Icons.SUCCESS} 成功图标")
    print(f"{Icons.ERROR} 错误图标")
    print(f"{Icons.WARNING} 警告图标")
    print(f"{Icons.INFO} 信息图标")
    print(f"{Icons.LOADING} 加载图标")
    print()
    
    print("智能体图标:")
    print(f"{Icons.CRAFTSMAN} 手工艺人")
    print(f"{Icons.CONSUMER} 消费者")
    print(f"{Icons.MANUFACTURER} 制造商")
    print(f"{Icons.DESIGNER} 设计师")
    print(f"{Icons.GOD_VIEW} 上帝视角")
    print()


def test_components():
    """测试UI组件"""
    print("=== UI组件测试 ===")
    
    # 测试面板
    panel = Panel("测试面板", 50)
    panel.add_line("这是面板内容第一行")
    panel.add_line("这是面板内容第二行")
    panel.add_separator()
    panel.add_line("分隔线后的内容")
    print(panel.render())
    print()
    
    # 测试菜单
    menu = Menu("测试菜单", 40)
    menu.add_option("1", "选项一", "第一个选项", "🎯")
    menu.add_option("2", "选项二", "第二个选项", "🎨")
    menu.add_option("3", "选项三", "第三个选项", "🔧")
    print(menu.render())
    print()
    
    # 测试状态指示器
    print(StatusIndicator.success("操作成功"))
    print(StatusIndicator.error("操作失败"))
    print(StatusIndicator.warning("警告信息"))
    print(StatusIndicator.info("提示信息"))
    print()


def test_themes():
    """测试主题系统"""
    print("=== 主题系统测试 ===")
    
    themes = theme_manager.list_themes()
    print(f"可用主题: {', '.join(themes)}")
    print(f"当前主题: {theme_manager.current_theme.name}")
    print()
    
    # 测试主题颜色
    print(primary("主色文本"))
    print(secondary("次色文本"))
    print(success("成功色文本"))
    print(warning("警告色文本"))
    print(error("错误色文本"))
    print(info("信息色文本"))
    print(accent("强调色文本"))
    print(muted("静音色文本"))
    print()


async def test_animations():
    """测试动画效果"""
    print("=== 动画效果测试 ===")
    
    # 测试打字机效果
    print("打字机效果演示:")
    Animations.typewriter_effect("这是打字机效果的演示文本", delay=0.05)
    print()
    
    # 测试进度条
    print("进度条演示:")
    tracker = ProgressTracker(5, "处理中")
    for i in range(6):
        tracker.update(i, f"步骤 {i+1}")
        await asyncio.sleep(0.3)
    tracker.finish("完成")
    print()


def test_ascii_art():
    """测试ASCII艺术"""
    print("=== ASCII艺术测试 ===")
    print(ASCIIArt.SIMPLE_LOGO)
    print()
    
    # 测试进度条样式
    for style in ["classic", "dots", "blocks"]:
        bar = ASCIIArt.create_progress_bar(0.7, 20, style)
        print(f"{style}: [{bar}]")
    print()


async def main():
    """主测试函数"""
    print(EnhancedColors.bright_cyan("🎨 TableRound UI美化组件测试"))
    print(EnhancedColors.silver("=" * 50))
    print()
    
    try:
        test_colors()
        test_icons()
        test_components()
        test_themes()
        test_ascii_art()
        await test_animations()
        
        print(EnhancedColors.bright_green("✅ 所有测试完成！"))
        
    except Exception as e:
        print(EnhancedColors.bright_red(f"❌ 测试失败: {str(e)}"))
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
