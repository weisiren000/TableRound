# 角色转换与记忆机制实现指南

本文档详细说明了圆桌会议系统中角色转换和记忆机制的实现方法。

## 角色转换机制

### 关键要点

1. **转换为不同角色**：每个智能体需要转换成与自己原始身份不同的角色，而非预定义的其他智能体角色。

2. **保持记忆连续性**：角色转换后，智能体仍然保留之前的所有记忆，包括自己和其他智能体的发言。

3. **思维方式转变**：转换只是改变了思考问题的视角和方法，而不是完全变成另一个人。

4. **记忆贯穿整个对话**：智能体需要像人类一样，记住整个对话过程中的所有发言，直到本轮对话结束。

### 实现方案

#### 1. 角色转换机制

在 `src/core/agent.py` 中，需要更新 `switch_role` 方法：

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

#### 2. 提示词模板更新

在 `src/config/prompts.py` 中，更新角色转换提示词模板：

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

## 记忆机制

### 关键要点

1. **长期记忆**：智能体需要记住整个对话过程中的所有发言，包括自己和其他智能体的内容。

2. **记忆检索**：在对话过程中，智能体应能够检索和引用之前的发言。

3. **记忆连续性**：角色转换后，记忆仍然保持连续，不会丢失或重置。

4. **记忆格式化**：记忆需要以结构化的方式存储，便于检索和使用。

### 实现方案

#### 1. 记忆模块更新

在 `src/core/memory.py` 中，需要更新记忆模块：

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
```

#### 2. 对话管理更新

在 `src/core/conversation.py` 中，更新对话管理器，确保记忆在智能体之间共享：

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
        
        # 获取角色描述
        role_description = PromptTemplates.get_role_description(new_role)
        
        # 构建提示词
        prompt = f"""
        你现在需要从{agent.type}角色转换为{new_role}角色。
        
        {role_description}
        
        请记住，这只是一种思维方式的转变，你仍然记得之前所有的对话内容。
        请以新角色的身份简短介绍自己（100字以内），然后继续参与关于以下关键词的讨论：
        
        {', '.join(final_keywords)}
        """
        
        # 执行角色转换
        response = await agent.switch_role(new_role, self.topic)
        
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

## 实现注意事项

1. **提示词设计**：确保提示词明确指出智能体需要保持记忆连续性，只是换一种思维方式。

2. **记忆格式化**：记忆需要以结构化的方式存储，包含角色、主题、内容等信息。

3. **记忆检索**：在生成回复前，需要检索相关记忆，确保智能体能够引用之前的发言。

4. **角色分配**：确保每个智能体都转换为与自己原始身份不同的角色。

5. **系统提示词**：在系统提示词中强调记忆连续性和思维方式转变。

## 测试计划

1. **记忆连续性测试**：测试智能体在角色转换后是否能够正确引用之前的发言。

2. **角色转换测试**：测试智能体是否能够从原始角色转换为新角色，并保持记忆连续性。

3. **长期记忆测试**：测试智能体是否能够记住整个对话过程中的所有发言。

4. **思维方式测试**：测试智能体是否能够以新角色的视角思考问题，但保持记忆的连续性。
