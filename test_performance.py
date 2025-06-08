#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Redis vs 文件存储性能对比测试
"""

import asyncio
import time
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.redis_config import RedisManager
from core.redis_memory import RedisMemory
from core.memory import Memory


async def test_performance():
    """性能对比测试"""
    print("🚀 开始性能对比测试\n")
    
    # 测试数据
    test_count = 50  # 减少测试数量以便快速验证
    test_memories = []
    for i in range(test_count):
        test_memories.extend([
            ("introduction", {"role": f"agent_{i}", "content": f"我是智能体{i}，专注于传统工艺"}),
            ("discussion", {"role": f"agent_{i}", "topic": "测试主题", "content": f"这是第{i}条讨论内容，包含了很多详细的信息"}),
            ("keywords", {"role": f"agent_{i}", "topic": "测试主题", "keywords": [f"关键词{i}", f"词汇{i}", "传统", "工艺"]})
        ])
    
    print(f"📊 测试数据量: {len(test_memories)} 条记忆")
    
    # 测试Redis性能
    print("\n⏱️  测试Redis性能...")
    redis_manager = RedisManager()
    
    try:
        client = await redis_manager.get_client()
        redis_memory = RedisMemory("perf_test_redis", client)
        await redis_memory.clear_memories()
        
        # Redis写入测试
        start_time = time.time()
        for memory_type, content in test_memories:
            await redis_memory.add_memory(memory_type, content)
        redis_write_time = time.time() - start_time
        
        # Redis读取测试
        start_time = time.time()
        for _ in range(10):
            await redis_memory.get_relevant_memories("测试", limit=5)
        redis_read_time = time.time() - start_time
        
        # 获取统计信息
        stats = await redis_memory.get_memory_stats()
        
        print(f"   ✅ Redis写入: {redis_write_time:.3f}秒 ({len(test_memories)}条)")
        print(f"   ✅ Redis读取: {redis_read_time:.3f}秒 (10次查询)")
        print(f"   📊 Redis统计: {stats}")
        
    except Exception as e:
        print(f"   ❌ Redis测试失败: {str(e)}")
        return
    finally:
        await redis_manager.close()
    
    # 测试文件存储性能
    print("\n⏱️  测试文件存储性能...")
    
    try:
        # 需要提供settings参数来启用文件存储
        from config.settings import Settings
        settings = Settings()
        file_memory = Memory("perf_test_file", storage_type="file", settings=settings)
        file_memory.clear_memories()
        
        # 文件写入测试
        start_time = time.time()
        for memory_type, content in test_memories:
            file_memory.add_memory(memory_type, content)
        file_write_time = time.time() - start_time
        
        # 文件读取测试
        start_time = time.time()
        for _ in range(10):
            file_memory.get_relevant_memories("测试", limit=5)
        file_read_time = time.time() - start_time
        
        print(f"   ✅ 文件写入: {file_write_time:.3f}秒 ({len(test_memories)}条)")
        print(f"   ✅ 文件读取: {file_read_time:.3f}秒 (10次查询)")
        
    except Exception as e:
        print(f"   ❌ 文件测试失败: {str(e)}")
        return
    
    # 性能对比
    print(f"\n🚀 性能对比结果:")
    print(f"   📈 写入性能:")
    if redis_write_time > 0:
        write_speedup = file_write_time / redis_write_time
        print(f"      Redis: {redis_write_time:.3f}秒")
        print(f"      文件:  {file_write_time:.3f}秒")
        print(f"      提升:  {write_speedup:.2f}x")
    
    print(f"   📈 读取性能:")
    if redis_read_time > 0:
        read_speedup = file_read_time / redis_read_time
        print(f"      Redis: {redis_read_time:.3f}秒")
        print(f"      文件:  {file_read_time:.3f}秒")
        print(f"      提升:  {read_speedup:.2f}x")
    
    print(f"\n💡 结论:")
    if redis_write_time > 0 and redis_read_time > 0:
        avg_speedup = (write_speedup + read_speedup) / 2
        print(f"   Redis平均性能提升: {avg_speedup:.2f}x")
        if avg_speedup > 2:
            print("   🎉 Redis显著提升了系统性能！")
        elif avg_speedup > 1.5:
            print("   ✅ Redis明显改善了系统性能")
        else:
            print("   📊 Redis提供了稳定的性能")


if __name__ == "__main__":
    asyncio.run(test_performance())
