# 圆桌会议系统技术实现指南

本文档提供了圆桌会议系统各功能模块的技术实现指南，包括代码示例、API接口和实现思路。

## 1. 智能体自我介绍功能

### 1.1 修改智能体基类

在 `src/core/agent.py` 中，需要更新 `introduce()` 方法以限制字数：

```python
async def introduce(self) -> str:
    """
    智能体自我介绍

    Returns:
        自我介绍内容（限制300字以内）
    """
    self.logger.info(f"智能体 {self.name} 正在进行自我介绍")

    prompt = PromptTemplates.get_introduction_prompt(self.current_role)
    system_prompt = PromptTemplates.get_system_prompt(self.current_role)

    # 添加字数限制提示
    prompt += "\n\n请注意：自我介绍需控制在300字以内。"

    response = await self.model.generate(prompt, system_prompt)

    # 确保字数限制
    if len(response) > 600:  # 假设中文平均一个字符2个字节
        response = response[:600] + "..."

    # 将自我介绍存入记忆
    self.memory.add_memory(
        "introduction",
        {"role": self.current_role, "content": response}
    )

    return response
```

### 1.2 更新智能体提示词模板

在 `src/config/prompts.py` 中，更新自我介绍提示词模板：

```python
@staticmethod
def get_introduction_prompt(role: str) -> str:
    """获取自我介绍提示词"""
    return f"""
    你是一名{role}，请进行简短的自我介绍。

    在自我介绍中，请包含以下内容：
    1. 你的专业背景和经验
    2. 你关注的重点领域
    3. 你的工作方式

    请注意：
    - 自我介绍需控制在300字以内
    - 不要使用固定的性格特征描述自己
    - 保持语言自然流畅
    """
```

## 2. 图片故事讲述与关键词提取

### 2.1 实现图片处理功能

在 `src/utils/image.py` 中，确保图片处理功能支持多种格式：

```python
def prepare_image_for_api(self, image_path: str) -> Optional[str]:
    """
    准备图片用于API调用

    Args:
        image_path: 图片路径

    Returns:
        Base64编码的图片数据
    """
    try:
        # 支持的图片格式
        supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

        # 检查文件格式
        file_ext = os.path.splitext(image_path)[1].lower()
        if file_ext not in supported_formats:
            self.logger.error(f"不支持的图片格式: {file_ext}")
            return None

        # 读取图片
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    except Exception as e:
        self.logger.error(f"图片处理失败: {str(e)}")
        return None
```

### 2.2 实现智能体讲故事功能

在 `src/core/agent.py` 中，添加 `tell_story_from_image()` 方法：

```python
async def tell_story_from_image(self, image_path: str) -> Tuple[str, List[str]]:
    """
    根据图片讲故事并提取关键词

    Args:
        image_path: 图片路径

    Returns:
        故事内容和关键词列表
    """
    self.logger.info(f"智能体 {self.name} 正在根据图片讲故事")

    # 检查模型是否支持图像
    if not self.model.supports_vision():
        return "该模型不支持图像处理", []

    prompt = PromptTemplates.get_image_story_prompt(self.current_role)
    system_prompt = PromptTemplates.get_system_prompt(self.current_role)

    # 生成故事
    story = await self.model.generate_with_image(prompt, system_prompt, image_path)

    # 提取关键词
    keywords_prompt = f"""
    基于你刚才讲述的故事：

    {story}

    请提取5-10个关键词，这些关键词应该能够概括故事的核心元素和主题。

    请以JSON格式返回关键词列表，格式如下：
    ["关键词1", "关键词2", "关键词3", ...]
    """

    keywords_response = await self.model.generate(keywords_prompt, system_prompt)

    # 解析关键词
    try:
        # 尝试直接解析JSON
        keywords = json.loads(keywords_response)
    except:
        # 如果解析失败，尝试提取方括号内的内容
        match = re.search(r'\[(.*?)\]', keywords_response, re.DOTALL)
        if match:
            # 分割并清理关键词
            keywords_str = match.group(1)
            keywords = [k.strip().strip('"\'') for k in keywords_str.split(',')]
        else:
            # 如果仍然失败，使用简单的分行提取
            keywords = [line.strip().strip('"-,') for line in keywords_response.split('\n')
                       if line.strip() and not line.strip().startswith(('[', ']'))]

    # 确保关键词是列表类型
    if not isinstance(keywords, list):
        keywords = []

    # 限制关键词数量
    keywords = keywords[:10]

    # 将故事和关键词存入记忆
    self.memory.add_memory(
        "image_story",
        {
            "role": self.current_role,
            "story": story,
            "keywords": keywords,
            "image_path": image_path
        }
    )

    return story, keywords
```

### 2.3 在 `src/config/prompts.py` 中添加图片故事提示词：

```python
@staticmethod
def get_image_story_prompt(role: str) -> str:
    """获取图片故事提示词"""
    return f"""
    你是一名{role}，请根据提供的图片讲述一个故事。

    在讲述故事时，请基于你的身份和经验，进行联想和思维发散。故事应该：
    1. 与你的专业背景和经验相关
    2. 展现你对图片的独特理解和联想
    3. 包含丰富的细节和情感
    4. 长度控制在500字左右

    请注意：
    - 不要简单描述图片内容，而是要讲述一个有情节的故事
    - 故事应该有开头、发展和结尾
    - 可以自由发挥，但要保持与你的角色身份一致
    """
```

## 3. 智能体角色定义

### 3.1 更新智能体基类

在 `src/core/agent.py` 中，添加通用角色属性：

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
        """
        初始化智能体

        Args:
            agent_id: 智能体ID
            agent_type: 智能体类型
            name: 智能体名称
            model: AI模型
            memory: 记忆模块
            **kwargs: 其他参数
        """
        self.id = agent_id
        self.type = agent_type
        self.name = name
        self.model = model
        self.memory = memory
        self.logger = logging.getLogger(f"agent.{agent_type}.{agent_id}")

        # 智能体状态
        self.introduced = False
        self.current_role = agent_type
        self.original_role = agent_type
        self.keywords: List[str] = []

        # 通用角色属性
        self.age = kwargs.get("age", 30)  # 默认年龄
        self.background = kwargs.get("background", "")  # 人物介绍
        self.experience = kwargs.get("experience", "")  # 相关经历/经验
```

### 3.2 更新手工艺人智能体

在 `src/agents/craftsman.py` 中，更新手工艺人智能体的属性：

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
        """
        初始化手工艺人智能体

        Args:
            agent_id: 智能体ID
            name: 智能体名称
            model: AI模型
            memory: 记忆模块
            **kwargs: 其他参数
        """
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

        self.logger = logging.getLogger(f"agent.craftsman.{agent_id}")
```

### 3.3 更新制造商人智能体

在 `src/agents/manufacturer.py` 中，更新制造商人智能体的属性：

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
        """
        初始化制造商人智能体

        Args:
            agent_id: 智能体ID
            name: 智能体名称
            model: AI模型
            memory: 记忆模块
            **kwargs: 其他参数
        """
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
        self.manufacturing_methods = kwargs.get("manufacturing_methods", ["手工制作", "半自动化", "定制化生产"])

        self.logger = logging.getLogger(f"agent.manufacturer.{agent_id}")
```

### 3.4 更新设计师智能体

在 `src/agents/designer.py` 中，更新设计师智能体的属性：

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
        """
        初始化设计师智能体

        Args:
            agent_id: 智能体ID
            name: 智能体名称
            model: AI模型
            memory: 记忆模块
            **kwargs: 其他参数
        """
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
        self.design_philosophy = kwargs.get("design_philosophy", "在尊重传统的基础上创新，追求美学与实用的平衡")

        self.logger = logging.getLogger(f"agent.designer.{agent_id}")
```

### 3.5 更新消费者智能体

在 `src/agents/consumer.py` 中，更新消费者智能体的属性：

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
        """
        初始化消费者智能体

        Args:
            agent_id: 智能体ID
            name: 智能体名称
            model: AI模型
            memory: 记忆模块
            **kwargs: 其他参数
        """
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

        # 消费者通用属性
        self.gender = kwargs.get("gender", random.choice(["男", "女"]))
        self.preferences = kwargs.get("preferences", {
            "price_sensitivity": random.uniform(0.3, 0.9),  # 价格敏感度
            "quality_focus": random.uniform(0.5, 1.0),      # 质量关注度
            "design_focus": random.uniform(0.4, 0.9),       # 设计关注度
            "tradition_value": random.uniform(0.3, 0.8)     # 传统价值关注度
        })

        self.logger = logging.getLogger(f"agent.consumer.{agent_id}")
```

### 3.6 更新角色描述提示词

在 `src/config/prompts.py` 中，更新角色描述提示词：

```python
# 角色描述
ROLE_DESCRIPTIONS = {
    "craftsman": """你是一位60岁的蒙古族传统剪纸承人，从事蒙古族剪纸技艺长达50年。
你熟悉各种材料的特性和加工方法，对传统工艺有深厚的理解。
你注重作品的质量和工艺的传承，同时也关注如何将传统工艺与现代需求相结合。""",

    "consumer": """你是一位消费者，关注产品的使用体验和价值。
你代表市场上的普通用户，关心产品的实用性、美观性、价格和耐用性。
你的意见反映了大众消费者的需求和偏好，对产品的市场接受度有重要参考价值。""",

    "manufacturer": """你是一位35岁的文化创意产品生产商，从事四年手工艺品生产和开发。
你了解大规模生产的工艺流程和限制，能够评估设计方案的可行性。
你关注材料成本、生产效率、质量控制和供应链管理等方面的问题。""",

    "designer": """你是一位23岁的研究生设计师，有四年产品设计经验。
你擅长将创意转化为具体的设计方案，注重产品的视觉表达和用户体验。
你了解设计趋势和美学原则，能够平衡艺术性和实用性。"""
}
```

### 3.7 实现增强的记忆机制

在 `src/core/memory.py` 中，添加长期记忆功能：

```python
def get_all_memories(self) -> List[str]:
    """
    获取所有记忆

    Returns:
        所有记忆的文本表示
    """
    formatted_memories = []

    # 按时间戳排序
    sorted_memories = sorted(self.memories, key=lambda x: x.get("timestamp", 0))

    # 格式化每条记忆
    for memory in sorted_memories:
        formatted_memory = self._format_memory_as_text(memory)
        if formatted_memory:
            formatted_memories.append(formatted_memory)

    return formatted_memories

def get_conversation_history(self) -> str:
    """
    获取对话历史

    Returns:
        对话历史的文本表示
    """
    # 获取讨论类型的记忆
    discussion_memories = [m for m in self.memories if m.get("type") == "discussion"]

    # 按时间戳排序
    sorted_discussions = sorted(discussion_memories, key=lambda x: x.get("timestamp", 0))

    # 格式化对话历史
    history = []
    for memory in sorted_discussions:
        content = memory.get("content", {})
        role = content.get("role", "unknown")
        topic = content.get("topic", "unknown")
        text = content.get("content", "")

        history.append(f"{role} 关于 {topic} 的发言: {text}")

    return "\n\n".join(history)

def _format_memory_as_text(self, memory: Dict[str, Any]) -> str:
    """
    将记忆格式化为文本

    Args:
        memory: 记忆数据

    Returns:
        格式化后的文本
    """
    memory_type = memory.get("type", "")
    content = memory.get("content", {})
    timestamp = memory.get("timestamp", 0)

    # 格式化时间戳
    time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    # 根据记忆类型格式化内容
    if memory_type == "introduction":
        role = content.get("role", "unknown")
        text = content.get("content", "")
        return f"[{time_str}] 自我介绍 ({role}): {text}"

    elif memory_type == "discussion":
        role = content.get("role", "unknown")
        topic = content.get("topic", "unknown")
        text = content.get("content", "")
        return f"[{time_str}] 讨论 ({role} 关于 {topic}): {text}"

    elif memory_type == "keywords":
        role = content.get("role", "unknown")
        topic = content.get("topic", "unknown")
        keywords = content.get("keywords", [])
        keywords_str = ", ".join(keywords)
        return f"[{time_str}] 关键词 ({role} 关于 {topic}): {keywords_str}"

    elif memory_type == "voting":
        role = content.get("role", "unknown")
        topic = content.get("topic", "unknown")
        voted_keywords = content.get("voted_keywords", [])
        voted_str = ", ".join([k[0] for k in voted_keywords])
        return f"[{time_str}] 投票 ({role} 关于 {topic}): {voted_str}"

    elif memory_type == "role_switch":
        previous_role = content.get("previous_role", "unknown")
        new_role = content.get("new_role", "unknown")
        return f"[{time_str}] 角色转换: 从 {previous_role} 转换为 {new_role}"

    elif memory_type == "image_story":
        role = content.get("role", "unknown")
        story = content.get("story", "")
        keywords = content.get("keywords", [])
        keywords_str = ", ".join(keywords)
        return f"[{time_str}] 图片故事 ({role}): {story}\n关键词: {keywords_str}"

    elif memory_type == "design":
        role = content.get("role", "unknown")
        design = content.get("design", "")
        keywords = content.get("keywords", [])
        keywords_str = ", ".join(keywords)
        return f"[{time_str}] 设计方案 ({role}): {design}\n关键词: {keywords_str}"

    else:
        # 默认格式化
        return f"[{time_str}] {memory_type}: {str(content)}"
```

### 3.8 改进角色转换机制

在 `src/core/agent.py` 中，更新 `switch_role` 方法：

```python
async def switch_role(self, new_role: str, topic: str) -> str:
    """
    转换角色

    Args:
        new_role: 新角色
        topic: 讨论主题

    Returns:
        角色转换后的自我介绍
    """
    self.logger.info(f"智能体 {self.name} 正在从 {self.current_role} 转换为 {new_role}")

    # 保存原始角色
    original_role = self.current_role

    # 更新当前角色
    self.current_role = new_role

    # 获取角色转换提示词
    prompt = PromptTemplates.get_role_switch_prompt(
        original_role=original_role,
        new_role=new_role,
        topic=topic
    )

    # 获取系统提示词
    system_prompt = f"""你现在需要从{original_role}角色转换为{new_role}角色。
请记住，这只是一种思维方式的转变，你仍然记得之前所有的对话内容和你的原始身份。
你需要以新的视角思考问题，但保持记忆的连续性。
请以新角色的身份简短介绍自己（100字以内），然后继续参与关于"{topic}"的讨论。"""

    # 获取相关记忆
    memories = self.memory.get_all_memories()
    if memories:
        memory_text = "\n\n你的记忆:\n" + "\n".join(memories)
        prompt += memory_text

    # 生成角色转换后的自我介绍
    response = await self.model.generate(prompt, system_prompt)

    # 将角色转换记录存入记忆
    self.memory.add_memory(
        "role_switch",
        {
            "previous_role": original_role,
            "new_role": new_role,
            "topic": topic,
            "introduction": response
        }
    )

    return response
```

在 `src/config/prompts.py` 中，更新角色转换提示词：

```python
# 角色转换提示词
ROLE_SWITCH_PROMPT = """你现在需要从原来的{original_role}角色转换为{new_role}角色。

重要说明：
1. 这只是一种思维方式的转变，你仍然记得之前所有的对话内容
2. 你需要以新的视角思考问题，但保持记忆的连续性
3. 你不是在扮演预定义的其他智能体，而是采用一个全新的角色

作为{new_role}，你应该：
- 从{new_role}的视角思考问题
- 保持对之前讨论内容的记忆
- 考虑{new_role}可能关注的独特方面

请以新角色的身份简短介绍自己（100字以内），然后继续参与关于"{topic}"的讨论。
"""
```

在 `src/core/conversation.py` 中，更新角色转换逻辑：

```python
async def start_role_switch(self, final_keywords: List[str]) -> None:
    """
    开始角色转换阶段

    Args:
        final_keywords: 最终关键词列表
    """
    self.logger.info("开始角色转换阶段")

    # 设置最终关键词
    self.final_keywords = final_keywords

    # 更新阶段
    self.stage = "role_switch"

    # 获取所有智能体
    agents = list(self.agents.values())

    # 为每个智能体分配一个不同的角色
    roles = [agent.type for agent in agents]
    new_roles = roles.copy()
    random.shuffle(new_roles)

    # 确保每个智能体都转换为不同的角色
    while any(r1 == r2 for r1, r2 in zip(roles, new_roles)):
        random.shuffle(new_roles)

    # 角色转换
    for agent, new_role in zip(agents, new_roles):
        # 确保不转换为自己的原始角色
        if new_role == agent.type:
            # 找一个不同的角色
            available_roles = [r for r in roles if r != agent.type]
            new_role = random.choice(available_roles)

        # 执行角色转换
        self.logger.info(f"智能体 {agent.name} 从 {agent.type} 转换为 {new_role}")

        # 构建关键词字符串
        keywords_str = ", ".join(final_keywords)

        # 执行角色转换
        response = await agent.switch_role(new_role, keywords_str)

        # 流式输出
        await self.stream_handler.stream_output(
            f"【{agent.name}】从 {agent.type} 转换为 {new_role}:\n{response}\n"
        )

        # 添加到讨论历史
        self.discussion_history.append({
            "stage": "role_switch",
            "agent": agent.name,
            "original_role": agent.type,
            "new_role": new_role,
            "content": response
        })

    # 更新阶段
    self.stage = "discussion_after_switch"

    # 开始角色转换后的讨论
    await self.start_discussion_after_switch()
```

## 4. 关键词提取与KJ法分类

### 3.1 更新KJ法实现

在 `src/core/kj_method.py` 中，实现KJ法关键词分类：

```python
def categorize_keywords(self, keywords: List[str]) -> List[str]:
    """
    使用KJ法对关键词进行分类

    Args:
        keywords: 关键词列表

    Returns:
        分类后的关键词列表
    """
    self.logger.info(f"使用KJ法对 {len(keywords)} 个关键词进行分类")

    if not keywords:
        return []

    # 准备提示词
    prompt = f"""
    请使用KJ法对以下关键词进行分类和归纳：

    {', '.join(keywords)}

    KJ法是一种将分散的信息归纳整理的方法，步骤如下：
    1. 将所有关键词分组，将相似或相关的关键词放在一起
    2. 为每组关键词提炼一个上位概念或类别名称
    3. 进一步将这些类别归纳为更高层次的概念

    请返回分类结果，格式如下：

    一级类别1：[上位概念1]
    - 二级类别1.1：[上位概念1.1]
      - 关键词1
      - 关键词2
    - 二级类别1.2：[上位概念1.2]
      - 关键词3
      - 关键词4

    一级类别2：[上位概念2]
    - 二级类别2.1：[上位概念2.1]
      - 关键词5
      - 关键词6

    最后，请提供一个总结性的核心概念，概括所有关键词的共同主题。
    """

    # 使用模型进行分类
    response = self.model.generate(prompt)

    # 解析分类结果
    # 这里简化处理，直接返回模型生成的文本
    # 实际应用中可能需要更复杂的解析逻辑

    return [response]
```

### 3.2 实现关键词合并功能

在 `src/core/conversation.py` 中，添加关键词合并方法：

```python
def merge_keywords(self, kj_keywords: str, user_keywords: List[str]) -> List[str]:
    """
    合并KJ法分类结果和用户输入的关键词

    Args:
        kj_keywords: KJ法分类结果
        user_keywords: 用户输入的关键词

    Returns:
        合并后的关键词列表
    """
    self.logger.info("合并KJ法关键词和用户关键词")

    # 准备提示词
    prompt = f"""
    请将以下两组关键词合并，生成一组新的关键词：

    KJ法分类结果：
    {kj_keywords}

    用户输入的关键词：
    {', '.join(user_keywords)}

    请生成10个能够概括这两组关键词核心内容的新关键词，这些关键词将用于指导后续的角色扮演和设计讨论。

    请以JSON格式返回关键词列表，格式如下：
    ["关键词1", "关键词2", "关键词3", ...]
    """

    # 使用模型生成合并关键词
    response = self.model.generate(prompt)

    # 解析关键词
    try:
        merged_keywords = json.loads(response)
    except:
        # 解析失败时的备选方案
        match = re.search(r'\[(.*?)\]', response, re.DOTALL)
        if match:
            keywords_str = match.group(1)
            merged_keywords = [k.strip().strip('"\'') for k in keywords_str.split(',')]
        else:
            merged_keywords = [line.strip().strip('"-,') for line in response.split('\n')
                              if line.strip() and not line.strip().startswith(('[', ']'))]

    # 确保关键词是列表类型
    if not isinstance(merged_keywords, list):
        merged_keywords = []

    # 限制关键词数量
    merged_keywords = merged_keywords[:10]

    return merged_keywords
```

## 4. 剪纸文创产品设计场景

### 4.1 实现虚拟场景设置

在 `src/config/prompts.py` 中，添加剪纸研讨会场景描述：

```python
@staticmethod
def get_paper_cutting_scenario() -> str:
    """获取剪纸研讨会场景描述"""
    return """
    场景：你们正在参加一个剪纸文创产品设计研讨会。

    研讨会目标：设计出一个让消费者都满意的剪纸文创产品，以对称的剪纸风格的中国传统蝙蝠吉祥纹样为设计主题。

    蝙蝠在中国传统文化中象征着福气，因为"蝠"与"福"谐音。对称的剪纸风格是中国传统民间艺术的重要表现形式，具有浓厚的文化底蕴和艺术价值。

    在这个研讨会中，每位参与者都应该基于自己的专业背景和经验，为剪纸文创产品设计提供独特的见解和建议。最终，你们需要共同设计出一个既保留传统文化元素，又符合现代审美和使用需求的剪纸文创产品。
    """
```

### 4.2 实现设计卡牌生成

在 `src/core/agent.py` 中，添加设计卡牌生成方法：

```python
async def generate_design_card(self, keywords: List[str]) -> str:
    """
    生成设计卡牌

    Args:
        keywords: 关键词列表

    Returns:
        设计卡牌内容
    """
    self.logger.info(f"智能体 {self.name} 正在生成设计卡牌")

    # 获取剪纸研讨会场景描述
    scenario = PromptTemplates.get_paper_cutting_scenario()

    # 准备提示词
    prompt = f"""
    {scenario}

    基于以下关键词：
    {', '.join(keywords)}

    请你作为一名{self.current_role}，为对称的剪纸风格的中国传统蝙蝠吉祥纹样文创产品设计提供你的想法和建议。

    请包含以下内容：
    1. 产品形式（如：贴纸、书签、灯饰、壁挂等）
    2. 设计元素（如：色彩、图案、材质等）
    3. 功能特点（如：实用性、装饰性、收藏价值等）
    4. 目标用户（如：年龄段、兴趣爱好、消费习惯等）
    5. 文化内涵（如：传统象征意义、现代诠释等）

    请以设计卡牌的形式呈现你的想法，内容应该简洁明了，突出重点。
    """

    system_prompt = PromptTemplates.get_system_prompt(self.current_role)

    # 生成设计卡牌
    design_card = await self.model.generate(prompt, system_prompt)

    # 将设计卡牌存入记忆
    self.memory.add_memory(
        "design_card",
        {
            "role": self.current_role,
            "keywords": keywords,
            "content": design_card
        }
    )

    return design_card
```

## 5. 提示词生成纹样设计

### 5.1 实现提示词处理

在 `src/utils/image.py` 中，添加提示词处理方法：

```python
def optimize_image_prompt(self, user_prompt: str) -> str:
    """
    优化图像生成提示词

    Args:
        user_prompt: 用户输入的提示词

    Returns:
        优化后的提示词
    """
    # 基础提示词，确保生成的图像符合要求
    base_prompt = "对称的剪纸风格的中国传统蝙蝠吉祥纹样，"

    # 添加细节描述
    details = "精细的剪纸纹理，传统中国红色调，对称构图，"

    # 添加风格描述
    style = "中国传统民间艺术风格，平面设计，简洁清晰的线条，"

    # 组合提示词
    optimized_prompt = f"{base_prompt}{details}{style}{user_prompt}"

    return optimized_prompt
```

### 5.2 实现图像生成接口

在 `src/utils/image.py` 中，添加图像生成方法：

```python
async def generate_image(self, prompt: str, size: str = "1024x1024") -> Optional[str]:
    """
    生成图像

    Args:
        prompt: 提示词
        size: 图像尺寸

    Returns:
        生成的图像路径
    """
    try:
        # 优化提示词
        optimized_prompt = self.optimize_image_prompt(prompt)

        # 调用图像生成API
        # 这里使用OpenAI的DALL-E作为示例，实际应用中可能需要替换为其他API
        response = await self.client.images.generate(
            model="dall-e-3",
            prompt=optimized_prompt,
            size=size,
            quality="standard",
            n=1,
        )

        # 获取图像URL
        image_url = response.data[0].url

        # 下载图像
        image_data = requests.get(image_url).content

        # 生成文件名
        timestamp = int(time.time())
        file_name = f"design_{timestamp}.png"
        file_path = os.path.join(self.settings.IMAGE_DIR, file_name)

        # 保存图像
        with open(file_path, "wb") as f:
            f.write(image_data)

        return file_path

    except Exception as e:
        self.logger.error(f"图像生成失败: {str(e)}")
        return None
```

## 6. 实现命令行界面功能

在 `ui/cli/terminal.py` 中，添加设计流程相关功能：

```python
async def design_paper_cutting_flow(conversation_manager: ConversationManager):
    """
    剪纸文创产品设计流程

    Args:
        conversation_manager: 对话管理器
    """
    logger = logging.getLogger("cli.design_flow")

    print("\n" + "=" * 50)
    print("剪纸文创产品设计流程")
    print("=" * 50 + "\n")

    # 步骤1：上传图片，智能体讲故事
    print("步骤1: 上传图片，智能体讲故事\n")

    image_path = input("请输入图片路径: ")
    if not os.path.exists(image_path):
        print(f"错误: 图片 {image_path} 不存在")
        return

    logger.info(f"处理图片: {image_path}")

    print("\n正在处理图片...\n")
    keywords = await conversation_manager.process_image(image_path)

    print(f"\n提取的关键词: {', '.join(keywords)}")

    # 步骤2：用户输入关键词
    print("\n步骤2: 请输入您的关键词\n")

    user_keywords_input = input("请输入关键词（用逗号分隔）: ")
    user_keywords = [kw.strip() for kw in user_keywords_input.split(",") if kw.strip()]

    if not user_keywords:
        print("未输入关键词，使用系统提取的关键词")
        user_keywords = keywords

    # 步骤3：合并关键词，进入角色扮演阶段
    print("\n步骤3: 角色扮演阶段 - 剪纸研讨会\n")

    merged_keywords = conversation_manager.merge_keywords(keywords, user_keywords)

    print(f"合并后的关键词: {', '.join(merged_keywords)}")
    print("\n正在进入剪纸研讨会场景...\n")

    # 设置虚拟场景
    scenario = PromptTemplates.get_paper_cutting_scenario()
    print(scenario + "\n")

    # 智能体生成设计卡牌
    design_cards = {}
    for agent_id, agent in conversation_manager.agents.items():
        design_card = await agent.generate_design_card(merged_keywords)
        design_cards[agent_id] = design_card

        print(f"\n{agent.name} ({agent.type}) 的设计卡牌:\n")
        print(design_card + "\n")
        print("-" * 50)

    # 步骤4：用户输入设计提示词
    print("\n步骤4: 请输入设计提示词\n")

    design_prompt = input("请输入设计提示词: ")
    if not design_prompt:
        print("未输入设计提示词，使用默认提示词")
        design_prompt = "传统中国红色调，对称蝙蝠图案，吉祥如意"

    # 步骤5：生成设计图
    print("\n步骤5: 生成设计图\n")

    print("正在生成设计图...")
    image_path = await conversation_manager.generate_design_image(design_prompt)

    if image_path:
        print(f"\n设计图已生成: {image_path}")
    else:
        print("\n设计图生成失败")

    # 步骤6：用户上传原型
    print("\n步骤6: 请上传您的原型设计\n")

    user_prototype_path = input("请输入原型图片路径（留空跳过）: ")

    if user_prototype_path and os.path.exists(user_prototype_path):
        print("\n步骤7: 合并原型设计\n")

        final_design = await conversation_manager.merge_prototypes(image_path, user_prototype_path)

        if final_design:
            print(f"\n最终设计已生成: {final_design}")
        else:
            print("\n最终设计生成失败")

    print("\n设计流程完成！")
```

## 7. 实现数据结构

### 7.1 设计卡牌数据结构

在 `src/core/models.py` 中，添加设计卡牌数据类：

```python
class DesignCard:
    """设计卡牌类"""

    def __init__(
        self,
        card_id: str,
        agent_id: str,
        agent_type: str,
        content: str,
        keywords: List[str],
        timestamp: int = None
    ):
        """
        初始化设计卡牌

        Args:
            card_id: 卡牌ID
            agent_id: 智能体ID
            agent_type: 智能体类型
            content: 卡牌内容
            keywords: 关键词列表
            timestamp: 时间戳
        """
        self.card_id = card_id
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.content = content
        self.keywords = keywords
        self.timestamp = timestamp or int(time.time())

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "card_id": self.card_id,
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "content": self.content,
            "keywords": self.keywords,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DesignCard':
        """从字典创建设计卡牌"""
        return cls(
            card_id=data["card_id"],
            agent_id=data["agent_id"],
            agent_type=data["agent_type"],
            content=data["content"],
            keywords=data["keywords"],
            timestamp=data["timestamp"]
        )

    def save(self, directory: str) -> str:
        """
        保存设计卡牌

        Args:
            directory: 保存目录

        Returns:
            保存路径
        """
        os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, f"card_{self.card_id}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

        return file_path
```

## 8. 实现测试用例

在 `tests/test_design_flow.py` 中，添加设计流程测试：

```python
class TestDesignFlow(unittest.TestCase):
    """设计流程测试类"""

    def setUp(self):
        """测试前准备"""
        # 获取API密钥
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            self.skipTest("缺少OpenAI API密钥")

        # 创建模型
        self.model = OpenAIModel(
            model_name="gpt-4",
            api_key=self.api_key
        )

        # 创建设置
        self.settings = Settings()

        # 创建上帝视角
        self.god_view = GodView(self.settings)

        # 创建对话管理器
        self.conversation_manager = ConversationManager(self.god_view, self.settings)

        # 创建临时目录
        self.test_dir = ROOT_DIR / "tests" / "temp"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """测试后清理"""
        # 清理临时文件
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @unittest.skip("需要手动运行")
    def test_design_flow(self):
        """测试设计流程"""
        # 创建测试智能体
        self._create_test_agents()

        # 测试图片路径
        image_path = ROOT_DIR / "tests" / "data" / "test_image.jpg"

        # 测试关键词
        keywords = ["传统", "对称", "吉祥", "蝙蝠", "剪纸", "红色", "文化", "艺术", "设计", "创新"]

        # 测试设计卡牌生成
        for agent_id, agent in self.conversation_manager.agents.items():
            design_card = asyncio.run(agent.generate_design_card(keywords))

            # 验证设计卡牌
            self.assertIsInstance(design_card, str)
            self.assertTrue(len(design_card) > 0)
            print(f"{agent.name} 的设计卡牌:\n{design_card[:100]}...\n")

    def _create_test_agents(self):
        """创建测试智能体"""
        agent_types = {
            "craftsman": "手工艺人",
            "consumer": "消费者",
            "manufacturer": "制造商人",
            "designer": "设计师"
        }

        for i, (agent_type, agent_name) in enumerate(agent_types.items()):
            memory = Memory(
                agent_id=f"test_{agent_type}",
                storage_type="file",
                max_tokens=1000
            )

            agent = Agent(
                agent_id=f"test_{agent_type}",
                agent_type=agent_type,
                name=f"测试{agent_name}",
                model=self.model,
                memory=memory
            )

            self.conversation_manager.add_agent(agent)
```
