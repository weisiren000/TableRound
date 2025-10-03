#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Redis记忆模块测试脚本
"""

import asyncio
import time
import json
from src.config.redis_config import RedisManager, RedisSettings
from src.core.redis_memory import RedisMemory
from src.core.memory_adapter import MemoryAdapter


async def test_redis_connection():
    """测试Redis连接"""
    print("🔍 测试Redis连接...")
    
    redis_manager = RedisManager()
    
    try:
        client = await redis_manager.get_client()
        info = await redis_manager.get_info()
        
        print(f"✅ Redis连接成功")
        print(f"   版本: {info.get('redis_version', 'unknown')}")
        print(f"   内存使用: {info.get('used_memory_human', 'unknown')}")
        print(f"   连接数: {info.get('connected_clients', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Redis连接失败: {str(e)}")
        return False
    
    finally:
        await redis_manager.close()


async def test_redis_memory_basic():
    """测试Redis记忆模块基本功能"""
    print("\n🔍 测试Redis记忆模块基本功能...")
    
    redis_manager = RedisManager()
    
    try:
        client = await redis_manager.get_client()
        memory = RedisMemory("test_agent", client)
        
        # 清空测试数据
        await memory.clear_memories()
        
        # 测试添加记忆
        print("📝 添加记忆...")
        memory_id1 = await memory.add_memory(
            "introduction",
            {"role": "craftsman", "content": "我是一名手工艺人，专注于传统剪纸艺术"}
        )
        
        memory_id2 = await memory.add_memory(
            "discussion",
            {"role": "craftsman", "topic": "传统工艺", "content": "传统工艺在现代社会仍然有重要价值"}
        )
        
        memory_id3 = await memory.add_memory(
            "keywords",
            {"role": "craftsman", "topic": "传统工艺", "keywords": ["传承", "创新", "价值"]}
        )
        
        print(f"   记忆ID1: {memory_id1}")
        print(f"   记忆ID2: {memory_id2}")
        print(f"   记忆ID3: {memory_id3}")
        
        # 测试获取记忆
        print("\n📖 获取相关记忆...")
        relevant_memories = await memory.get_relevant_memories("传统工艺", limit=3)
        for i, mem in enumerate(relevant_memories, 1):
            print(f"   记忆{i}: {mem[:100]}...")
        
        # 测试按类型获取记忆
        print("\n📋 按类型获取记忆...")
        discussion_memories = await memory.get_memories_by_type("discussion")
        print(f"   讨论记忆数量: {len(discussion_memories)}")
        
        # 测试统计信息
        print("\n📊 获取统计信息...")
        stats = await memory.get_memory_stats()
        print(f"   统计信息: {json.dumps(stats, ensure_ascii=False, indent=2)}")
        
        print("✅ Redis记忆模块基本功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ Redis记忆模块测试失败: {str(e)}")
        return False
    
    finally:
        await redis_manager.close()


async def test_memory_adapter():
    """测试记忆适配器"""
    print("\n🔍 测试记忆适配器...")
    
    try:
        # 测试自动模式（优先使用Redis）
        adapter = MemoryAdapter("test_adapter_agent", storage_type="auto")
        
        # 获取存储信息
        storage_info = await adapter.get_storage_info()
        print(f"📋 存储信息: {json.dumps(storage_info, ensure_ascii=False, indent=2)}")
        
        # 添加记忆
        await adapter.add_memory(
            "introduction",
            {"role": "designer", "content": "我是一名设计师，专注于文创产品设计"}
        )
        
        await adapter.add_memory(
            "discussion",
            {"role": "designer", "topic": "现代设计", "content": "现代设计需要融合传统元素"}
        )
        
        # 获取记忆
        memories = await adapter.get_relevant_memories("设计", limit=2)
        print(f"\n📖 获取到 {len(memories)} 条记忆:")
        for i, mem in enumerate(memories, 1):
            print(f"   记忆{i}: {mem[:100]}...")
        
        # 获取统计信息
        stats = await adapter.get_memory_stats()
        print(f"\n📊 统计信息: {json.dumps(stats, ensure_ascii=False, indent=2)}")
        
        print("✅ 记忆适配器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 记忆适配器测试失败: {str(e)}")
        return False


async def test_performance_comparison():
    """测试性能对比"""
    print("\n🔍 测试性能对比...")
    
    # 测试数据
    test_memories = []
    for i in range(100):
        test_memories.extend([
            ("introduction", {"role": f"agent_{i}", "content": f"我是智能体{i}"}),
            ("discussion", {"role": f"agent_{i}", "topic": "测试主题", "content": f"这是第{i}条讨论内容"}),
            ("keywords", {"role": f"agent_{i}", "topic": "测试主题", "keywords": [f"关键词{i}", f"词汇{i}"]})
        ])
    
    redis_manager = RedisManager()
    
    try:
        # 测试Redis性能
        print("⏱️  测试Redis写入性能...")
        client = await redis_manager.get_client()
        redis_memory = RedisMemory("perf_test_redis", client)
        await redis_memory.clear_memories()
        
        start_time = time.time()
        for memory_type, content in test_memories:
            await redis_memory.add_memory(memory_type, content)
        redis_write_time = time.time() - start_time
        
        print("⏱️  测试Redis读取性能...")
        start_time = time.time()
        for _ in range(10):
            await redis_memory.get_relevant_memories("测试", limit=10)
        redis_read_time = time.time() - start_time
        
        # 测试文件存储性能
        print("⏱️  测试文件存储写入性能...")
        from src.core.memory import Memory
        file_memory = MemoryAdapter("perf_test_file", storage_type="redis")
        file_memory.clear_memories()
        
        start_time = time.time()
        for memory_type, content in test_memories:
            file_memory.add_memory(memory_type, content)
        file_write_time = time.time() - start_time
        
        print("⏱️  测试文件存储读取性能...")
        start_time = time.time()
        for _ in range(10):
            file_memory.get_relevant_memories("测试", limit=10)
        file_read_time = time.time() - start_time
        
        # 输出结果
        print(f"\n📊 性能对比结果:")
        print(f"   Redis写入时间: {redis_write_time:.3f}秒 ({len(test_memories)}条记忆)")
        print(f"   文件写入时间: {file_write_time:.3f}秒 ({len(test_memories)}条记忆)")
        print(f"   Redis读取时间: {redis_read_time:.3f}秒 (10次查询)")
        print(f"   文件读取时间: {file_read_time:.3f}秒 (10次查询)")
        
        print(f"\n🚀 性能提升:")
        write_speedup = file_write_time / redis_write_time if redis_write_time > 0 else 0
        read_speedup = file_read_time / redis_read_time if redis_read_time > 0 else 0
        print(f"   写入速度提升: {write_speedup:.2f}x")
        print(f"   读取速度提升: {read_speedup:.2f}x")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能测试失败: {str(e)}")
        return False
    
    finally:
        await redis_manager.close()


async def main():
    """主测试函数"""
    print("🚀 开始Redis记忆模块测试\n")
    
    # 测试Redis连接
    redis_ok = await test_redis_connection()
    
    if redis_ok:
        # 测试Redis记忆模块
        await test_redis_memory_basic()
        
        # 测试记忆适配器
        await test_memory_adapter()
        
        # 测试性能对比
        await test_performance_comparison()
    else:
        print("\n⚠️  Redis不可用，跳过相关测试")
    
    print("\n🎉 测试完成")


if __name__ == "__main__":
    asyncio.run(main())
