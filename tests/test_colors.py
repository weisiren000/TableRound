#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试终端颜色支持
"""

import os
import sys
import time
from pathlib import Path

# 添加项目根目录到系统路径
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT_DIR))

# 定义简单的颜色代码
GREEN = "\033[32m"
RESET = "\033[0m"


def test_colors():
    """测试终端颜色"""
    print("测试终端颜色支持")
    print("-" * 30)

    # 测试绿色文本
    print(f"绿色文本: {GREEN}绿色{RESET}")

    # 测试关键词显示
    keywords = ["传统文化", "剪纸艺术", "蝙蝠图案", "吉祥寓意", "对称设计"]
    colored_keywords = [f"{GREEN}{kw}{RESET}" for kw in keywords]
    keywords_str = ", ".join(colored_keywords)
    print(f"关键词: {keywords_str}")


def test_keywords_display():
    """测试关键词显示"""
    print("\n测试KJ法分类结果")
    print("-" * 30)

    # 模拟KJ法分类结果
    print(f"【核心概念】\n{GREEN}中国传统剪纸艺术的现代文创应用{RESET}\n")

    print("【一级关键词】")
    print(f"1. {GREEN}传统文化元素{RESET}")
    print(f"2. {GREEN}设计元素{RESET}")
    print("")

    print("【二级关键词】")
    print(f"1.1 {GREEN}吉祥符号{RESET}：{GREEN}蝙蝠{RESET}, {GREEN}福气{RESET}")
    print(f"2.1 {GREEN}视觉元素{RESET}：{GREEN}红色{RESET}, {GREEN}对称设计{RESET}")


if __name__ == "__main__":
    test_colors()
    test_keywords_display()
