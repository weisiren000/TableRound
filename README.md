# 圆桌会议 (TableRound)

圆桌会议是一个基于多智能体对话的圆桌会议系统，专注于剪纸文创产品设计，采用两阶段AI架构，支持统一图像描述机制和智能记忆管理。

## 项目特点

- **多智能体系统**：六个不同角色的智能体（手工艺人、消费者×3、制造商、设计师）
- **两阶段AI架构**：视觉理解(Google Gemini) + 对话生成(DeepSeek R1)
- **统一图像描述**：避免重复调用视觉模型，一次描述全员共享
- **Redis统一记忆**：高性能统一存储方案，支持自动清理和备份
- **流式对话**：实时流式输出的多智能体对话
- **KJ法关键词提取**：智能体使用KJ法总结和分类关键词
- **角色扮演**：支持智能体角色转换和场景模拟
- **图像处理**：支持图片输入和智能体基于图片的故事讲述
- **设计生成**：基于关键词生成剪纸文创产品设计
- **UI美化**：增强的终端界面，支持多种主题和动画效果

## 安装与使用

### 环境要求

- Python 3.8+
- Redis服务器 (localhost:6379)
- AI API密钥：
  - OpenRouter API密钥 (推荐，支持多种模型)
  - 豆包API密钥 (图像生成)
  - Google Gemini API密钥 (视觉理解)
- 相关依赖包（见requirements.txt）

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/weisiren000/roundtable.git
cd tableround
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖
```bash
# 推荐使用uv包管理器
uv pip install -r requirements.txt
# 或使用传统pip
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，填入你的API密钥
```

5. 启动Redis服务器
```bash
# Windows (使用Docker)
docker run -d -p 6379:6379 redis:latest
# 或安装本地Redis服务
```

6. 运行程序
```bash
# 推荐使用uv
uv run run.py
# 或使用传统python
python run.py
```

## 项目结构

```
tableround/
├── data/                  # 数据目录
│   ├── images/            # 用户上传的图片
│   ├── keywords/          # 提取的关键词
│   └── memories/          # 智能体记忆备份
├── src/                   # 源代码目录
│   ├── agents/            # 智能体定义
│   ├── config/            # 配置模块 (模型、提示词、Redis等)
│   ├── core/              # 核心功能 (对话、记忆、会议清理等)
│   ├── models/            # 对接不同AI模型的接口
│   ├── ui_enhanced/       # UI美化模块 (颜色、图标、动画等)
│   └── utils/             # 工具函数
├── ui/                    # 用户界面
│   └── cli/               # 命令行界面
├── .env.example           # 环境变量示例
├── .gitignore             # Git忽略配置
├── arc.md                 # 项目架构文档
├── README.md              # 项目说明
├── requirements.txt       # 依赖列表
└── run.py                 # 启动脚本
```

## 使用示例

### 基本对话流程

1. 智能体自我介绍
2. 用户输入讨论主题
3. 智能体按顺序进行对话
4. 智能体提取关键词并投票
5. 用户输入关键词进入下一阶段
6. 智能体角色转换后继续讨论

### 图像处理流程

1. 用户输入图片路径
2. 智能体根据图片讲故事
3. 提取关键词
4. 可选择进入设计阶段

### 设计流程

1. 用户输入关键词
2. 智能体生成设计卡牌
3. 用户输入设计提示词
4. 系统生成设计图像
5. 可选择上传原型进行合并

## 命令行参数

- `--config`：配置文件路径，默认为`.env`
- `--log-level`：日志级别，可选值：DEBUG, INFO, WARNING, ERROR, CRITICAL，默认为INFO
- `--log-file`：日志文件路径，默认为`logs/app.log`
- `--no-console-log`：不输出日志到控制台

## 智能体角色

系统支持以下六个智能体角色：

1. **手工艺人1**：60岁的蒙古族传统剪纸传承人，从事蒙古族剪纸技艺长达50年
2. **消费者1**：关注产品的使用体验和价值
3. **消费者2**：关注产品的使用体验和价值
4. **消费者3**：关注产品的使用体验和价值
5. **制造商人1**：35岁的文化创意产品生产商，从事四年手工艺品生产和开发
6. **设计师1**：23岁的研究生设计师，有四年产品设计经验

### 对话顺序
智能体按特定顺序进行对话：手工艺人→消费者→制造商→消费者→设计师→消费者

## 技术架构

### 两阶段AI处理
- **第一阶段**: Google Gemini 2.0 Flash 进行图像视觉理解
- **第二阶段**: DeepSeek R1 进行多智能体对话生成
- **图像生成**: 豆包API (doubao-seedream-3-0-t2i) 生成设计图像

### Redis统一记忆系统
- **统一存储**: 所有智能体记忆统一存储在Redis中
- **自动清理**: 每次会议开始时自动清理旧数据
- **性能优化**: 支持TTL过期、批量操作、安全处理
- **备份机制**: 清理前自动备份重要数据

### UI增强功能
- **多主题支持**: 6种预设主题，支持动态切换
- **动画效果**: 加载动画、打字机效果、渐变动画
- **彩色输出**: 256色支持、RGB渐变、智能体专属颜色
- **进度指示**: 实时进度条、状态指示器

## 贡献指南

欢迎贡献代码、报告问题或提出改进建议。请遵循以下步骤：

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 联系方式

如有任何问题或建议，请通过以下方式联系我们：

- 电子邮件：cxyvsir04@gmail.com
- GitHub Issues：[https://github.com/weisiren000/roundtable/issues](https://github.com/weisiren000/roundtable/issues)
