### 圆桌会议

### 描述
- 接入兼容OPENAI SDK的AI模型
- 流式输出
- 记忆模块，支持上下文记忆
- 智能体使用KJ法总结关键词
- 兼容多种API提供商。
```list
  - openai
  - google
  - anthropic
  - DeepSeek
  - OpenRouter
  - OpenAI Compatible
```
Google（model list）：
  - gemini-2.5-flash-preview-04-17
  - gemini-2.5-flash-preview-05-20
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

OpenRouter（model list）：
  - qwen/qwen3-235b-a22b:free
  - microsoft/phi-4-reasoning-plus:free
  - deepseek/deepseek-r1:free
  - deepseek/deepseek-chat-v3-0324:free
  - thudm/glm-4-32b:free
  - thudm/glm-z1-32b:free
  - moonshotai/kimi-vl-a3b-thinking:free
  - meta-llama/llama-4-maverick:free
  - meta-llama/llama-4-scout:free
注意：以上模型有思维模型，思维模型思考内容的标志是 <think>...</think>
base_url="https://openrouter.ai/api/v1"

```

### 功能设计
阶段1：
- 开头各智能体先进行自我介绍，然后进入讨论
- 上帝视角：可以观察多个AI之间的对话，并进行干预
- 设计记忆存储模块，帮助AI进行记忆
- 设计定义6个不同的智能体，每个智能体有不同的性格和记忆，他们分别是“1个手工艺人”、“3个消费者”、“1个制造商人”、“1个设计师”（1CRAFTSMAN, 3CONSUMERS, 1MANUFACTURER, 1DESIGNER）
- 对话顺序：手工艺人、消费者、制造商人、消费者、设计师、消费者
- 用户输入课题，AI根据课题进行对话讨论
- 第一个智能体回答得出关键词（KJ法总结关键词），第二个智能体可以有“认同、反对、补充”三种选择，如果认同，则继续，如果反对，则提出反对意见，如果补充，则提出补充意见。每个智能体可以有5-10个左右关键词。
- 模型进行一轮讨论之后会得到n个关键词。
- 最后经过一轮讨论之后，六个智能体会进入黑箱投票阶段，他们会进入六个独立的投票阶段，他们会思考然后投票选出之前由六个智能体讨论出的关键词中，他们认为最符合课题的关键词5-10个。

等待阶段：
- 在上一轮智能体投票结束之后，上帝视角会进行总结，并给出最终的关键词。（也就是等待上帝输入一个关键词，然后AI会根据这个关键词进行下一轮的对话）

阶段2：
- 角色带着上一轮对话的记忆进入角色转换阶段，智能体转化自己的角色（随机转换角色，只要不是上一轮的角色就行）
- 角色转换之后智能体再次进入对话阶段，他们会根据上帝给出的关键词然后带着上一轮对话的记忆进行角色转换思考，以不同的角色视角去思考问题（第一轮输入的问题），然后同理进行讨论、黑箱投票得出阶段二的n个关键词。

等待阶段：
- pass

### 一些描述
- 上帝视角：上帝视角可以观察多个AI之间的对话，对话是以群聊式的进行，文本以流式输出。
