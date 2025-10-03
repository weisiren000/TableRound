#!/usr/bin/env python3
"""
简单的Google API测试脚本 - 使用requests库
"""

import os
import base64
import requests
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_google_api():
    """测试Google Gemini API"""
    
    print("=== 简单的Google API测试 ===")
    
    # 获取配置
    api_key = os.getenv("GOOGLE_API_KEY")
    model = "gemini-2.5-flash-preview-05-20"
    image_path = "d:\\codee\\tableround\\data\\images\\design_1749387656.png"
    
    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: None")
    print(f"Model: {model}")
    
    if not api_key:
        print("❌ GOOGLE_API_KEY环境变量未设置")
        return False
    
    if not os.path.exists(image_path):
        print(f"❌ 图片文件不存在: {image_path}")
        return False
    
    print(f"✅ 图片文件存在: {image_path}")
    
    # 读取图片并转换为Base64
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        print(f"✅ Base64转换完成，长度: {len(base64_image)}")
    except Exception as e:
        print(f"❌ 图片读取失败: {e}")
        return False
    
    # 构建请求数据
    data = {
        "contents": [
            {
                "parts": [
                    {"text": "请详细描述这张图片的内容，包括颜色、形状、主题等。"},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }
    
    # 构建URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    print("🔄 发送API请求...")
    print(f"URL: {url}")
    
    try:
        # 发送请求
        response = requests.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"},
            params={"key": api_key},
            timeout=30
        )
        
        print(f"✅ HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # 解析响应
            if "candidates" in result and result["candidates"]:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if parts and "text" in parts[0]:
                        text = parts[0]["text"]
                        print("✅ API请求成功!")
                        print("📝 响应内容:")
                        print(text)
                        return True
            
            print("⚠️ 响应格式异常:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return False
        else:
            print(f"❌ API请求失败: HTTP {response.status_code}")
            print("错误详情:")
            print(response.text)
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误")
        return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

if __name__ == "__main__":
    success = test_google_api()
    if success:
        print("\n🎉 测试成功！")
    else:
        print("\n💥 测试失败！")
