# TableRound (圆桌会议)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

**TableRound (圆桌会议)** 是一个先进的、基于多智能体协作的AI系统。它模拟一个圆桌会议场景，让不同角色的AI智能体（如设计师、制造商等）协同工作，以解决复杂的问题和完成创造性任务。

项目利用Redis实现了一个统一、高效、可扩展的记忆系统，并支持动态切换多种大型语言模型（LLM），旨在为复杂工作流提供一个强大的自动化协作框架。

## 核心特性

- **多智能体协作**: 内置多种预设角色（消费者、手工艺人、设计师、制造商），模拟真实世界团队的工作流程。
- **持久化记忆系统**: 基于Redis构建，提供高效、可扩展的长期和短期记忆，确保对话的连贯性和深度。
- **可插拔模型架构**: 支持动态切换和集成多种AI模型（OpenAI, Google, Anthropic, DeepSeek, 豆包等）。
- **丰富的功能模块**:
  - **KJ法总结**: 自动对讨论内容进行关键词提取和归纳（`kj_method.py`）。
  - **上帝视角**: 提供一个全局监控和调试工具（`god_view.py`）。
  - **智能投票**: 智能体可以根据讨论内容进行投票决策（`voting.py`）。
- **增强的命令行界面 (CLI)**: 提供美观、易用的彩色终端界面，支持主题切换、动画效果和实时流式输出。
- **异步架构**: 全面采用 `asyncio`，实现高效的并发API请求和数据处理。

## 系统架构

系统通过对话管理器（Conversation）调度不同的智能体（Agents），所有交互和记忆都通过全局记忆模块（GlobalMemory）统一存入Redis，实现了逻辑与数据存储的分离。

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

## 快速开始

### 1. 环境准备

- 克隆本项目:
  ```bash
  git clone https://github.com/weisiren000/roundtable.git
  cd roundtable
  ```

- 安装 [Redis](https://redis.io/docs/getting-started/installation/) 并启动服务。

### 2. 安装依赖

- 建议使用虚拟环境:
  ```bash
  python -m venv venv
  # Windows
  venv\Scripts\activate
  # Linux / macOS
  source venv/bin/activate
  ```

- 安装依赖包:
  ```bash
  pip install -r requirements.txt
  ```

### 3. 配置环境

- 复制环境变量示例文件:
  ```bash
  copy .env.example .env
  ```
- 编辑 `.env` 文件，填入你的AI模型API密钥和Redis连接信息。
  ```env
  # 例如:
  OPENAI_API_KEY="sk-..."
  REDIS_URL="redis://localhost:6379/0"
  ```

### 4. 启动应用

- 运行主程序:
  ```bash
  python run.py
  ```
- 系统将启动命令行界面，你可以开始输入任务，观察智能体们的协作过程。

## 项目结构

```
roundtable/
├── data/               # 数据存储（图片、关键词等）
├── docs/               # 项目文档
├── src/
│   ├── agents/         # 定义不同角色的智能体
│   ├── config/         # 全局配置、模型设置和提示词模板
│   ├── core/           # 核心业务逻辑（对话、记忆、智能体基类等）
│   ├── models/         # 对接不同AI模型的接口
│   ├── ui_enhanced/    # UI美化组件
│   └── utils/          # 通用工具（日志、图像处理等）
├── ui/
│   └── cli/            # 命令行界面实现
├── ARCHITECTURE.md     # 详细的架构文档
├── requirements.txt    # Python依赖
└── run.py              # 项目启动脚本
```

## 贡献

欢迎通过Fork和Pull Request的方式为本项目做出贡献。

1. Fork 本项目。
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 提交一个 Pull Request。

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。