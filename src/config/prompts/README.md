# TableRound 提示词管理系统 v2.0

## 概述

这是TableRound项目的新一代模块化提示词管理系统。相比原来的集中式管理，新系统采用分散式文件管理，提供更好的可维护性和扩展性。

## 目录结构

```
src/config/prompts/
├── __init__.py                 # 模块初始化和统一导出
├── README.md                   # 本文档
├── base_prompts.py            # 基础通用提示词模板
├── template_manager.py        # 提示词管理器和向后兼容接口
├── agent_prompts/             # 智能体相关提示词
│   ├── __init__.py
│   ├── craftsman_prompts.py   # 手工艺人提示词
│   ├── consumer_prompts.py    # 消费者提示词
│   ├── manufacturer_prompts.py # 制造商提示词（待创建）
│   └── designer_prompts.py    # 设计师提示词（待创建）
└── function_prompts/          # 功能相关提示词
    ├── __init__.py
    ├── keyword_extraction_prompts.py  # 关键词提取
    ├── role_switch_prompts.py         # 角色转换（待创建）
    ├── image_story_prompts.py         # 图片故事（待创建）
    └── scenario_prompts.py            # 场景设置（待创建）
```

## 使用方法

### 1. 向后兼容使用（推荐用于现有代码）

```python
# 原有代码无需修改，自动使用新系统
from src.config.prompts import PromptTemplates

# 所有原有方法都可以正常使用
system_prompt = PromptTemplates.get_system_prompt("craftsman")
keyword_prompt = PromptTemplates.get_keyword_extraction_prompt(content, topic)
```

### 2. 新的模块化使用（推荐用于新代码）

```python
# 使用提示词管理器
from src.config.prompts import prompt_manager

# 基础功能
system_prompt = prompt_manager.get_system_prompt("craftsman")
intro_prompt = prompt_manager.get_introduction_prompt("consumer")

# 高级功能
keyword_prompt = prompt_manager.get_keyword_extraction_prompt(
    content, topic, extraction_type="hierarchical"
)

# 智能体特定功能
design_eval = prompt_manager.get_craftsman_design_evaluation_prompt(design)
```

### 3. 直接使用特定模块

```python
# 使用手工艺人专用提示词
from src.config.prompts.agent_prompts import CraftsmanPrompts

role_desc = CraftsmanPrompts.get_role_description()
material_prompt = CraftsmanPrompts.get_material_suggestion_prompt(design)

# 使用关键词提取专用提示词
from src.config.prompts.function_prompts import KeywordExtractionPrompts

basic_prompt = KeywordExtractionPrompts.get_basic_extraction_prompt(content, topic)
multilingual_prompt = KeywordExtractionPrompts.get_multilingual_prompt(content, topic)
```

## 新功能特性

### 1. 多种关键词提取模式

- **基础提取** (`basic`): 标准的5-10个关键词提取
- **多语言提取** (`multilingual`): 支持中英文混合处理
- **层次化提取** (`hierarchical`): 分为核心和扩展关键词
- **情感导向提取** (`sentiment`): 按情感倾向分类关键词

### 2. 智能体专业化提示词

每个智能体都有专门的提示词模块，包含：
- 角色描述和专业技能
- 特定功能的提示词
- 专业评估和建议模板

### 3. 灵活的配置管理

- 支持动态添加新角色
- 可以扩展新的提示词类型
- 提供版本管理和兼容性保证

## 扩展指南

### 添加新的智能体提示词

1. 在 `agent_prompts/` 目录下创建新文件，如 `new_agent_prompts.py`
2. 定义提示词类，继承或参考现有模式
3. 在 `template_manager.py` 中添加角色描述
4. 更新 `__init__.py` 文件导出新类

### 添加新的功能提示词

1. 在 `function_prompts/` 目录下创建新文件
2. 定义功能相关的提示词类
3. 在 `template_manager.py` 中添加相应方法
4. 更新导出配置

### 示例：创建新智能体

```python
# agent_prompts/marketing_prompts.py
class MarketingPrompts:
    ROLE_DESCRIPTION = "你是一位市场营销专家..."
    
    @staticmethod
    def get_campaign_strategy_prompt(product: str) -> str:
        return f"请为以下产品制定营销策略：{product}"
```

## 迁移指南

### 从旧系统迁移

1. **无需立即修改现有代码** - 向后兼容接口确保现有代码正常工作
2. **逐步迁移** - 新功能使用新接口，旧功能保持不变
3. **测试验证** - 确保迁移后功能正常

### 迁移步骤

1. 确认现有代码正常工作
2. 新功能使用 `prompt_manager` 或直接导入特定模块
3. 逐步替换旧的直接导入方式
4. 测试所有功能点

## 最佳实践

### 1. 提示词设计原则

- **模块化**: 每个文件专注特定功能
- **可复用**: 提取公共模板到基础类
- **可扩展**: 支持参数化和定制化
- **可测试**: 提供清晰的输入输出接口

### 2. 命名规范

- 文件名: `{功能}_prompts.py`
- 类名: `{功能}Prompts`
- 方法名: `get_{具体功能}_prompt`

### 3. 文档规范

- 每个类和方法都要有详细的文档字符串
- 提供使用示例和参数说明
- 说明提示词的适用场景和限制

## 性能考虑

### 1. 延迟加载

- 模块采用延迟加载，只在需要时导入
- 避免循环导入和不必要的依赖

### 2. 缓存机制

- 提示词管理器可以添加缓存机制
- 避免重复格式化相同的提示词

### 3. 内存优化

- 使用静态方法减少实例创建
- 合理使用字符串格式化和模板

## 版本历史

- **v2.0.0**: 模块化重构，支持分散式管理
- **v1.0.0**: 原始集中式管理系统

## 贡献指南

1. 遵循现有的代码风格和命名规范
2. 为新功能添加完整的文档和示例
3. 确保向后兼容性
4. 添加适当的测试用例

## 常见问题

### Q: 为什么要重构提示词管理系统？

A: 原来的集中式管理在项目规模增长后出现以下问题：
- 单文件过大，难以维护
- 多人协作时容易产生冲突
- 扩展新功能需要修改核心文件
- 缺乏专业化的提示词管理

### Q: 新系统如何保证向后兼容？

A: 通过 `template_manager.py` 中的 `PromptTemplates` 类提供完全兼容的接口，现有代码无需修改即可使用新系统。

### Q: 如何选择使用哪种接口？

A: 
- 现有代码：继续使用原有接口
- 新功能：使用 `prompt_manager` 或直接导入特定模块
- 高级功能：直接使用专业化的提示词类

### Q: 性能是否会受到影响？

A: 不会。新系统采用延迟加载和静态方法，性能与原系统相当或更好。