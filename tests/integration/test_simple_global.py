#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单的全局记忆测试
"""

import asyncio
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from core.global_memory import GlobalMemory
    print("✅ GlobalMemory导入成功")
except ImportError as e:
    print(f"❌ GlobalMemory导入失败: {str(e)}")
    sys.exit(1)


async def simple_test():
    """简单测试"""
    print("🔍 开始简单全局记忆测试...")
    
    try:
        # 创建全局记忆实例
        global_memory = GlobalMemory("test_session", storage_type="auto")
        print("✅ 创建全局记忆成功")
        
        # 添加参与者
        await global_memory.add_participant("agent_1", "张师傅", "craftsman")
        print("✅ 添加参与者成功")
        
        # 记录发言
        speech_id = await global_memory.record_speech(
            agent_id="agent_1",
            agent_name="张师傅",
            speech_type="introduction",
            content="我是一名传统手工艺人",
            stage="introduction"
        )
        print(f"✅ 记录发言成功: {speech_id}")
        
        # 获取时间线
        timeline = await global_memory.get_meeting_timeline(limit=5)
        print(f"✅ 获取时间线成功: {len(timeline)} 条记录")
        
        # 获取上下文
        context = await global_memory.get_current_context("agent_1")
        print(f"✅ 获取上下文成功: {len(context)} 字符")
        
        # 获取统计
        stats = await global_memory.get_meeting_stats()
        print(f"✅ 获取统计成功: {stats}")
        
        print("🎉 简单全局记忆测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主函数"""
    print("🚀 开始简单全局记忆测试\n")
    
    success = await simple_test()
    
    if success:
        print("\n✅ 全局记忆测试成功！")
        print("   AI现在拥有了全局记忆能力")
    else:
        print("\n❌ 全局记忆测试失败")


if __name__ == "__main__":
    asyncio.run(main())
