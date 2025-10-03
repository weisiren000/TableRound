#!/usr/bin/env python3
"""
测试Google模型的图像处理功能 - 使用新的Google GenAI SDK
"""

import asyncio
import os
import sys
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_google_vision_new_sdk():
    """使用新的Google GenAI SDK测试图像处理功能"""

    try:
        from google import genai
        from google.genai import types
        print("✅ 成功导入新的Google GenAI SDK")
    except ImportError as e:
        print(f"❌ 无法导入Google GenAI SDK: {e}")
        print("请安装: pip install google-genai")
        return False

    # 获取配置
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = "gemini-2.0-flash-001"  # 使用支持图像的模型

    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: None")
    print(f"Model: {model_name}")

    if not api_key:
        print("❌ Google API密钥未设置")
        return False

    # 创建客户端
    try:
        client = genai.Client(api_key=api_key)
        print("✅ 客户端创建成功")
    except Exception as e:
        print(f"❌ 客户端创建失败: {e}")
        return False

    # 测试图像路径
    image_path = "d:\\codee\\tableround\\data\\images\\design_1749387656.png"

    if not os.path.exists(image_path):
        print(f"❌ 图像文件不存在: {image_path}")
        return False

    print(f"📁 图像文件存在: {image_path}")

    # 测试图像处理
    try:
        print("🔄 开始图像处理...")

        # 读取图像
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # 构建内容
        contents = [
            "请详细描述这张图片的内容，包括颜色、形状、主题等。",
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        ]

        # 调用API
        response = client.models.generate_content(
            model=model_name,
            contents=contents
        )

        print("✅ 图像处理完成")
        print(f"📝 结果: {response.text}")

        return True

    except Exception as e:
        print(f"❌ 图像处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_google_vision_old_method():
    """测试原有的Google模型实现"""

    from src.models.google import GoogleModel

    # 获取配置
    api_key = os.getenv("GOOGLE_API_KEY")
    base_url = os.getenv("GOOGLE_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    model_name = os.getenv("AI_MODEL", "gemini-2.5-flash-preview-05-20")

    print(f"\n=== 测试原有实现 ===")
    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: None")
    print(f"Base URL: {base_url}")
    print(f"Model: {model_name}")

    if not api_key:
        print("❌ Google API密钥未设置")
        return False

    # 创建模型实例
    try:
        model = GoogleModel(
            model_name=model_name,
            api_key=api_key,
            base_url=base_url
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

        return True

    except Exception as e:
        print(f"❌ 图像处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== 测试新的Google GenAI SDK ===")
    success1 = asyncio.run(test_google_vision_new_sdk())

    print("\n=== 测试原有实现 ===")
    success2 = asyncio.run(test_google_vision_old_method())

    if success1 or success2:
        print("\n🎉 至少一种方法测试成功！")
    else:
        print("\n💥 所有测试都失败了！")
