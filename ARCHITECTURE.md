# TableRound 系统架构文档

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## 1. 系统概述

TableRound（圆桌会议）是一个基于多智能体协作的讨论系统，采用Redis作为统一存储后端，支持不同角色智能体之间的交互讨论、记忆管理、关键词提取、角色转换和图像处理等功能。

### 1.1 项目信息

- **项目名称**: TableRound (圆桌会议)
- **代码仓库**: https://github.com/weisiren000/TableRound.git
- **作者**: weisiren
- **更新日期**: 2025年10月3日

## 2. 系统架构

### 2.1 核心组件

```
                     ┌──────────────────┐
                     │   命令行界面     │
                     │  (CLI Terminal)  │
                     └────────┬─────────┘
                              │
                              ▼
┌───────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  智能体模块   │     │                  │     │                  │
│   (Agents)    │◄────┤  对话管理器     ├────►│   上帝视角       │
└───────┬───────┘     │ (Conversation)  │     │  (God View)      │
        │             └────────┬─────────┘     └──────────────────┘
        │                      │
        │                      │
        ▼                      ▼
┌───────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  记忆适配器   │     │                  │     │                  │
│   (Memory)    │◄────┤  全局记忆       ├────►│  Redis存储       │
└───────────────┘     │ (GlobalMemory)  │     │  (RedisMemory)   │
                      └──────────────────┘     └──────────────────┘
```

1. **主入口模块**
   - `run.py`: 项目启动脚本
   - `src/main.py`: 主程序入口，负责初始化系统

2. **核心模块**
   - `src/core/agent.py`: 智能体基类
   - `src/core/conversation.py`: 对话管理器
   - `src/core/god_view.py`: 上帝视角
   - `src/core/global_memory.py`: 全局记忆管理
   - `src/core/memory_adapter.py`: 记忆适配器
   - `src/core/redis_memory.py`: Redis记忆实现
   - `src/core/kj_method.py`: KJ法关键词分类
   - `src/core/meeting_cleaner.py`: 会议清理工具

3. **模型接口**
   - `src/models/base.py`: 模型基类
   - `src/models/openai.py`: OpenAI模型接口
   - `src/models/openrouter.py`: OpenRouter模型接口
   - 其他模型实现：支持Google、Anthropic、DeepSeek、豆包等

4. **配置模块**
   - `src/config/settings.py`: 全局设置
   - `src/config/redis_config.py`: Redis配置
   - `src/config/prompts/`: 提示词模板

5. **UI模块**
   - `ui/cli/terminal.py`: 命令行界面
   - `src/ui_enhanced/`: UI增强组件

### 2.2 数据流

```
用户输入 → 命令行界面 → 对话管理器 → 智能体交互 → 记忆存储 → 结果输出
                      ↓                  ↑
                   记忆查询          模型调用
                      ↓                  ↑
                   Redis存储        AI模型接口
```

### 2.3 Redis存储架构

- **键名设计**
  - `agent:{agent_id}:memory:{memory_id}`: 智能体记忆详情
  - `agent:{agent_id}:memories:list`: 智能体记忆列表（有序集合）
  - `agent:{agent_id}:memories:types`: 智能体记忆类型分组
  - `agent:{agent_id}:stats`: 智能体统计信息
  - `meeting:{session_id}:timeline`: 会议时间线
  - `meeting:{session_id}:speech:{speech_id}`: 发言详情
  - `meeting:{session_id}:participants`: 会议参与者
  - `meeting:{session_id}:stage`: 会议阶段

## 3. 主要模块详解

### 3.1 智能体系统

**代理类型**:
- 手工艺人 (craftsman)
- 消费者 (consumer)
- 制造商 (manufacturer)
- 设计师 (designer)

**智能体能力**:
- 自我介绍 (introduce)
- 讨论 (discuss)
- 关键词提取 (extract_keywords)
- 角色切换 (switch_role)
- 图像分析 (tell_story_from_image)
- 投票 (intelligent_vote)

### 3.2 记忆系统

**Redis记忆实现**:
- 使用哈希表和有序集合高效存储
- 按记忆类型分组
- 异步操作支持并发访问
- 自动清理过期记忆
- 本地缓存减少重复访问

**全局记忆功能**:
- 会话管理
- 时间线记录
- 上下文检索
- 状态统计

### 3.3 图像处理

**图像分析**:
- 使用视觉模型解读图像
- 生成图像关键词
- 整合图像信息到讨论

**图像生成**:
- 支持多种生成模型
- 优化提示词生成
- 自动处理和保存图像

### 3.4 用户界面

**美化命令行界面**:
- 彩色文本和渐变效果
- 加载动画和进度指示
- 装饰性面板和分隔线
- 主题切换功能

## 4. 核心流程

### 4.1 会话启动流程

```
加载配置 → 初始化Redis → 创建智能体 → 清理旧数据 → 启动界面
```

### 4.2 讨论流程

```
自我介绍 → 多轮讨论 → 关键词提取 → 投票 → 角色转换 → 设计生成
```

### 4.3 内存管理流程

```
会话开始 → 清理旧数据 → 记忆写入 → 索引更新 → 过期控制 → 会话结束
```

## 5. 技术特点

### 5.1 Redis统一存储

- 替代JSON文件存储，减少约800行冗余代码
- 提供高效的读写性能和数据持久性
- 支持复杂数据结构和查询操作

### 5.2 异步编程

- 使用asyncio实现非阻塞操作
- 支持并发API调用和Redis操作
- 异步流式输出支持实时显示

### 5.3 模型抽象

- 抽象基类定义通用接口
- 支持多种模型提供商切换
- 实现流式生成和图像处理

### 5.4 拟人化交互

- 个性化表达和说话风格
- 记忆连贯性和上下文感知
- 自然对话逻辑和情感表达

## 6. 部署架构

### 6.1 基础部署

```
[用户终端] ← → [Python应用] ← → [Redis服务器] ← → [外部AI API]
```

### 6.2 Docker部署

```
┌─────────────────────────────────┐
│          Docker Host            │
│ ┌───────────┐    ┌───────────┐  │
│ │ TableRound│    │  Redis    │  │
│ │ Container │◄──►│ Container │  │
│ └───────────┘    └───────────┘  │
└─────────────────────────────────┘
           ▲                ▲
           │                │
           ▼                ▼
┌────────────────┐  ┌─────────────┐
│ 用户终端/界面  │  │  外部AI API  │
└────────────────┘  └─────────────┘
```

## 7. 扩展与未来规划

1. **多模态交互**
   - 增强图像处理能力
   - 添加语音输入输出
   - 支持3D模型生成

2. **分布式部署**
   - Redis集群支持
   - 智能体分布式执行
   - 负载均衡机制

3. **界面升级**
   - Web界面开发
   - 移动端支持
   - 可视化交互展示

4. **功能扩展**
   - 更多智能体角色
   - 跨语言支持
   - 插件系统

---

*文档由weisiren创建于2025年6月24日* 