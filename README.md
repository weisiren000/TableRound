# Roundtable 项目

## 项目描述

Roundtable 是一个基于多代理协作的 AI 系统，模拟圆桌会议场景，用于处理复杂任务。系统集成了多种 AI 模型（如 OpenAI、Anthropic、DeepSeek 等），支持记忆管理、提示模板、图像处理和 UI 增强。核心功能包括代理角色（如消费者、工匠、设计师、制造商）、全局记忆、会议清理和投票机制。

该项目旨在提供一个高效的 AI 协作框架，支持从数据处理到生成式任务的端到端流程。

## 特性

- **多代理系统**：支持消费者（consumer）、工匠（craftsman）、设计师（designer）和制造商（manufacturer）等角色代理。
- **模型集成**：兼容 OpenAI、Anthropic、Google、DeepSeek、Doubao 和 OpenRouter 等模型。
- **记忆管理**：使用 Redis 作为后端，支持全局记忆和会话记忆。
- **提示模板**：模块化提示系统，包括代理提示和功能提示（如关键词提取、图像故事生成）。
- **UI 增强**：CLI 终端界面，支持动画、颜色主题和图标。
- **工具支持**：图像压缩、流式输出、日志记录和 KJ 方法（亲和图法）用于会议总结。
- **数据处理**：支持图像、关键词和记忆文件处理。

## 安装

1. 克隆仓库：
   ```
   git clone git@github.com:weisiren000/roundtable.git
   cd roundtable
   ```

2. 创建虚拟环境（推荐）：
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

4. 配置环境变量：
   - 复制 `.env.example` 为 `.env` 并填写必要的 API 密钥（如 OPENAI_API_KEY、REDIS_URL 等）。

5. 安装 Redis（如果未安装）：
   - 下载并启动 Redis 服务器。

## 用法

1. 运行主程序：
   ```
   python run.py
   ```

2. 通过 CLI 界面交互：
   - 系统将启动终端 UI，支持输入查询、查看代理交互和输出结果。
   - 示例：输入一个任务描述，系统将分配代理角色进行协作处理。

3. 自定义配置：
   - 编辑 `src/config/settings.py` 以调整模型和代理行为。
   - 使用 `src/config/prompts/` 中的模板自定义提示。

## 项目结构

```
roundtable/
├── .augmentignore
├── .env.example
├── .gitignore
├── ARCHITECTURE.md
├── CLAUDE.md
├── LICENSE
├── requirements.txt
├── run.py
├── data/
│   ├── images.zip
│   ├── keywords/
│   └── memories/
├── logs/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── agents/
│   │   ├── consumer.py
│   │   ├── craftsman.py
│   │   ├── designer.py
│   │   └── manufacturer.py
│   ├── config/
│   │   ├── models.py
│   │   ├── redis_config.py
│   │   ├── settings.py
│   │   └── prompts/
│   │       ├── __init__.py
│   │       ├── base_prompts.py
│   │       ├── template_manager.py
│   │       ├── agent_prompts/
│   │       └── function_prompts/
│   ├── core/
│   │   ├── agent.py
│   │   ├── conversation.py
│   │   ├── global_memory.py
│   │   ├── god_view.py
│   │   ├── kj_method.py
│   │   ├── meeting_cleaner.py
│   │   ├── memory_adapter.py
│   │   └── redis_memory.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── anthropic.py
│   │   ├── base.py
│   │   ├── deepseek.py
│   │   ├── doubao.py
│   │   ├── github.py
│   │   ├── google.py
│   │   ├── openai.py
│   │   └── openrouter.py
│   ├── ui_enhanced/
│   │   ├── __init__.py
│   │   ├── animations.py
│   │   ├── enhanced_colors.py
│   │   ├── icons.py
│   │   ├── themes.py
│   │   └── ui_components.py
│   └── utils/
│       ├── colors.py
│       ├── image_compressor.py
│       ├── image.py
│       ├── logger.py
│       ├── stream.py
│       └── voting.py
└── ui/
    └── cli/
        └── terminal.py
```

## 贡献

1. Fork 项目。
2. 创建分支：`git checkout -b feature-branch`。
3. 提交更改：`git commit -am 'Add new feature'`。
4. 推送分支：`git push origin feature-branch`。
5. 创建 Pull Request。

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系

如有问题，请通过 GitHub Issues 提交。