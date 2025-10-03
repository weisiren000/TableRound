# 智能体角色定义

根据提供的表格信息，我们需要更新系统中的智能体角色定义。本文档详细说明了每个智能体的属性和实现方法。

## 智能体角色概览

| 参与者身份 | 年龄 | 人物介绍 | 相关经历/经验 |
|----------|-----|---------|-------------|
| 手工艺人/智能体手工艺人角色 | 60 岁 | 蒙古族传统剪纸承人 | 从事蒙古族剪纸技艺长达 50 年 |
| 生产商/智能体生产商角色 | 35 岁 | 文化创意产品生产商 | 对文化创意产品的市场有相关了解，从事有四年手工艺品生产和开发的基础 |
| 设计师/智能体设计师角色 | 23 岁 | 研究生 | 有四年产品设计经验 |
| 消费者/智能体消费者 | 23 岁 | 学生 | 少数民族，喜欢购买具有文化特色的手工艺品 |
| 消费者/智能体消费者 | 27 岁 | 自由职业者 | 喜欢旅游，经常购买文化创意品 |
| 消费者/智能体消费者 | 22 岁 | 学生 | 经常购买文化创意品 |

## 实现计划

### 1. 更新智能体基类

在 `src/core/agent.py` 中，需要确保基类支持以下属性：

```python
class Agent:
    """智能体基类"""

    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        name: str,
        model: BaseModel,
        memory: Memory,
        **kwargs
    ):
        # 基本属性
        self.id = agent_id
        self.type = agent_type
        self.name = name
        self.model = model
        self.memory = memory
        
        # 通用角色属性
        self.age = kwargs.get("age", 30)  # 默认年龄
        self.background = kwargs.get("background", "")  # 人物介绍
        self.experience = kwargs.get("experience", "")  # 相关经历/经验
        
        # 其他属性...
```

### 2. 更新手工艺人智能体

在 `src/agents/craftsman.py` 中，需要更新手工艺人智能体的属性：

```python
class Craftsman(Agent):
    """手工艺人智能体类"""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        model: BaseModel,
        memory: Memory,
        **kwargs
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type="craftsman",
            name=name,
            model=model,
            memory=memory
        )
        
        # 手工艺人特定属性
        self.age = kwargs.get("age", 60)  # 年龄：60岁
        self.background = kwargs.get("background", "蒙古族传统剪纸承人")  # 人物介绍
        self.experience = kwargs.get("experience", "从事蒙古族剪纸技艺长达50年")  # 相关经历
        self.crafts = kwargs.get("crafts", ["剪纸", "刺绣", "木雕", "陶艺"])
        self.specialties = kwargs.get("specialties", ["传统工艺", "文化传承", "手工制作"])
```

### 3. 更新生产商智能体

在 `src/agents/manufacturer.py` 中，需要更新生产商智能体的属性：

```python
class Manufacturer(Agent):
    """制造商人智能体类"""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        model: BaseModel,
        memory: Memory,
        **kwargs
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type="manufacturer",
            name=name,
            model=model,
            memory=memory
        )
        
        # 制造商人特定属性
        self.age = kwargs.get("age", 35)  # 年龄：35岁
        self.background = kwargs.get("background", "文化创意产品生产商")  # 人物介绍
        self.experience = kwargs.get("experience", "对文化创意产品的市场有相关了解，从事有四年手工艺品生产和开发的基础")  # 相关经历
        self.company_size = kwargs.get("company_size", "中型")  # 小型、中型、大型
        self.production_capacity = kwargs.get("production_capacity", 5000)  # 每月产能
        self.specialties = kwargs.get("specialties", ["文创产品", "工艺品", "纪念品"])
```

### 4. 更新设计师智能体

在 `src/agents/designer.py` 中，需要更新设计师智能体的属性：

```python
class Designer(Agent):
    """设计师智能体类"""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        model: BaseModel,
        memory: Memory,
        **kwargs
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type="designer",
            name=name,
            model=model,
            memory=memory
        )
        
        # 设计师特定属性
        self.age = kwargs.get("age", 23)  # 年龄：23岁
        self.background = kwargs.get("background", "研究生")  # 人物介绍
        self.experience = kwargs.get("experience", "有四年产品设计经验")  # 相关经历
        self.design_style = kwargs.get("design_style", "融合传统与现代")
        self.specialties = kwargs.get("specialties", ["视觉设计", "产品设计", "文创设计"])
```

### 5. 更新消费者智能体

在 `src/agents/consumer.py` 中，需要支持多种消费者角色：

```python
class Consumer(Agent):
    """消费者智能体类"""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        model: BaseModel,
        memory: Memory,
        **kwargs
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type="consumer",
            name=name,
            model=model,
            memory=memory
        )
        
        # 消费者特定属性
        consumer_id = int(agent_id.split("_")[-1]) if "_" in agent_id else 1
        
        # 根据消费者ID设置不同的属性
        if consumer_id == 1:
            # 第一个消费者：学生，23岁
            self.age = kwargs.get("age", 23)
            self.background = kwargs.get("background", "学生")
            self.experience = kwargs.get("experience", "少数民族，喜欢购买具有文化特色的手工艺品")
            self.interests = kwargs.get("interests", ["文化", "艺术", "手工艺品"])
        elif consumer_id == 2:
            # 第二个消费者：自由职业者，27岁
            self.age = kwargs.get("age", 27)
            self.background = kwargs.get("background", "自由职业者")
            self.experience = kwargs.get("experience", "喜欢旅游，经常购买文化创意品")
            self.interests = kwargs.get("interests", ["旅游", "文化创意", "收藏"])
        else:
            # 第三个消费者：学生，22岁
            self.age = kwargs.get("age", 22)
            self.background = kwargs.get("background", "学生")
            self.experience = kwargs.get("experience", "经常购买文化创意品")
            self.interests = kwargs.get("interests", ["设计", "创意", "时尚"])
```

### 6. 更新智能体创建逻辑

在 `ui/cli/terminal.py` 中，需要更新智能体创建逻辑，确保使用正确的属性：

```python
def create_agents(settings: Settings, model: BaseModel) -> ConversationManager:
    """创建智能体"""
    logger = logging.getLogger("cli.create_agents")
    
    # 创建对话管理器
    god_view = GodView(settings)
    conversation_manager = ConversationManager(god_view, settings)
    
    # 智能体类型映射
    agent_types = {
        "craftsman": "手工艺人",
        "consumer": "消费者",
        "manufacturer": "制造商人",
        "designer": "设计师"
    }
    
    # 创建智能体
    for agent_type, count in settings.agent_counts.items():
        for i in range(count):
            agent_id = f"{agent_type}_{i+1}"
            agent_name = f"{agent_types.get(agent_type, agent_type)}{i+1}"
            
            # 创建记忆模块
            memory = Memory(
                agent_id=agent_id,
                storage_type=settings.memory_storage_type,
                max_tokens=settings.memory_max_tokens,
                settings=settings
            )
            
            # 根据智能体类型创建不同的智能体
            if agent_type == "craftsman":
                agent = Craftsman(
                    agent_id=agent_id,
                    name=agent_name,
                    model=model,
                    memory=memory
                )
            elif agent_type == "consumer":
                agent = Consumer(
                    agent_id=agent_id,
                    name=agent_name,
                    model=model,
                    memory=memory
                )
            elif agent_type == "manufacturer":
                agent = Manufacturer(
                    agent_id=agent_id,
                    name=agent_name,
                    model=model,
                    memory=memory
                )
            elif agent_type == "designer":
                agent = Designer(
                    agent_id=agent_id,
                    name=agent_name,
                    model=model,
                    memory=memory
                )
            else:
                # 默认使用基类
                agent = Agent(
                    agent_id=agent_id,
                    agent_type=agent_type,
                    name=agent_name,
                    model=model,
                    memory=memory
                )
            
            # 添加到对话管理器
            conversation_manager.add_agent(agent)
            
            logger.info(f"创建了智能体: {agent_name} ({agent_type})")
    
    return conversation_manager
```

## 实现步骤

1. 更新 `src/core/agent.py` 中的 Agent 基类，添加通用角色属性
2. 更新 `src/agents/craftsman.py` 中的 Craftsman 类，设置手工艺人属性
3. 更新 `src/agents/manufacturer.py` 中的 Manufacturer 类，设置生产商属性
4. 更新 `src/agents/designer.py` 中的 Designer 类，设置设计师属性
5. 更新 `src/agents/consumer.py` 中的 Consumer 类，支持多种消费者角色
6. 更新 `ui/cli/terminal.py` 中的智能体创建逻辑
7. 更新 `src/config/prompts.py` 中的角色描述，确保与新的角色定义一致

## 测试计划

1. 创建测试用例，验证每个智能体的属性是否正确设置
2. 测试自我介绍功能，确保介绍内容反映了智能体的背景和经验
3. 测试对话功能，确保智能体在对话中表现出符合其角色的特点
4. 测试角色转换功能，确保转换后的角色保留原有的背景和经验
