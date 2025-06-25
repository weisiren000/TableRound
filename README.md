# TableRound (圆桌会议)

<div align="center">
  <img src="images/logo.png" alt="TableRound Logo" width="200"/>
  <p>基于多智能体的协作讨论平台</p>
</div>

## 项目简介

TableRound（圆桌会议）是一个基于多智能体协作的交互式讨论系统，通过模拟不同角色的智能体（手工艺人、消费者、制造商、设计师）共同参与讨论，实现创意发想与设计方案生成。系统采用Redis作为统一存储后端，支持记忆管理、关键词提取、角色转换、图像处理等功能。

## 核心特性

- **多智能体协作**：支持多种AI代理角色进行交互讨论
- **统一Redis存储**：高效的记忆管理和智能体状态存储
- **图像理解与生成**：支持图像分析和AI绘画生成
- **关键词提取与投票**：智能提取讨论要点并进行投票
- **角色动态切换**：支持智能体在不同角色间灵活转换
- **美化命令行界面**：直观友好的用户交互体验

## 快速开始

### 环境要求

- Python 3.8+
- Redis 6.0+
- Docker (可选，用于Redis部署)

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/weisiren000/roundtable.git
cd roundtable
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

复制示例配置文件并修改：

```bash
cp .env.example .env
# 编辑.env文件，填入API密钥等配置
```

5. 启动Redis (Docker方式)

```bash
docker run -d --name tableround-redis -p 6379:6379 redis
```

6. 运行程序

```bash
python run.py
```

## 使用指南

启动程序后，可通过命令行界面使用以下功能：

1. **开始新对话**：启动多智能体圆桌讨论
2. **处理图片**：上传图片进行智能分析
3. **设计剪纸文创**：基于关键词设计文创产品
4. **AI绘画图像测试**：快速提示词迭代测试
5. **关键词提取测试**：快速测试设计要素关键词提取

## 系统架构

详细架构说明请参考 [ARCHITECTURE.md](ARCHITECTURE.md)

## 技术栈

- **后端**：Python, asyncio
- **存储**：Redis
- **AI模型**：OpenAI, Anthropic, Google, DeepSeek, 豆包等
- **界面**：命令行增强UI

## 开发路线

- [ ] 多模态交互增强
- [ ] Web界面开发
- [ ] 分布式部署支持
- [ ] 更多智能体角色
- [ ] 社区版本发布

## 贡献指南

欢迎提交问题和贡献代码！请参考以下步骤：

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 作者

- **weisiren** - [GitHub](https://github.com/weisiren000)

## 致谢

- 感谢所有为项目做出贡献的开发者
- 特别感谢各大AI模型提供商提供的API支持

---

*更新日期: 2025年6月24日* 