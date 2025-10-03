#!/usr/bin/env python3
"""
测试修复后的Google模型图像处理功能
"""

import asyncio
import os
import sys
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.google import GoogleModel
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_google_fixed():
    """测试修复后的Google模型图像处理功能"""
    
    print("=== 测试修复后的Google模型 ===")
    
    # 获取配置
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = "gemini-2.5-flash-preview-05-20"  # 使用指定的模型
    
    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: None")
    print(f"Model: {model_name}")
    
    if not api_key:
        print("❌ Google API密钥未设置")
        return False
    
    # 创建模型实例
    try:
        model = GoogleModel(
            model_name=model_name,
            api_key=api_key
        )
        print(f"✅ 模型实例创建成功")
        print(f"📷 支持图像处理: {model.supports_vision()}")
        
    except Exception as e:
        print(f"❌ 模型实例创建失败: {e}")
        return False
    
    # 测试图像路径
    image_path = "d:\\codee\\tableround\\data\\images\\design_1749387656.png"
    
    if not os.path.exists(image_path):
        print(f"❌ 图像文件不存在: {image_path}")
        return False
    
    print(f"📁 图像文件存在: {image_path}")
    
    # 测试图像处理
    try:
        prompt = "请详细描述这张图片的内容，包括颜色、形状、主题等。"
        system_prompt = "你是一个专业的图像分析师，请仔细观察图片并给出详细的描述。"
        
        print("🔄 开始图像处理...")
        result = await model.generate_with_image(prompt, system_prompt, image_path)
        
        print("✅ 图像处理完成")
        print(f"📝 结果: {result}")
        
        # 检查结果是否包含错误信息
        if "生成失败" in result or "该模型不支持图像处理" in result:
            print("❌ 图像处理返回错误")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 图像处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_google_fixed())
    if success:
        print("\n🎉 测试成功！")
    else:
        print("\n💥 测试失败！")
