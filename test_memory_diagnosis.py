#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
记忆功能诊断工具
用于检查记忆存储、检索和使用情况
"""

import asyncio
import json
from datetime import datetime
from src.core.memory_adapter import MemoryAdapter
from src.core.global_memory import GlobalMemory
from src.config.redis_config import get_redis_client, RedisSettings
from src.config.settings import Settings


async def diagnose_memory_system():
    """诊断记忆系统的各个环节"""
    print("🔍 开始记忆系统诊断...")
    print("=" * 60)
    
    # 1. 检查Redis连接
    print("\n1. 检查Redis连接状态")
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
        print("✅ Redis连接正常")
        
        # 检查Redis中的数据
        keys = []
        async for key in redis_client.scan_iter(match="agent:*"):
            keys.append(key.decode('utf-8'))
        
        print(f"📊 Redis中存储的agent相关key数量: {len(keys)}")
        if keys:
            print("🔑 部分key示例:")
            for key in keys[:5]:
                print(f"   - {key}")
                
    except Exception as e:
        print(f"❌ Redis连接失败: {str(e)}")
        return False
    
    # 2. 检查个人记忆功能
    print("\n2. 检查个人记忆功能")
    settings = Settings()
    memory_adapter = MemoryAdapter("test_agent", storage_type="auto", settings=settings)
    
    # 添加测试记忆
    test_memory = {
        "topic": "中国精神",
        "content": "我认为中国精神体现在传统文化的传承中",
        "role": "craftsman"
    }
    
    try:
        await memory_adapter.add_memory("discussion", test_memory)
        print("✅ 记忆添加成功")
        
        # 检索相关记忆
        relevant_memories = await memory_adapter.get_relevant_memories("中国精神", limit=3)
        print(f"🔍 检索到相关记忆数量: {len(relevant_memories)}")
        
        if relevant_memories:
            print("📝 检索到的记忆内容:")
            for i, memory in enumerate(relevant_memories, 1):
                print(f"   {i}. {memory[:100]}...")
        else:
            print("⚠️  没有检索到相关记忆")
            
        # 获取所有记忆
        all_memories = await memory_adapter.get_all_memories()
        print(f"📚 总记忆数量: {len(all_memories)}")
        
    except Exception as e:
        print(f"❌ 个人记忆功能异常: {str(e)}")
    
    # 3. 检查全局记忆功能
    print("\n3. 检查全局记忆功能")
    global_memory = GlobalMemory("diagnosis_session", storage_type="auto")
    
    try:
        # 添加参与者
        await global_memory.add_participant("test_agent_1", "测试智能体1", "craftsman")
        await global_memory.add_participant("test_agent_2", "测试智能体2", "consumer")
        print("✅ 全局记忆参与者添加成功")
        
        # 记录发言
        speech_id = await global_memory.record_speech(
            agent_id="test_agent_1",
            agent_name="测试智能体1",
            speech_type="discussion",
            content="我是一名传统手工艺人，专注于剪纸艺术",
            stage="discussion",
            additional_data={"topic": "中国精神"}
        )
        print(f"✅ 发言记录成功: {speech_id}")
        
        # 获取会议上下文
        context = await global_memory.get_current_context("test_agent_2", max_context=5)
        print(f"🌐 全局上下文长度: {len(context)} 字符")
        if context and "暂无" not in context:
            print(f"📄 上下文内容预览: {context[:200]}...")
        else:
            print("⚠️  全局上下文为空或无效")
            
        # 获取会议统计
        stats = await global_memory.get_meeting_stats()
        print(f"📊 会议统计: {stats}")
        
    except Exception as e:
        print(f"❌ 全局记忆功能异常: {str(e)}")
    
    # 4. 检查记忆在对话中的使用情况
    print("\n4. 模拟记忆在对话中的使用")
    try:
        # 模拟智能体讨论时的记忆检索
        topic = "产品设计"
        
        # 获取个人相关记忆
        personal_memories = await memory_adapter.get_relevant_memories(topic, limit=3)
        
        # 获取全局上下文
        global_context = await global_memory.get_current_context("test_agent_1", max_context=5)
        
        # 构建模拟prompt
        prompt_parts = [f"讨论主题: {topic}"]
        
        if personal_memories:
            prompt_parts.append(f"\n个人相关记忆:\n" + "\n".join(personal_memories))
        
        if global_context and "暂无" not in global_context:
            prompt_parts.append(f"\n{global_context}")
        
        full_prompt = "\n".join(prompt_parts)
        print(f"🎯 构建的prompt长度: {len(full_prompt)} 字符")
        print(f"📝 prompt预览:\n{full_prompt[:300]}...")
        
        # 分析prompt中记忆内容的比例
        memory_content_length = len("\n".join(personal_memories)) if personal_memories else 0
        global_content_length = len(global_context) if global_context and "暂无" not in global_context else 0
        total_memory_length = memory_content_length + global_content_length
        
        if total_memory_length > 0:
            memory_ratio = total_memory_length / len(full_prompt) * 100
            print(f"📊 记忆内容占prompt比例: {memory_ratio:.1f}%")
        else:
            print("⚠️  prompt中没有记忆内容")
            
    except Exception as e:
        print(f"❌ 记忆使用模拟失败: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🏁 记忆系统诊断完成")
    
    return True


async def check_existing_memories():
    """检查现有的记忆数据"""
    print("\n🔍 检查现有记忆数据...")
    
    try:
        redis_client = await get_redis_client()
        
        # 查找所有agent的记忆
        agent_keys = []
        async for key in redis_client.scan_iter(match="agent:*:memories:list"):
            agent_keys.append(key.decode('utf-8'))
        
        print(f"📊 发现 {len(agent_keys)} 个智能体的记忆数据")
        
        for agent_key in agent_keys:
            agent_id = agent_key.split(':')[1]
            print(f"\n🤖 智能体: {agent_id}")
            
            # 获取记忆数量
            memory_count = await redis_client.zcard(agent_key)
            print(f"   📚 记忆数量: {memory_count}")
            
            if memory_count > 0:
                # 获取最近的几条记忆
                recent_memories = await redis_client.zrevrange(agent_key, 0, 2)
                print(f"   🕒 最近的记忆ID:")
                for memory_id in recent_memories:
                    memory_id_str = memory_id.decode('utf-8')
                    print(f"      - {memory_id_str}")
                    
                    # 获取记忆详情
                    memory_key = f"agent:{agent_id}:memory:{memory_id_str}"
                    memory_data = await redis_client.hgetall(memory_key)
                    if memory_data:
                        memory_type = memory_data.get(b'type', b'').decode('utf-8')
                        created_at = memory_data.get(b'created_at', b'').decode('utf-8')
                        print(f"        类型: {memory_type}, 时间: {created_at}")
        
        # 检查全局记忆
        print(f"\n🌐 检查全局记忆数据...")
        meeting_keys = []
        async for key in redis_client.scan_iter(match="meeting:*:timeline"):
            meeting_keys.append(key.decode('utf-8'))
        
        print(f"📊 发现 {len(meeting_keys)} 个会议的全局记忆")
        
        for meeting_key in meeting_keys:
            session_id = meeting_key.split(':')[1]
            print(f"\n🏢 会议: {session_id}")
            
            timeline_count = await redis_client.zcard(meeting_key)
            print(f"   📝 发言记录数量: {timeline_count}")
            
    except Exception as e:
        print(f"❌ 检查现有记忆失败: {str(e)}")


if __name__ == "__main__":
    async def main():
        await diagnose_memory_system()
        await check_existing_memories()
    
    asyncio.run(main())
