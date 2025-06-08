# TableRound 项目架构

## 项目概述
TableRound 是一个基于多智能体对话的圆桌会议系统，专注于剪纸文创产品设计。

## 目录结构

```
tableround/
├── src/                           # 源代码目录
│   ├── __init__.py
│   ├── main.py                    # 主程序入口
│   ├── agents/                    # 智能体模块
│   │   ├── __init__.py
│   │   ├── craftsman.py          # 手工艺人智能体
│   │   ├── consumer.py           # 消费者智能体
│   │   ├── manufacturer.py       # 制造商智能体
│   │   └── designer.py           # 设计师智能体
│   ├── core/                      # 核心模块
│   │   ├── __init__.py
│   │   ├── agent.py              # 智能体基类
│   │   ├── conversation.py       # 对话管理
│   │   ├── god_view.py           # 上帝视角
│   │   ├── kj_method.py          # KJ法分类
│   │   ├── memory.py             # 文件记忆模块
│   │   ├── redis_memory.py       # Redis记忆模块
│   │   └── memory_adapter.py     # 记忆适配器
│   ├── models/                    # AI模型接口
│   │   ├── __init__.py
│   │   ├── base.py               # 模型基类
│   │   ├── openai.py             # OpenAI模型
│   │   ├── anthropic.py          # Anthropic模型
│   │   ├── google.py             # Google模型
│   │   ├── deepseek.py           # DeepSeek模型
│   │   ├── doubao.py             # 豆包模型
│   │   ├── openrouter.py         # OpenRouter模型
│   │   └── mock.py               # 模拟模型
│   ├── config/                    # 配置模块
│   │   ├── __init__.py
│   │   ├── settings.py           # 全局设置
│   │   ├── prompts.py            # 提示词模板(向后兼容)
│   │   ├── models.py             # 模型配置
│   │   ├── redis_config.py       # Redis配置
│   │   └── prompts/              # 模块化提示词系统
│   │       ├── __init__.py
│   │       ├── README.md         # 提示词系统文档
│   │       ├── base_prompts.py   # 基础通用提示词
│   │       ├── template_manager.py # 提示词管理器
│   │       ├── test_prompts.py   # 测试文件
│   │       ├── agent_prompts/    # 智能体专用提示词
│   │       │   ├── __init__.py
│   │       │   ├── craftsman_prompts.py   # 手工艺人提示词
│   │       │   ├── consumer_prompts.py    # 消费者提示词
│   │       │   ├── manufacturer_prompts.py # 制造商提示词
│   │       │   └── designer_prompts.py    # 设计师提示词
│   │       └── function_prompts/ # 功能相关提示词
│   │           ├── __init__.py
│   │           ├── keyword_extraction_prompts.py # 关键词提取
│   │           ├── role_switch_prompts.py         # 角色转换
│   │           ├── scenario_prompts.py            # 场景设置
│   │           └── image_story_prompts.py         # 图片故事
│   ├── utils/                     # 工具模块
│   │   ├── __init__.py
│   │   ├── logger.py             # 日志工具
│   │   ├── colors.py             # 颜色工具
│   │   ├── stream.py             # 流式输出
│   │   ├── voting.py             # 投票机制
│   │   └── image.py              # 图像处理
│   └── api/                       # API接口（预留）
│       └── __init__.py
├── ui/                            # 用户界面
│   └── cli/                       # 命令行界面
│       └── terminal.py           # 终端界面
├── data/                          # 数据目录
│   ├── memories/                  # 记忆存储
│   ├── images/                    # 图片存储
│   └── keywords/                  # 关键词存储
├── logs/                          # 日志目录
├── docs/                          # 文档目录
├── tests/                         # 测试目录
├── requirements.txt               # Python依赖
├── .env.example                   # 环境变量示例
├── .gitignore                     # Git忽略文件
└── README.md                      # 项目说明
```

## 核心组件

### 1. 智能体系统 (src/agents/)
- **Craftsman**: 手工艺人智能体，专注传统工艺和制作技术
- **Consumer**: 消费者智能体，关注用户需求和市场反馈
- **Manufacturer**: 制造商智能体，考虑生产成本和工艺流程
- **Designer**: 设计师智能体，负责创意设计和美学表达

### 2. 核心引擎 (src/core/)
- **Agent**: 智能体基类，提供通用功能
- **ConversationManager**: 对话管理器，协调智能体交互
- **GodView**: 上帝视角，监控和引导对话流程
- **Memory**: 记忆模块，存储和检索对话历史
- **KJMethod**: KJ法分类，整理和归纳讨论内容

### 3. AI模型层 (src/models/)
- 支持多种AI模型提供商
- 统一的模型接口
- 流式输出支持
- 图像处理能力

### 4. 配置系统 (src/config/)
- 全局设置管理
- 提示词模板
- 模型配置

### 5. 工具库 (src/utils/)
- 日志系统
- 颜色输出
- 流式处理
- 投票机制
- 图像处理

## 技术特性

### 多智能体协作
- 六个智能体按特定顺序对话
- 角色转换机制，保持记忆的同时切换视角
- 智能体自我介绍（300字限制）

### 对话流程
1. 智能体自我介绍
2. 主题讨论（一轮对话）
3. 关键词提取和投票
4. 角色转换
5. 剪纸研讨会场景讨论
6. 用户输入设计提示词
7. 图像生成

### 图像生成
- 支持豆包API图像生成
- 使用模型：doubao-seedream-3-0-t2i-250415
- 自动优化提示词
- 图像下载和存储

### 记忆系统
- 对话历史记录
- 关键词记忆
- 角色转换记忆
- 设计卡牌记忆

### 流式输出
- 实时显示智能体对话
- 彩色关键词高亮
- 进度提示

## 配置要求

### 环境变量
```
# AI模型配置
AI_PROVIDER=openrouter
AI_MODEL=meta-llama/llama-4-maverick:free

# API密钥
OPENROUTER_API_KEY=your_key_here
DOUBAO_API_KEY=your_key_here
DOUBAO_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# 智能体数量
CRAFTSMAN_COUNT=1
CONSUMER_COUNT=3
MANUFACTURER_COUNT=1
DESIGNER_COUNT=1

# 对话设置
MAX_TURNS=1
MAX_KEYWORDS=10
```

### 依赖包
- aiohttp: 异步HTTP客户端
- openai: OpenAI API客户端
- anthropic: Anthropic API客户端
- google-generativeai: Google AI客户端
- requests: HTTP请求库
- python-dotenv: 环境变量加载
- Pillow: 图像处理

## 使用流程

1. 配置环境变量
2. 安装依赖包
3. 运行主程序：`python src/main.py`
4. 选择操作：
   - 开始新对话
   - 处理图片
   - 设计剪纸文创产品
5. 按提示输入主题和参数
6. 查看生成的图像和设计结果

## 扩展性

### 新增智能体
1. 在 `src/agents/` 创建新的智能体类
2. 继承 `Agent` 基类
3. 实现特定的方法和属性
4. 在配置中添加智能体类型

### 新增AI模型
1. 在 `src/models/` 创建新的模型类
2. 继承 `BaseModel` 基类
3. 实现必要的接口方法
4. 在设置中添加模型配置

### 新增功能
1. 在相应模块中添加新功能
2. 更新配置和提示词
3. 添加相应的测试用例

## 项目特点

### 架构优势
- **模块化设计**: 清晰的分层架构，便于维护和扩展
- **插件化模型**: 支持多种AI模型提供商，易于切换
- **异步处理**: 全异步架构，提高性能和响应速度
- **配置驱动**: 通过环境变量和配置文件灵活控制行为

### 核心功能
- **多智能体对话**: 模拟真实的圆桌会议场景
- **角色转换**: 智能体可以切换视角但保持记忆
- **关键词提取**: 自动提取和投票选择关键词
- **图像生成**: 基于讨论结果生成设计图像
- **记忆系统**: 持久化存储对话历史和关键信息

### 技术亮点
- **流式输出**: 实时显示对话过程，提升用户体验
- **彩色终端**: 使用颜色区分不同类型的信息
- **错误处理**: 完善的异常处理和日志记录
- **扩展性**: 易于添加新的智能体类型和AI模型

## 项目历程记录

### 开发记录汇总 (2025年6月8日更新)
项目开发历程已完整汇总到 `_experiments` 目录：

#### 汇总文件
- **SUM2.md**: 完整开发历程总结 (2025年5月21日-6月8日)
- **EXP2.md**: 全流程开发经验汇总
- **MEM2.md**: 项目开发记忆总结

#### 原始记录来源
- `sum/` 目录: sum1.md-sum9.md (后端开发历程)
- `_SUM/` 目录: 前端开发和API配置系统
- `_EXP/` 目录: 代码分析和Bug修复经验

#### 时间线概览
1. **第一阶段** (5月21日-6月3日): 后端多智能体系统开发
2. **第二阶段** (6月3日): 前端开发与API配置系统
3. **第三阶段** (6月3日): 代码分析与Bug修复
4. **第四阶段** (6月8日): 项目结构优化，移除前端

### 核心成就
- ✅ 完整的多智能体协作系统
- ✅ 6种AI模型提供商集成
- ✅ 角色转换与记忆保持机制
- ✅ 关键词提取与KJ法分类
- ✅ 图像生成功能 (文生图/图生图)
- ✅ 流式输出与可视化
- ✅ 完善的错误处理和日志系统
- ✅ 模块化架构设计
- ✅ 模块化提示词管理系统 v2.0

### 最新更新 (2024年12月19日)
**提示词重复清理完成**：
- 🧹 清理了agents文件中的硬编码提示词重复问题
- 🔄 统一使用模块化提示词系统
- 📦 消除了4个智能体类中的重复提示词
- 🔗 保持100%向后兼容性和功能完整性
- 📚 完善了提示词模块的功能覆盖

**清理内容**：
- **Craftsman**: 设计评估、材料建议提示词
- **Consumer**: 产品评估、改进建议提示词
- **Designer**: AI图像生成、设计分析提示词
- **Manufacturer**: 可行性评估、成本估算提示词

**新增提示词**：
- `ConsumerPrompts.PRODUCT_IMPROVEMENT_PROMPT`: 产品改进建议
- `DesignerPrompts.AI_IMAGE_PROMPT_GENERATION`: AI图像生成提示词创作
- `DesignerPrompts.DESIGN_IMAGE_ANALYSIS_PROMPT`: 设计图像分析
- `ManufacturerPrompts.COST_ESTIMATION_PROMPT`: 成本估算

**代码优化**：
- 清理未使用的导入模块
- 统一代码风格和结构
- 提高可维护性和一致性

**验证结果**：
- ✅ 所有提示词模块导入成功
- ✅ 语法检查通过
- ✅ 功能测试正常
- ✅ 重复问题完全解决
