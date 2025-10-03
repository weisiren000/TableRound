#!/usr/bin/env python3
"""
测试单个智能体的图像处理功能
"""

import asyncio
import os
import sys
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.craftsman import Craftsman
from src.config.settings import Settings
from src.models.google import GoogleModel
from src.core.memory import Memory
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_single_agent_vision():
    """测试单个智能体的图像处理功能"""
    
    print("=== 测试单个智能体图像处理功能 ===")
    
    # 创建设置
    settings = Settings()

    # 创建模型
    model = GoogleModel(
        model_name=settings.model,
        api_key=os.getenv("GOOGLE_API_KEY"),
        base_url=os.getenv("GOOGLE_BASE_URL")
    )

    # 创建记忆
    memory = MemoryAdapter(
        agent_id="test_craftsman_1",
        storage_type="memory",
        max_tokens=4000
    )

    # 创建手工艺人智能体
    agent = Craftsman(
        agent_id="test_craftsman_1",
        name="测试手工艺人",
        model=model,
        memory=memory
    )
    
    print(f"✅ 创建智能体: {agent.name}")
    print(f"📷 支持图像处理: {agent.model.supports_vision()}")
    
    # 测试图像路径
    image_path = "d:\\codee\\tableround\\data\\images\\design_1749387656.png"
    
    if not os.path.exists(image_path):
        print(f"❌ 图像文件不存在: {image_path}")
        return False
    
    print(f"📁 图像文件存在: {image_path}")
    
    # 测试图像处理
    try:
        print("🔄 开始图像处理...")
        
        # 调用智能体的图像分析方法
        story, keywords = await agent.tell_story_from_image(image_path)

        print("✅ 图像处理完成")
        print(f"📝 故事: {story}")
        print(f"🏷️ 关键词: {keywords}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_single_agent_vision())
    if success:
        print("\n🎉 测试成功！")
    else:
        print("\n💥 测试失败！")
