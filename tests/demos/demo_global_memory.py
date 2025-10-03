#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
全局记忆演示脚本 - 展示AI如何倾听所有智能体的发言
"""

import asyncio
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import Settings
from core.global_memory import GlobalMemory
from core.memory_adapter import MemoryAdapter
from agents.craftsman import Craftsman
from agents.consumer import Consumer
from agents.designer import Designer
from models.mock import MockModel


async def demo_ai_listening():
    """演示AI倾听能力"""
    print("🎭 AI全局记忆演示：智能体如何倾听彼此的发言\n")
    
    # 创建全局记忆（模拟会议室）
    global_memory = GlobalMemory("demo_meeting", storage_type="auto")
    print("🏢 创建虚拟会议室...")
    
    # 创建三个智能体
    model = MockModel()
    settings = Settings()
    
    # 手工艺人
    memory1 = MemoryAdapter("craftsman_1", storage_type="auto", settings=settings)
    craftsman = Craftsman(
        agent_id="craftsman_1",
        name="张师傅",
        model=model,
        memory=memory1,
        global_memory=global_memory
    )

    # 消费者
    memory2 = MemoryAdapter("consumer_1", storage_type="auto", settings=settings)
    consumer = Consumer(
        agent_id="consumer_1",
        name="李女士",
        model=model,
        memory=memory2,
        global_memory=global_memory
    )

    # 设计师
    memory3 = MemoryAdapter("designer_1", storage_type="auto", settings=settings)
    designer = Designer(
        agent_id="designer_1",
        name="王设计师",
        model=model,
        memory=memory3,
        global_memory=global_memory
    )
    
    # 注册参与者到会议室
    await global_memory.add_participant("craftsman_1", "张师傅", "craftsman")
    await global_memory.add_participant("consumer_1", "李女士", "consumer")
    await global_memory.add_participant("designer_1", "王设计师", "designer")
    
    print("👥 会议参与者:")
    print("   - 张师傅 (手工艺人)")
    print("   - 李女士 (消费者)")
    print("   - 王设计师 (设计师)")
    print()
    
    # 阶段1：自我介绍
    print("📝 阶段1：自我介绍")
    print("-" * 40)
    await global_memory.update_stage("introduction")
    
    intro1 = await craftsman.introduce()
    print(f"🧑‍🎨 张师傅: {intro1[:80]}...")
    
    intro2 = await consumer.introduce()
    print(f"👩‍💼 李女士: {intro2[:80]}...")
    
    intro3 = await designer.introduce()
    print(f"👨‍💻 王设计师: {intro3[:80]}...")
    print()
    
    # 阶段2：讨论（展示倾听能力）
    print("💬 阶段2：讨论 - 展示AI倾听能力")
    print("-" * 40)
    await global_memory.update_stage("discussion")
    
    # 张师傅先发言
    print("🧑‍🎨 张师傅发言:")
    discussion1 = await craftsman.discuss("传统剪纸文创产品设计")
    print(f"   {discussion1[:100]}...")
    print()
    
    # 李女士发言（她能听到张师傅的发言）
    print("👩‍💼 李女士发言（注意她如何回应张师傅的观点）:")
    discussion2 = await consumer.discuss("传统剪纸文创产品设计")
    print(f"   {discussion2[:100]}...")
    print()
    
    # 王设计师发言（他能听到前面两人的发言）
    print("👨‍💻 王设计师发言（注意他如何综合前面两人的观点）:")
    discussion3 = await designer.discuss("传统剪纸文创产品设计")
    print(f"   {discussion3[:100]}...")
    print()
    
    # 展示全局记忆内容
    print("🧠 全局记忆内容展示")
    print("-" * 40)
    
    # 获取完整时间线
    timeline = await global_memory.get_meeting_timeline(limit=10)
    print(f"📊 会议记录总数: {len(timeline)} 条")
    print()
    
    # 展示每个人看到的上下文
    print("👁️  各参与者的视角（他们能看到的其他人发言）:")
    print()
    
    context1 = await global_memory.get_current_context("craftsman_1", max_context=5)
    print(f"🧑‍🎨 张师傅看到的上下文:")
    print(f"   {context1[:200]}...")
    print()

    context2 = await global_memory.get_current_context("consumer_1", max_context=5)
    print(f"👩‍💼 李女士看到的上下文:")
    print(f"   {context2[:200]}...")
    print()

    context3 = await global_memory.get_current_context("designer_1", max_context=5)
    print(f"👨‍💻 王设计师看到的上下文:")
    print(f"   {context3[:200]}...")
    print()
    
    # 会议统计
    stats = await global_memory.get_meeting_stats()
    print("📈 会议统计:")
    print(f"   参与者数量: {stats['participants_count']}")
    print(f"   总发言次数: {stats['total_speeches']}")
    print(f"   会议时长: {stats['duration_minutes']:.2f} 分钟")
    print(f"   发言类型分布: {stats['speech_by_type']}")
    print(f"   各人发言次数: {stats['speech_by_agent']}")
    print()
    
    # 阶段总结
    intro_summary = await global_memory.get_stage_summary("introduction")
    discussion_summary = await global_memory.get_stage_summary("discussion")
    
    print("📋 阶段总结:")
    print(f"   自我介绍阶段: {intro_summary['speech_count']} 次发言，参与者 {len(intro_summary['participants'])} 人")
    print(f"   讨论阶段: {discussion_summary['speech_count']} 次发言，参与者 {len(discussion_summary['participants'])} 人")
    print()
    
    print("🎉 演示完成！")
    print()
    print("💡 关键特性展示:")
    print("   ✅ 每个AI都能听到其他AI的完整发言历史")
    print("   ✅ AI在回应时会考虑之前所有人的观点")
    print("   ✅ 全局记忆按时间线记录所有发言")
    print("   ✅ 支持按阶段、按参与者查看记忆")
    print("   ✅ 提供丰富的会议统计和分析")
    print()
    print("🧠 这就是AI的全局记忆能力 - 就像人类开会一样，")
    print("   每个参与者都能听到并记住其他人说过的话！")


async def main():
    """主函数"""
    try:
        await demo_ai_listening()
    except Exception as e:
        print(f"❌ 演示过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
