#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI美化特效演示程序
展示所有可用的美化特效
"""

import sys
import time
import asyncio
from pathlib import Path

# 添加项目根目录到系统路径
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.ui_enhanced import (
    EnhancedColors, Icons, ASCIIArt, Decorations,
    UIComponents, Panel, ProgressBar, Menu, StatusIndicator, AgentCard,
    Animations, LoadingSpinner, ProgressTracker,
    ThemeManager, theme_manager, primary, secondary, success, warning, error, info, text, muted, accent
)


def demo_loading_frames():
    """演示加载动画帧"""
    print(primary("=== 加载动画帧演示 ==="))
    print()
    
    print("旋转加载动画:")
    for i in range(20):
        frame = ASCIIArt.get_loading_frame(i)
        colored_frame = EnhancedColors.bright_cyan(frame)
        print(f"\r{colored_frame} 加载中...", end="", flush=True)
        time.sleep(0.1)
    print("\r" + success("✓ 加载完成!") + " " * 10)
    print()


def demo_progress_styles():
    """演示进度条样式"""
    print(primary("=== 进度条样式演示 ==="))
    print()
    
    styles = ["classic", "dots", "blocks"]
    
    for style in styles:
        print(f"{style.capitalize()} 样式:")
        for progress in [0.0, 0.25, 0.5, 0.75, 1.0]:
            bar = ASCIIArt.create_progress_bar(progress, 30, style)
            if progress < 0.3:
                colored_bar = EnhancedColors.bright_red(bar)
            elif progress < 0.7:
                colored_bar = EnhancedColors.bright_yellow(bar)
            else:
                colored_bar = EnhancedColors.bright_green(bar)
            
            print(f"  [{colored_bar}] {progress*100:5.1f}%")
        print()


def demo_ascii_art():
    """演示ASCII艺术"""
    print(primary("=== ASCII艺术演示 ==="))
    print()
    
    # 显示完整Logo
    print("完整Logo:")
    logo = EnhancedColors.gradient_text(ASCIIArt.TABLEROUND_LOGO, (0, 150, 255), (255, 0, 150))
    print(logo)
    print()
    
    # 显示简化Logo
    print("简化Logo:")
    simple_logo = EnhancedColors.rainbow_text(ASCIIArt.SIMPLE_LOGO)
    print(simple_logo)
    print()


def demo_decorations():
    """演示装饰性元素"""
    print(primary("=== 装饰性元素演示 ==="))
    print()
    
    # 分隔线
    print("分隔线样式:")
    print(EnhancedColors.bright_blue(Decorations.create_separator(50, "─")))
    print(EnhancedColors.bright_green(Decorations.create_separator(50, "═")))
    print(EnhancedColors.bright_magenta(Decorations.create_separator(50, "▓")))
    print(EnhancedColors.bright_yellow(Decorations.create_separator(50, "●")))
    print()
    
    # 标题框
    print("标题框:")
    title_box = Decorations.create_title_box("重要通知", 40)
    print(EnhancedColors.bright_cyan(title_box))
    print()
    
    # 面板
    print("面板:")
    panel_content = "这是面板内容\n支持多行文本\n可以显示各种信息"
    panel = Decorations.create_panel(panel_content, "信息面板", 45)
    print(EnhancedColors.bright_white(panel))
    print()


def demo_icons():
    """演示图标系统"""
    print(primary("=== 图标系统演示 ==="))
    print()
    
    # 状态图标
    print("状态图标:")
    print(f"  {success(Icons.SUCCESS)} 成功状态")
    print(f"  {error(Icons.ERROR)} 错误状态")
    print(f"  {warning(Icons.WARNING)} 警告状态")
    print(f"  {info(Icons.INFO)} 信息状态")
    print(f"  {EnhancedColors.bright_cyan(Icons.LOADING)} 加载状态")
    print(f"  {EnhancedColors.bright_yellow(Icons.QUESTION)} 问题状态")
    print()
    
    # 智能体图标
    print("智能体图标:")
    print(f"  {Icons.CRAFTSMAN} 手工艺人")
    print(f"  {Icons.CONSUMER} 消费者")
    print(f"  {Icons.MANUFACTURER} 制造商")
    print(f"  {Icons.DESIGNER} 设计师")
    print(f"  {Icons.GOD_VIEW} 上帝视角")
    print()
    
    # 装饰图标
    print("装饰图标:")
    print(f"  {EnhancedColors.bright_red(Icons.HEART)} 爱心")
    print(f"  {EnhancedColors.bright_yellow(Icons.STAR)} 星星")
    print(f"  {EnhancedColors.bright_blue(Icons.DIAMOND)} 钻石")
    print(f"  {EnhancedColors.bright_green(Icons.CIRCLE)} 圆形")
    print(f"  {EnhancedColors.bright_magenta(Icons.SQUARE)} 方形")
    print(f"  {EnhancedColors.bright_cyan(Icons.TRIANGLE)} 三角")
    print()


def demo_animations():
    """演示动画效果"""
    print(primary("=== 动画效果演示 ==="))
    print()
    
    # 打字机效果
    print("打字机效果:")
    Animations.typewriter_effect(
        "这是一个打字机效果的演示，文字会逐个字符显示出来。", 
        delay=0.05
    )
    print()
    
    # 淡入效果
    print("淡入效果:")
    Animations.fade_in_text("这段文字会逐渐淡入显示", steps=8, delay=0.1)
    print()
    
    # 波浪效果
    print("波浪效果:")
    Animations.wave_text("🌊 波浪文字效果 🌊", waves=2, delay=0.1)
    print()
    
    # 弹跳效果
    print("弹跳效果:")
    Animations.bounce_text("⚡ 弹跳文字 ⚡", bounces=2, delay=0.2)
    print()


def demo_themes():
    """演示主题系统"""
    print(primary("=== 主题系统演示 ==="))
    print()
    
    themes = theme_manager.list_themes()
    current_theme = theme_manager.current_theme.name
    
    print(f"当前主题: {accent(current_theme)}")
    print(f"可用主题: {', '.join(themes)}")
    print()
    
    # 展示当前主题的颜色
    print("当前主题颜色:")
    print(f"  主色: {primary('主色文本')}")
    print(f"  次色: {secondary('次色文本')}")
    print(f"  成功: {success('成功文本')}")
    print(f"  警告: {warning('警告文本')}")
    print(f"  错误: {error('错误文本')}")
    print(f"  信息: {info('信息文本')}")
    print(f"  强调: {accent('强调文本')}")
    print(f"  静音: {muted('静音文本')}")
    print()


async def demo_loading_spinner():
    """演示加载旋转器"""
    print(primary("=== 加载旋转器演示 ==="))
    print()
    
    styles = ["spinner", "dots", "bars", "blocks"]
    
    for style in styles:
        print(f"{style.capitalize()} 样式:")
        spinner = LoadingSpinner(f"加载中 ({style})", style)
        spinner.start()
        await asyncio.sleep(2)
        spinner.stop()
        print(success("✓ 完成"))
        print()


async def main():
    """主演示函数"""
    print(EnhancedColors.rainbow_text("🎨 TableRound UI美化特效完整演示"))
    print(EnhancedColors.bright_cyan("=" * 60))
    print()
    
    # 依次演示各种特效
    demo_ascii_art()
    demo_icons()
    demo_decorations()
    demo_progress_styles()
    demo_loading_frames()
    demo_themes()
    demo_animations()
    await demo_loading_spinner()
    
    print(EnhancedColors.bright_green("🎉 所有美化特效演示完成！"))
    print()
    print(muted("这些特效都可以在TableRound项目中使用，"))
    print(muted("让终端界面更加美观和用户友好。"))


if __name__ == "__main__":
    asyncio.run(main())
