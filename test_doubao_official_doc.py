#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
豆包API图像生成测试程序 - 基于官方文档
"""

import os
import requests
import base64
from openai import OpenAI
from dotenv import load_dotenv
import time

# 加载环境变量
load_dotenv()

# 获取API密钥
api_key = os.environ.get("DOUBAO_API_KEY")
if not api_key:
    raise ValueError("请在.env文件中设置DOUBAO_API_KEY环境变量")

# 创建图像保存目录
image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "images")
os.makedirs(image_dir, exist_ok=True)

def test_openai_client():
    """
    使用OpenAI客户端测试豆包API图像生成
    """
    print("使用OpenAI客户端测试豆包API图像生成...")
    
    # 初始化客户端
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=api_key
    )
    
    try:
        # 生成图像
        response = client.images.generate(
            model="doubao-seedream-3-0-t2i-250415",  # 使用官方文档中的模型ID
            prompt="对称的剪纸风格的中国传统蝙蝠吉祥纹样，红色背景，精细的剪纸纹理",
            size="1024x1024",
            response_format="url"
        )
        
        # 获取图像URL
        image_url = response.data[0].url
        print(f"图像生成成功，URL: {image_url}")
        
        # 下载图像
        image_data = requests.get(image_url).content
        
        # 保存图像
        timestamp = int(time.time())
        file_name = f"test_openai_client_{timestamp}.png"
        file_path = os.path.join(image_dir, file_name)
        
        with open(file_path, "wb") as f:
            f.write(image_data)
        
        print(f"图像已保存到: {file_path}")
        return True
        
    except Exception as e:
        print(f"使用OpenAI客户端测试失败: {str(e)}")
        return False

def test_direct_api():
    """
    直接使用requests库测试豆包API图像生成
    """
    print("直接使用requests库测试豆包API图像生成...")
    
    # 构建URL
    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    
    # 构建请求数据
    data = {
        "model": "doubao-seedream-3-0-t2i-250415",  # 使用官方文档中的模型ID
        "prompt": "对称的剪纸风格的中国传统蝙蝠吉祥纹样，红色背景，精细的剪纸纹理",
        "size": "1024x1024",
        "n": 1,
        "response_format": "url"
    }
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        # 发送请求
        response = requests.post(url, json=data, headers=headers)
        
        # 检查响应
        if response.status_code != 200:
            print(f"API请求失败: {response.status_code}, {response.text}")
            return False
        
        # 解析响应
        result = response.json()
        
        # 获取图像URL
        image_url = result["data"][0]["url"]
        print(f"图像生成成功，URL: {image_url}")
        
        # 下载图像
        image_data = requests.get(image_url).content
        
        # 保存图像
        timestamp = int(time.time())
        file_name = f"test_direct_api_{timestamp}.png"
        file_path = os.path.join(image_dir, file_name)
        
        with open(file_path, "wb") as f:
            f.write(image_data)
        
        print(f"图像已保存到: {file_path}")
        return True
        
    except Exception as e:
        print(f"直接使用requests库测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始测试豆包API图像生成...")
    
    # 测试OpenAI客户端
    openai_client_success = test_openai_client()
    
    # 测试直接API调用
    direct_api_success = test_direct_api()
    
    # 输出测试结果
    print("\n测试结果:")
    print(f"OpenAI客户端测试: {'成功' if openai_client_success else '失败'}")
    print(f"直接API调用测试: {'成功' if direct_api_success else '失败'}")
