#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
快速迁移验证测试
"""

import asyncio
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

async def test_imports():
    """测试导入"""
    print("🔍 测试模块导入...")
    
    try:
        from config.settings import Settings
        print("✅ Settings导入成功")
        
        from config.redis_config import RedisManager
        print("✅ RedisManager导入成功")
        
        from core.memory_adapter import MemoryAdapter
        print("✅ MemoryAdapter导入成功")
        
        from core.agent import Agent
        print("✅ Agent导入成功")
        
        from agents.craftsman import Craftsman
        print("✅ Craftsman导入成功")
        
        return True
    except Exception as e:
        print(f"❌ 导入失败: {str(e)}")
        return False


async def test_redis_connection():
    """测试Redis连接"""
    print("\n🔍 测试Redis连接...")
    
    try:
        from config.redis_config import RedisManager
        
        redis_manager = RedisManager()
        client = await redis_manager.get_client()
        
        # 测试ping
        result = await client.ping()
        print(f"✅ Redis连接成功: {result}")
        
        await redis_manager.close()
        return True
        
    except Exception as e:
        print(f"⚠️  Redis连接失败: {str(e)}")
        return False


async def test_memory_adapter():
    """测试记忆适配器"""
    print("\n🔍 测试记忆适配器...")
    
    try:
        from config.settings import Settings
        from core.memory_adapter import MemoryAdapter
        
        settings = Settings()
        memory = MemoryAdapter("test_quick", storage_type="auto", settings=settings)
        
        # 获取存储信息
        storage_info = await memory.get_storage_info()
        print(f"📋 存储类型: {storage_info['storage_type']}")
        
        # 添加测试记忆
        await memory.add_memory("test", {"content": "测试记忆"})
        
        # 获取记忆
        memories = await memory.get_relevant_memories("测试", limit=1)
        print(f"📝 记忆数量: {len(memories)}")
        
        # 获取统计
        stats = await memory.get_memory_stats()
        print(f"📊 统计信息: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ 记忆适配器测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主函数"""
    print("🚀 快速迁移验证测试\n")
    
    # 测试导入
    import_ok = await test_imports()
    
    if not import_ok:
        print("❌ 导入测试失败，停止测试")
        return
    
    # 测试Redis连接
    redis_ok = await test_redis_connection()
    
    # 测试记忆适配器
    memory_ok = await test_memory_adapter()
    
    print(f"\n🎉 快速验证完成")
    print(f"   导入测试: {'✅' if import_ok else '❌'}")
    print(f"   Redis连接: {'✅' if redis_ok else '⚠️'}")
    print(f"   记忆适配器: {'✅' if memory_ok else '❌'}")
    
    if import_ok and memory_ok:
        print("\n🎊 迁移验证成功！")
        print("   Agent系统已成功迁移到Redis记忆模块")
        if redis_ok:
            print("   Redis记忆存储正常工作")
        else:
            print("   自动降级到文件存储")
    else:
        print("\n❌ 迁移验证失败")


if __name__ == "__main__":
    asyncio.run(main())
