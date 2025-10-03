# TableRound 测试套件

本目录包含TableRound项目的所有测试脚本，按功能分类组织。

## 目录结构

```
tests/
├── README.md                    # 本文件
├── __init__.py                  # 测试模块初始化
├── api/                         # API和模型测试
│   ├── __init__.py
│   ├── test_openrouter_basic.py      # OpenRouter API基础测试
│   ├── test_doubao_image_generation.py # 豆包图像生成API测试
│   └── test_doubao_watermark.py       # 豆包watermark参数测试
├── memory/                      # 记忆系统测试
│   ├── __init__.py
│   ├── test_redis_memory.py          # Redis记忆模块测试
│   ├── test_redis_simple.py          # Redis简单功能测试
│   ├── test_global_memory.py         # 全局记忆功能测试
│   ├── test_enhanced_memory.py       # 增强记忆功能测试
│   └── test_memory_diagnosis.py      # 记忆系统诊断测试
├── integration/                 # 系统集成测试
│   ├── __init__.py
│   ├── test_comprehensive.py         # Redis记忆模块综合测试
│   ├── test_migration.py             # Agent系统迁移测试
│   ├── test_quick_migration.py       # 快速迁移验证测试
│   ├── test_simple_migration.py      # 简单迁移测试
│   └── test_simple_global.py         # 简单全局功能测试
├── features/                    # 功能特性测试
│   ├── __init__.py
│   ├── test_role_switch_improvements.py # 角色转换改进测试
│   └── test_performance.py           # 性能测试
├── demos/                       # 演示脚本
│   ├── __init__.py
│   └── demo_global_memory.py         # 全局记忆演示
├── test_agents.py              # 智能体测试（原有）
├── test_colors.py              # 颜色工具测试（原有）
├── test_conversation.py        # 对话管理测试（原有）
├── test_memory.py              # 记忆模块测试（原有）
├── test_models.py              # 模型接口测试（原有）
└── test_role_playing.py        # 角色扮演测试（原有）
```

## 测试分类说明

### 1. API测试 (api/)
测试各种AI模型API的接口功能：
- **OpenRouter API**: 基础连接和调用测试
- **豆包图像生成**: 图像生成功能测试
- **Watermark参数**: 豆包API的水印控制功能测试

### 2. 记忆系统测试 (memory/)
测试项目的记忆存储和检索功能：
- **Redis记忆**: Redis作为存储后端的记忆功能
- **全局记忆**: 跨智能体的全局记忆共享
- **增强记忆**: 记忆功能的增强和优化
- **记忆诊断**: 记忆系统的健康检查和诊断

### 3. 系统集成测试 (integration/)
测试各个模块之间的集成和协作：
- **综合测试**: 完整的系统功能测试
- **迁移测试**: 系统迁移和升级测试
- **全局功能**: 系统级别的功能验证

### 4. 功能特性测试 (features/)
测试特定功能特性的实现：
- **角色转换**: 智能体角色切换功能
- **性能测试**: 系统性能基准测试

### 5. 演示脚本 (demos/)
用于演示和展示功能的脚本：
- **全局记忆演示**: 展示全局记忆功能的使用

## 运行测试

### 运行单个测试
```bash
# 从项目根目录运行
python tests/api/test_doubao_watermark.py
python tests/memory/test_redis_memory.py
python tests/integration/test_comprehensive.py
```

### 运行分类测试
```bash
# 运行所有API测试
python -m pytest tests/api/

# 运行所有记忆系统测试
python -m pytest tests/memory/

# 运行所有集成测试
python -m pytest tests/integration/
```

### 运行所有测试
```bash
# 运行整个测试套件
python -m pytest tests/
```

## 测试环境要求

### 基础要求
- Python 3.8+
- 项目依赖包（见requirements.txt）

### API测试要求
- OpenRouter API密钥
- 豆包API密钥
- 网络连接

### 记忆系统测试要求
- Redis服务器（可选，会自动降级到文件存储）
- 足够的磁盘空间

### 环境变量
确保设置了以下环境变量：
```bash
OPENROUTER_API_KEY=your_openrouter_key
DOUBAO_API_KEY=your_doubao_key
DOUBAO_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
```

## 测试数据

测试过程中会产生以下数据：
- **图像文件**: 保存在`images/`目录
- **记忆数据**: 保存在`data/memories/`目录
- **日志文件**: 保存在`logs/`目录

## 故障排除

### 常见问题
1. **导入错误**: 确保从项目根目录运行测试
2. **API错误**: 检查API密钥和网络连接
3. **Redis连接失败**: 检查Redis服务状态，或使用文件存储模式

### 调试模式
在测试脚本中设置详细日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 贡献指南

### 添加新测试
1. 选择合适的分类目录
2. 创建测试文件，命名格式：`test_功能名称.py`
3. 确保导入路径正确
4. 添加适当的文档说明

### 测试规范
- 使用描述性的测试函数名
- 添加详细的文档字符串
- 包含错误处理和清理代码
- 提供清晰的输出信息

## 更新历史

- **2025-06-08**: 重新组织测试目录结构，按功能分类
- **2025-06-08**: 修复所有测试文件的导入路径
- **2025-06-08**: 添加watermark参数测试
