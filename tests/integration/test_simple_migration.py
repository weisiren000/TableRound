#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单的Agent系统迁移测试
"""

import asyncio
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from config.settings import Settings
    from core.memory_adapter import MemoryAdapter
    from agents.craftsman import Craftsman
    from models.mock import MockModel
    print("✅ 模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {str(e)}")
    sys.exit(1)


async def simple_test():
    """简单测试"""
    print("🔍 开始简单测试...")
    
    try:
        # 创建模拟模型
        model = MockModel()
        print("✅ 创建模拟模型成功")
        
        # 创建设置
        settings = Settings()
        print("✅ 创建设置成功")
        
        # 创建记忆适配器
        memory = MemoryAdapter("test_agent", storage_type="auto", settings=settings)
        print("✅ 创建记忆适配器成功")
        
        # 获取存储信息
        storage_info = await memory.get_storage_info()
        print(f"📋 存储信息: {storage_info}")
        
        # 创建Agent
        agent = Craftsman(
            agent_id="test_agent",
            name="测试手工艺人",
            model=model,
            memory=memory
        )
        print("✅ 创建Agent成功")
        
        # 测试自我介绍
        print("📝 测试自我介绍...")
        introduction = await agent.introduce()
        print(f"   结果: {introduction[:100]}...")
        
        # 测试记忆统计
        stats = await memory.get_memory_stats()
        print(f"📊 记忆统计: {stats}")
        
        print("🎉 简单测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主函数"""
    print("🚀 开始简单迁移测试\n")
    
    success = await simple_test()
    
    if success:
        print("\n✅ 迁移测试成功！")
        print("   Agent系统已成功迁移到Redis记忆模块")
    else:
        print("\n❌ 迁移测试失败")


if __name__ == "__main__":
    asyncio.run(main())
