# 圆桌会议系统API文档

## 简介

圆桌会议系统提供了一组RESTful API，用于与多智能体交互系统进行交互。这些API支持开始对话、角色转换、处理图片和设计剪纸等功能。

## 基础URL

```
http://127.0.0.1:8000
```

## 认证

目前API不需要认证。

## 响应格式

所有API响应都使用JSON格式，包含以下字段：

- `success`: 布尔值，表示请求是否成功
- `message`: 字符串，表示请求的结果消息
- `data`: 对象，包含响应数据（如果有）

成功响应示例：

```json
{
  "success": true,
  "message": "成功开始主题为 '传统工艺的现代应用' 的对话",
  "data": {
    "topic": "传统工艺的现代应用"
  }
}
```

错误响应示例：

```json
{
  "success": false,
  "message": "开始对话失败: 对话管理器未初始化"
}
```

## API端点

### 获取系统状态

获取系统当前状态。

**请求**

```
GET /status
```

**响应**

```json
{
  "success": true,
  "message": "系统正常运行",
  "data": {
    "stage": "waiting",
    "topic": "传统工艺的现代应用",
    "agent_count": 6
  }
}
```

### 开始对话

开始一个新的对话。

**请求**

```
POST /conversation/start
```

**请求体**

```json
{
  "topic": "传统工艺的现代应用"
}
```

**响应**

```json
{
  "success": true,
  "message": "成功开始主题为 '传统工艺的现代应用' 的对话",
  "data": {
    "topic": "传统工艺的现代应用"
  }
}
```

### 开始角色转换

开始角色转换阶段。

**请求**

```
POST /conversation/role-switch
```

**请求体**

```json
{
  "keywords": ["传统", "创新", "文化", "市场", "技艺"]
}
```

**响应**

```json
{
  "success": true,
  "message": "成功开始角色转换阶段",
  "data": {
    "keywords": ["传统", "创新", "文化", "市场", "技艺"]
  }
}
```

### 处理图片

上传并处理图片。

**请求**

```
POST /image/process
```

**请求体**

使用 `multipart/form-data` 格式，包含一个名为 `file` 的文件字段。

**响应**

```json
{
  "success": true,
  "message": "成功处理图片",
  "data": {
    "image_path": "/app/data/images/example.jpg",
    "keywords": ["传统", "文化", "艺术", "手工", "精致"]
  }
}
```

### 设计剪纸文创产品

根据关键词设计剪纸文创产品。

**请求**

```
POST /design/paper-cutting
```

**请求体**

```json
{
  "keywords": ["蝴蝶", "吉祥", "对称", "传统", "红色"]
}
```

**响应**

```json
{
  "success": true,
  "message": "成功设计剪纸文创产品",
  "data": {
    "keywords": ["蝴蝶", "吉祥", "对称", "传统", "红色"],
    "designs": {
      "craftsman_1": "设计方案内容...",
      "consumer_1": "设计方案内容...",
      "manufacturer_1": "设计方案内容...",
      "designer_1": "设计方案内容..."
    }
  }
}
```

## 错误代码

| 状态码 | 描述 |
|--------|------|
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 使用示例

### 使用curl开始对话

```bash
curl -X POST \
  http://127.0.0.1:8000/conversation/start \
  -H 'Content-Type: application/json' \
  -d '{"topic": "传统工艺的现代应用"}'
```

### 使用Python开始对话

```python
import requests
import json

url = "http://127.0.0.1:8000/conversation/start"
payload = {"topic": "传统工艺的现代应用"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
```

### 使用curl上传图片

```bash
curl -X POST \
  http://127.0.0.1:8000/image/process \
  -F 'file=@/path/to/image.jpg'
```

### 使用Python上传图片

```python
import requests

url = "http://127.0.0.1:8000/image/process"
files = {"file": open("/path/to/image.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

## 限制

- 图片上传大小限制为10MB
- API请求频率限制为每分钟60次
- 对话内容长度限制为10000个字符

## 版本历史

| 版本 | 日期 | 描述 |
|------|------|------|
| 1.0.0 | 2023-06-01 | 初始版本 |
