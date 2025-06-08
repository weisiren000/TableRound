#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Redis记忆模块简单测试脚本
"""

import asyncio
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from config.redis_config import RedisManager, RedisSettings
    from core.redis_memory import RedisMemory
    from core.memory_adapter import MemoryAdapter
    print("✅ 模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {str(e)}")
    sys.exit(1)


async def test_redis_connection():
    """测试Redis连接"""
    print("\n🔍 测试Redis连接...")
    
    redis_manager = RedisManager()
    
    try:
        client = await redis_manager.get_client()
        
        # 测试ping
        result = await client.ping()
        print(f"✅ Redis连接成功，ping结果: {result}")
        
        # 测试基本操作
        await client.set("test_key", "test_value")
        value = await client.get("test_key")
        print(f"✅ 基本读写测试成功: {value.decode() if value else None}")
        
        # 清理测试数据
        await client.delete("test_key")
        
        return True
        
    except Exception as e:
        print(f"❌ Redis连接失败: {str(e)}")
        return False
    
    finally:
        await redis_manager.close()


async def test_redis_memory_basic():
    """测试Redis记忆模块基本功能"""
    print("\n🔍 测试Redis记忆模块...")
    
    redis_manager = RedisManager()
    
    try:
        client = await redis_manager.get_client()
        memory = RedisMemory("test_agent", client)
        
        # 清空测试数据
        await memory.clear_memories()
        print("🧹 清空测试数据")
        
        # 测试添加记忆
        print("📝 添加记忆...")
        memory_id1 = await memory.add_memory(
            "introduction",
            {"role": "craftsman", "content": "我是一名手工艺人"}
        )
        print(f"   记忆ID1: {memory_id1}")
        
        memory_id2 = await memory.add_memory(
            "discussion",
            {"role": "craftsman", "topic": "传统工艺", "content": "传统工艺很重要"}
        )
        print(f"   记忆ID2: {memory_id2}")
        
        # 测试获取记忆
        print("\n📖 获取记忆...")
        memories = await memory.get_relevant_memories("传统工艺", limit=2)
        print(f"   获取到 {len(memories)} 条记忆")
        for i, mem in enumerate(memories, 1):
            print(f"   记忆{i}: {mem[:80]}...")
        
        # 测试统计信息
        print("\n📊 获取统计信息...")
        stats = await memory.get_memory_stats()
        print(f"   统计信息: {stats}")
        
        print("✅ Redis记忆模块测试成功")
        return True
        
    except Exception as e:
        print(f"❌ Redis记忆模块测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        await redis_manager.close()


async def test_memory_adapter():
    """测试记忆适配器"""
    print("\n🔍 测试记忆适配器...")
    
    try:
        # 测试自动模式
        adapter = MemoryAdapter("test_adapter_agent", storage_type="auto")
        
        # 获取存储信息
        storage_info = await adapter.get_storage_info()
        print(f"📋 存储信息: {storage_info}")
        
        # 添加记忆
        await adapter.add_memory(
            "introduction",
            {"role": "designer", "content": "我是一名设计师"}
        )
        print("📝 添加记忆成功")
        
        # 获取记忆
        memories = await adapter.get_relevant_memories("设计", limit=1)
        print(f"📖 获取到 {len(memories)} 条记忆")
        if memories:
            print(f"   记忆内容: {memories[0][:80]}...")
        
        print("✅ 记忆适配器测试成功")
        return True
        
    except Exception as e:
        print(f"❌ 记忆适配器测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("🚀 开始Redis记忆模块简单测试\n")
    
    # 测试Redis连接
    redis_ok = await test_redis_connection()
    
    if redis_ok:
        # 测试Redis记忆模块
        await test_redis_memory_basic()
        
        # 测试记忆适配器
        await test_memory_adapter()
    else:
        print("\n⚠️  Redis不可用，跳过相关测试")
    
    print("\n🎉 测试完成")


if __name__ == "__main__":
    asyncio.run(main())
