#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试角色转换改进功能
验证：
1. 角色转换后不再自我介绍
2. 反思式角色转换
3. 避免发言风格同质化
"""

import asyncio
from src.core.agent import Agent
from src.core.memory_adapter import MemoryAdapter
from src.core.global_memory import GlobalMemory
from src.config.settings import Settings


async def test_role_switch_improvements():
    """测试角色转换改进功能"""
    print("🔧 测试角色转换改进功能...")
    print("=" * 60)
    
    # 初始化
    settings = Settings()
    
    # 创建全局记忆
    global_memory = GlobalMemory("test_session", storage_type="auto")
    
    # 创建不同角色的智能体
    agents = []
    
    # 手工艺人
    craftsman_memory = MemoryAdapter("test_craftsman", storage_type="auto", settings=settings)
    craftsman = Agent(
        agent_id="test_craftsman",
        agent_type="craftsman",
        name="张师傅",
        model=settings.get_model_instance("openrouter", "meta-llama/llama-4-maverick:free"),
        memory=craftsman_memory,
        global_memory=global_memory,
        age=65,
        background="蒙古族传统剪纸传承人",
        experience="从事剪纸艺术45年"
    )
    
    # 消费者
    consumer_memory = MemoryAdapter("test_consumer", storage_type="auto", settings=settings)
    consumer = Agent(
        agent_id="test_consumer",
        agent_type="consumer",
        name="小雪",
        model=settings.get_model_instance("openrouter", "meta-llama/llama-4-maverick:free"),
        memory=consumer_memory,
        global_memory=global_memory,
        age=23,
        background="大学生，文创产品爱好者",
        experience="市场营销专业，关注产品体验"
    )
    
    agents = [craftsman, consumer]
    
    # 添加参与者到全局记忆
    for agent in agents:
        await global_memory.add_participant(agent.id, agent.name, agent.type)
    
    print("\n1. 测试不同角色的说话风格")
    print("-" * 40)
    
    topic = "传统文化的现代传承"
    
    # 每个智能体先进行一次讨论，建立对话历史
    for agent in agents:
        print(f"\n【{agent.name}】({agent.type}) 初始发言:")
        response = await agent.discuss(topic)
        print(response[:200] + "..." if len(response) > 200 else response)
        
        # 记录到全局记忆
        await global_memory.record_speech(
            agent_id=agent.id,
            agent_name=agent.name,
            speech_type="discussion",
            content=response,
            stage="discussion"
        )
    
    print("\n2. 测试反思式角色转换")
    print("-" * 40)
    
    # 角色转换：手工艺人 → 消费者，消费者 → 设计师
    role_switches = [
        (craftsman, "consumer"),
        (consumer, "designer")
    ]
    
    for agent, new_role in role_switches:
        original_role = agent.current_role
        print(f"\n【{agent.name}】角色转换: {original_role} → {new_role}")
        
        # 执行角色转换
        response = await agent.switch_role(new_role, topic)
        print(response)
        
        # 检查是否包含反思元素
        reflection_indicators = [
            "之前", "刚才", "回顾", "反思", "想到", "现在从", "角度", "视角"
        ]
        
        found_indicators = [indicator for indicator in reflection_indicators if indicator in response]
        if found_indicators:
            print(f"✅ 包含反思元素: {', '.join(found_indicators)}")
        else:
            print("❌ 缺少反思元素")
        
        # 检查是否避免了自我介绍
        intro_indicators = [
            "我叫", "我是", "很高兴见到大家", "自我介绍", "我的名字"
        ]
        
        found_intro = [indicator for indicator in intro_indicators if indicator in response]
        if found_intro:
            print(f"❌ 包含自我介绍元素: {', '.join(found_intro)}")
        else:
            print("✅ 成功避免自我介绍")
    
    print("\n3. 测试说话风格差异化")
    print("-" * 40)
    
    # 重置智能体角色
    craftsman.current_role = "craftsman"
    consumer.current_role = "consumer"
    
    # 测试相同主题下不同角色的表达风格
    test_topic = "产品设计理念"
    
    responses = {}
    for agent in agents:
        print(f"\n【{agent.name}】({agent.current_role}) 对'{test_topic}'的看法:")
        response = await agent.discuss(test_topic)
        responses[agent.current_role] = response
        print(response[:150] + "..." if len(response) > 150 else response)
    
    # 分析风格差异
    print("\n风格差异分析:")
    
    # 检查是否使用了相同的开场白
    common_openings = [
        "我觉得这个话题真的很有意思",
        "嗯，我觉得",
        "这个话题很有意思"
    ]
    
    for opening in common_openings:
        agents_using = [role for role, response in responses.items() if opening in response]
        if len(agents_using) > 1:
            print(f"❌ 多个角色使用相同开场白 '{opening}': {', '.join(agents_using)}")
        else:
            print(f"✅ 开场白 '{opening}' 使用情况正常")
    
    # 检查角色特有的表达方式
    role_expressions = {
        "craftsman": ["传统", "工艺", "经验", "技艺", "这个嘛", "让我想想"],
        "consumer": ["感觉", "体验", "实用", "好用", "说实话", "我觉得"]
    }
    
    for role, expressions in role_expressions.items():
        if role in responses:
            found_expressions = [expr for expr in expressions if expr in responses[role]]
            if found_expressions:
                print(f"✅ {role} 使用了角色特有表达: {', '.join(found_expressions)}")
            else:
                print(f"❌ {role} 缺少角色特有表达")
    
    print("\n" + "=" * 60)
    print("🏁 角色转换改进功能测试完成")


if __name__ == "__main__":
    asyncio.run(test_role_switch_improvements())
