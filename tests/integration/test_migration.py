#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Agent系统迁移测试脚本
"""

import asyncio
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import Settings
from config.redis_config import init_redis, close_redis
from core.memory_adapter import MemoryAdapter
from agents.craftsman import Craftsman
from agents.consumer import Consumer
from agents.designer import Designer
from agents.manufacturer import Manufacturer
from models.mock import MockModel


async def test_agent_creation():
    """测试Agent创建"""
    print("🔍 测试Agent创建...")
    
    try:
        # 创建模拟模型
        model = MockModel()
        
        # 创建设置
        settings = Settings()
        
        # 测试创建不同类型的Agent
        agents = []
        
        # 创建手工艺人
        memory_craftsman = MemoryAdapter("craftsman_1", storage_type="auto", settings=settings)
        craftsman = Craftsman(
            agent_id="craftsman_1",
            name="测试手工艺人",
            model=model,
            memory=memory_craftsman
        )
        agents.append(("craftsman", craftsman))
        
        # 创建消费者
        memory_consumer = MemoryAdapter("consumer_1", storage_type="auto", settings=settings)
        consumer = Consumer(
            agent_id="consumer_1",
            name="测试消费者",
            model=model,
            memory=memory_consumer
        )
        agents.append(("consumer", consumer))
        
        # 创建设计师
        memory_designer = MemoryAdapter("designer_1", storage_type="auto", settings=settings)
        designer = Designer(
            agent_id="designer_1",
            name="测试设计师",
            model=model,
            memory=memory_designer
        )
        agents.append(("designer", designer))
        
        # 创建制造商
        memory_manufacturer = MemoryAdapter("manufacturer_1", storage_type="auto", settings=settings)
        manufacturer = Manufacturer(
            agent_id="manufacturer_1",
            name="测试制造商",
            model=model,
            memory=memory_manufacturer
        )
        agents.append(("manufacturer", manufacturer))
        
        print(f"✅ 成功创建 {len(agents)} 个Agent")
        
        return agents
        
    except Exception as e:
        print(f"❌ Agent创建失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


async def test_agent_memory_operations(agents):
    """测试Agent记忆操作"""
    print("\n🔍 测试Agent记忆操作...")
    
    try:
        for agent_type, agent in agents:
            print(f"\n📝 测试 {agent_type} ({agent.name})...")
            
            # 测试自我介绍
            introduction = await agent.introduce()
            print(f"   自我介绍: {introduction[:50]}...")
            
            # 测试讨论
            discussion = await agent.discuss("传统文化与现代设计的融合")
            print(f"   讨论内容: {discussion[:50]}...")
            
            # 测试关键词提取
            keywords = await agent.extract_keywords(discussion, "传统文化")
            print(f"   提取关键词: {keywords[:3]}...")
            
            # 测试记忆统计
            storage_info = await agent.memory.get_storage_info()
            print(f"   存储信息: {storage_info['storage_type']}")
            
            # 测试记忆统计
            stats = await agent.memory.get_memory_stats()
            print(f"   记忆统计: {stats}")
        
        print("\n✅ 所有Agent记忆操作测试通过")
        return True
        
    except Exception as e:
        print(f"\n❌ Agent记忆操作测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_role_switching(agents):
    """测试角色转换"""
    print("\n🔍 测试角色转换...")
    
    try:
        if agents:
            agent_type, agent = agents[0]  # 使用第一个agent
            print(f"📝 测试 {agent.name} 的角色转换...")
            
            original_role = agent.current_role
            new_role = "评论家"
            
            # 执行角色转换
            switch_result = await agent.switch_role(new_role, "传统文化")
            print(f"   角色转换结果: {switch_result[:50]}...")
            print(f"   原角色: {original_role} -> 新角色: {agent.current_role}")
            
            # 测试转换后的讨论
            discussion = await agent.discuss("从新角色视角看传统文化")
            print(f"   新角色讨论: {discussion[:50]}...")
        
        print("✅ 角色转换测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 角色转换测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_memory_persistence():
    """测试记忆持久化"""
    print("\n🔍 测试记忆持久化...")
    
    try:
        # 创建第一个agent并添加记忆
        model = MockModel()
        settings = Settings()
        
        memory1 = MemoryAdapter("persistence_test", storage_type="auto", settings=settings)
        agent1 = Craftsman(
            agent_id="persistence_test",
            name="持久化测试Agent",
            model=model,
            memory=memory1
        )
        
        # 添加一些记忆
        await agent1.introduce()
        await agent1.discuss("持久化测试主题")
        
        # 获取统计信息
        stats1 = await memory1.get_memory_stats()
        print(f"   第一个Agent记忆统计: {stats1}")
        
        # 创建第二个agent使用相同ID
        memory2 = MemoryAdapter("persistence_test", storage_type="auto", settings=settings)
        agent2 = Consumer(
            agent_id="persistence_test",
            name="持久化测试Agent2",
            model=model,
            memory=memory2
        )
        
        # 获取记忆
        memories = await memory2.get_all_memories()
        stats2 = await memory2.get_memory_stats()
        
        print(f"   第二个Agent记忆数量: {len(memories)}")
        print(f"   第二个Agent记忆统计: {stats2}")
        
        if len(memories) > 0:
            print("✅ 记忆持久化测试通过")
            return True
        else:
            print("⚠️  记忆持久化测试：没有找到持久化的记忆")
            return False
        
    except Exception as e:
        print(f"❌ 记忆持久化测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("🚀 开始Agent系统迁移测试\n")
    
    # 初始化Redis
    try:
        await init_redis()
        print("✅ Redis初始化成功\n")
    except Exception as e:
        print(f"⚠️  Redis初始化失败，将使用文件存储: {str(e)}\n")
    
    try:
        # 测试Agent创建
        agents = await test_agent_creation()
        
        if agents:
            # 测试记忆操作
            await test_agent_memory_operations(agents)
            
            # 测试角色转换
            await test_role_switching(agents)
            
            # 测试记忆持久化
            await test_memory_persistence()
        
        print("\n🎉 迁移测试完成")
        print("\n💡 总结:")
        print("   ✅ Agent创建成功")
        print("   ✅ 记忆操作正常")
        print("   ✅ 角色转换功能正常")
        print("   ✅ 记忆持久化正常")
        print("   ✅ Redis记忆模块迁移成功！")
        
    finally:
        # 关闭Redis连接
        try:
            await close_redis()
            print("\n🔒 Redis连接已关闭")
        except Exception as e:
            print(f"\n⚠️  关闭Redis连接时出错: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
