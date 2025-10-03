#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试当前配置是否正确
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到系统路径
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT_DIR))

from src.config.settings import Settings


def test_current_config():
    """测试当前配置"""
    
    print("=== 当前配置测试 ===\n")
    
    # 加载设置
    settings = Settings()
    
    print(f"AI提供商: {settings.provider}")
    print(f"AI模型: {settings.model}")
    print(f"支持的提供商: {list(settings.supported_providers.keys())}")
    
    # 检查API密钥
    api_key = settings.get_api_key(settings.provider)
    print(f"API密钥存在: {'是' if api_key else '否'}")
    if api_key:
        print(f"API密钥前缀: {api_key[:10]}...")
    
    # 检查基础URL
    base_url = settings.get_base_url(settings.provider)
    print(f"基础URL: {base_url}")
    
    # 尝试创建模型实例
    try:
        model = settings.get_model_instance()
        print(f"模型实例类型: {type(model).__name__}")
        print(f"模型名称: {model.model_name}")
        
        if hasattr(model, 'vision_model'):
            print(f"视觉模型: {model.vision_model}")
        if hasattr(model, 'chat_model'):
            print(f"对话模型: {model.chat_model}")
        if hasattr(model, 'supports_vision'):
            print(f"支持图像处理: {model.supports_vision()}")
            
    except Exception as e:
        print(f"创建模型实例失败: {str(e)}")
    
    print("\n=== 智能体配置 ===")
    print(f"智能体数量: {settings.agent_counts}")
    print(f"最大轮次: {settings.max_turns}")
    print(f"最大关键词: {settings.max_keywords}")


if __name__ == "__main__":
    test_current_config()
