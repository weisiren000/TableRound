# 圆桌会议 (TableRound)

圆桌会议是一个多智能体交互系统，支持多种AI模型，实现智能体之间的对话、讨论、关键词提取和角色扮演等功能。

## 项目特点

- **多智能体系统**：四个不同角色的智能体（手工艺人、消费者、制造商人、设计师）
- **流式对话**：实时流式输出的多智能体对话
- **KJ法关键词提取**：智能体使用KJ法总结和分类关键词
- **记忆模块**：支持上下文记忆，智能体能够记住之前的对话
- **角色扮演**：支持智能体角色转换和场景模拟
- **图像处理**：支持图片输入和智能体基于图片的故事讲述
- **设计生成**：基于关键词生成剪纸文创产品设计

## 安装与使用

### 环境要求

- Python 3.8+
- OpenAI API密钥（或其他兼容的API）
- 相关依赖包（见requirements.txt）

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/tableround.git
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
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，填入你的API密钥
```

5. 运行程序
```bash
python run.py
```

## 项目结构

```
tableround/
├── data/                  # 数据目录
│   ├── images/            # 图片目录
│   ├── keywords/          # 关键词目录
│   └── memories/          # 记忆目录
├── src/                   # 源代码目录
│   ├── agents/            # 智能体定义
│   ├── api/               # API接口
│   ├── config/            # 配置模块
│   ├── core/              # 核心功能
│   ├── models/            # AI模型接口
│   └── utils/             # 工具函数
├── ui/                    # 用户界面
│   └── cli/               # 命令行界面
├── .env.example           # 环境变量示例
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

系统支持以下四种智能体角色：

1. **手工艺人**：60岁的蒙古族传统剪纸承人，从事蒙古族剪纸技艺长达50年
2. **消费者**：关注产品的使用体验和价值
3. **制造商人**：35岁的文化创意产品生产商，从事四年手工艺品生产和开发
4. **设计师**：23岁的研究生设计师，有四年产品设计经验

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

- 电子邮件：your.email@example.com
- GitHub Issues：[https://github.com/yourusername/tableround/issues](https://github.com/yourusername/tableround/issues)
