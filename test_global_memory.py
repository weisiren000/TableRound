#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
全局记忆功能测试脚本
"""

import asyncio
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.settings import Settings
from config.redis_config import init_redis, close_redis
from core.global_memory import GlobalMemory
from core.memory_adapter import MemoryAdapter
from agents.craftsman import Craftsman
from agents.consumer import Consumer
from models.mock import MockModel


async def test_global_memory_basic():
    """测试全局记忆基本功能"""
    print("🔍 测试全局记忆基本功能...")
    
    try:
        # 创建全局记忆实例
        global_memory = GlobalMemory("test_session_001", storage_type="auto")
        
        # 添加参与者
        await global_memory.add_participant("agent_1", "张师傅", "craftsman")
        await global_memory.add_participant("agent_2", "李女士", "consumer")
        
        # 记录发言
        speech_id1 = await global_memory.record_speech(
            agent_id="agent_1",
            agent_name="张师傅",
            speech_type="introduction",
            content="我是一名传统手工艺人，专注于剪纸艺术30年",
            stage="introduction",
            additional_data={"role": "craftsman"}
        )
        
        speech_id2 = await global_memory.record_speech(
            agent_id="agent_2",
            agent_name="李女士",
            speech_type="introduction",
            content="我是一名消费者，喜欢传统文化产品",
            stage="introduction",
            additional_data={"role": "consumer"}
        )
        
        print(f"   记录发言ID: {speech_id1}, {speech_id2}")
        
        # 获取会议时间线
        timeline = await global_memory.get_meeting_timeline(limit=10)
        print(f"   会议时间线记录数: {len(timeline)}")
        
        # 获取上下文（从张师傅的角度）
        context = await global_memory.get_current_context("agent_1", max_context=5)
        print(f"   张师傅看到的上下文: {context[:100]}...")
        
        # 获取统计信息
        stats = await global_memory.get_meeting_stats()
        print(f"   会议统计: 参与者{stats['participants_count']}人，发言{stats['total_speeches']}次")
        
        print("✅ 全局记忆基本功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 全局记忆基本功能测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_agent_with_global_memory():
    """测试Agent与全局记忆的集成"""
    print("\n🔍 测试Agent与全局记忆的集成...")
    
    try:
        # 创建全局记忆
        global_memory = GlobalMemory("test_session_002", storage_type="auto")
        
        # 创建模拟模型和设置
        model = MockModel()
        settings = Settings()
        
        # 创建两个Agent
        memory1 = MemoryAdapter("craftsman_1", storage_type="auto", settings=settings)
        craftsman = Craftsman(
            agent_id="craftsman_1",
            name="王师傅",
            model=model,
            memory=memory1,
            global_memory=global_memory
        )
        
        memory2 = MemoryAdapter("consumer_1", storage_type="auto", settings=settings)
        consumer = Consumer(
            agent_id="consumer_1",
            name="赵女士",
            model=model,
            memory=memory2,
            global_memory=global_memory
        )
        
        # 注册参与者
        await global_memory.add_participant("craftsman_1", "王师傅", "craftsman")
        await global_memory.add_participant("consumer_1", "赵女士", "consumer")
        
        # 更新会议阶段
        await global_memory.update_stage("introduction")
        
        # Agent自我介绍
        print("   📝 Agent自我介绍...")
        intro1 = await craftsman.introduce()
        print(f"      王师傅: {intro1[:50]}...")
        
        intro2 = await consumer.introduce()
        print(f"      赵女士: {intro2[:50]}...")
        
        # 更新会议阶段
        await global_memory.update_stage("discussion")
        
        # Agent讨论（此时应该能看到对方的自我介绍）
        print("   💬 Agent讨论...")
        discussion1 = await craftsman.discuss("传统文化与现代设计")
        print(f"      王师傅讨论: {discussion1[:50]}...")
        
        discussion2 = await consumer.discuss("传统文化与现代设计")
        print(f"      赵女士讨论: {discussion2[:50]}...")
        
        # 检查全局记忆中的记录
        timeline = await global_memory.get_meeting_timeline(limit=10)
        print(f"   📊 全局记忆记录数: {len(timeline)}")
        
        # 检查上下文获取
        context_for_craftsman = await global_memory.get_current_context("craftsman_1")
        context_for_consumer = await global_memory.get_current_context("consumer_1")
        
        print(f"   🔍 王师傅看到的上下文长度: {len(context_for_craftsman)}")
        print(f"   🔍 赵女士看到的上下文长度: {len(context_for_consumer)}")
        
        # 验证上下文中包含对方的发言
        if "赵女士" in context_for_craftsman:
            print("   ✅ 王师傅能看到赵女士的发言")
        else:
            print("   ⚠️  王师傅看不到赵女士的发言")
        
        if "王师傅" in context_for_consumer:
            print("   ✅ 赵女士能看到王师傅的发言")
        else:
            print("   ⚠️  赵女士看不到王师傅的发言")
        
        print("✅ Agent与全局记忆集成测试通过")
        return True
        
    except Exception as e:
        print(f"❌ Agent与全局记忆集成测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_conversation_flow():
    """测试完整的对话流程"""
    print("\n🔍 测试完整的对话流程...")
    
    try:
        # 创建全局记忆
        global_memory = GlobalMemory("test_session_003", storage_type="auto")
        
        # 创建多个Agent
        model = MockModel()
        settings = Settings()
        
        agents = []
        for i, (agent_type, agent_class, name) in enumerate([
            ("craftsman", Craftsman, "张师傅"),
            ("consumer", Consumer, "李女士"),
            ("craftsman", Craftsman, "王师傅")
        ]):
            memory = MemoryAdapter(f"{agent_type}_{i}", storage_type="auto", settings=settings)
            agent = agent_class(
                agent_id=f"{agent_type}_{i}",
                name=name,
                model=model,
                memory=memory,
                global_memory=global_memory
            )
            agents.append(agent)
            
            # 注册参与者
            await global_memory.add_participant(f"{agent_type}_{i}", name, agent_type)
        
        # 模拟完整对话流程
        print("   📝 阶段1: 自我介绍")
        await global_memory.update_stage("introduction")
        
        for agent in agents:
            intro = await agent.introduce()
            print(f"      {agent.name}: {intro[:30]}...")
        
        print("   💬 阶段2: 讨论")
        await global_memory.update_stage("discussion")
        
        for agent in agents:
            discussion = await agent.discuss("传统剪纸文创产品设计")
            print(f"      {agent.name}: {discussion[:30]}...")
        
        print("   🔑 阶段3: 关键词提取")
        await global_memory.update_stage("keywords")
        
        for agent in agents:
            keywords = await agent.extract_keywords("传统剪纸文创产品设计", "传统文化")
            print(f"      {agent.name}关键词: {keywords[:3]}...")
        
        # 获取最终统计
        stats = await global_memory.get_meeting_stats()
        print(f"   📊 最终统计:")
        print(f"      参与者: {stats['participants_count']}人")
        print(f"      总发言: {stats['total_speeches']}次")
        print(f"      会议时长: {stats['duration_minutes']:.1f}分钟")
        print(f"      发言类型: {stats['speech_by_type']}")
        
        # 获取阶段总结
        intro_summary = await global_memory.get_stage_summary("introduction")
        discussion_summary = await global_memory.get_stage_summary("discussion")
        
        print(f"   📋 自我介绍阶段: {intro_summary['speech_count']}次发言")
        print(f"   📋 讨论阶段: {discussion_summary['speech_count']}次发言")
        
        print("✅ 完整对话流程测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 完整对话流程测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("🚀 开始全局记忆功能测试\n")
    
    # 初始化Redis
    try:
        await init_redis()
        print("✅ Redis初始化成功\n")
    except Exception as e:
        print(f"⚠️  Redis初始化失败，将使用文件存储: {str(e)}\n")
    
    try:
        # 运行测试
        test1 = await test_global_memory_basic()
        test2 = await test_agent_with_global_memory()
        test3 = await test_conversation_flow()
        
        print(f"\n🎉 全局记忆功能测试完成")
        print(f"   基本功能测试: {'✅' if test1 else '❌'}")
        print(f"   Agent集成测试: {'✅' if test2 else '❌'}")
        print(f"   完整流程测试: {'✅' if test3 else '❌'}")
        
        if test1 and test2 and test3:
            print("\n🎊 全局记忆功能测试全部通过！")
            print("   AI现在拥有了全局记忆能力，可以倾听所有智能体的发言")
        else:
            print("\n❌ 部分测试失败，需要检查问题")
        
    finally:
        # 关闭Redis连接
        try:
            await close_redis()
            print("\n🔒 Redis连接已关闭")
        except Exception as e:
            print(f"\n⚠️  关闭Redis连接时出错: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
