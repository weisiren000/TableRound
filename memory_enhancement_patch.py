#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
记忆功能增强补丁
改进现有的记忆功能，让记忆效果在对话中更明显
"""

import asyncio
from src.core.memory_adapter import MemoryAdapter
from src.core.global_memory import GlobalMemory
from src.config.settings import Settings


class EnhancedMemoryPromptBuilder:
    """增强的记忆prompt构建器"""
    
    @staticmethod
    def build_enhanced_discussion_prompt(
        agent_name: str,
        agent_role: str,
        agent_background: str,
        topic: str,
        personal_memories: list,
        global_context: str,
        base_prompt: str
    ) -> str:
        """
        构建增强的讨论prompt
        
        Args:
            agent_name: 智能体名称
            agent_role: 智能体角色
            agent_background: 智能体背景
            topic: 讨论主题
            personal_memories: 个人记忆列表
            global_context: 全局上下文
            base_prompt: 基础prompt
            
        Returns:
            增强的prompt
        """
        
        # 构建记忆部分
        memory_section = ""
        if personal_memories:
            memory_section = f"""
你的个人记忆和经验：
{chr(10).join(personal_memories)}

请基于这些记忆和经验来回答，体现出你的个人特色和专业背景。"""
        
        # 构建全局上下文部分
        context_section = ""
        if global_context and "暂无" not in global_context:
            context_section = f"""
会议中其他人的发言：
{global_context}

请对其他人的发言进行回应，展现你的观点和态度。"""
        
        # 构建增强prompt
        enhanced_prompt = f"""你是{agent_name}，{agent_background}

当前讨论主题：{topic}

{memory_section}

{context_section}

{base_prompt}

重要提示：
1. 请以第一人称回答，体现你的个人经历和专业背景
2. 如果有其他人的发言，请进行回应和互动
3. 展现你的情感、态度和个人观点
4. 使用你熟悉的专业术语和表达方式
5. 字数控制在150-300字之间"""
        
        return enhanced_prompt


async def apply_memory_enhancement():
    """应用记忆增强功能"""
    print("🔧 应用记忆功能增强...")
    print("=" * 60)
    
    # 1. 为现有智能体添加丰富的背景记忆
    print("\n1. 为现有智能体添加背景记忆...")
    
    settings = Settings()
    
    # 智能体背景数据
    agent_backgrounds = {
        "craftsman_1": {
            "name": "张师傅",
            "background": "65岁的蒙古族剪纸艺术传承人，从事剪纸艺术45年",
            "memories": [
                {
                    "type": "background",
                    "content": {
                        "specialty": "传统蝙蝠吉祥纹样设计",
                        "philosophy": "传统与现代相结合，让古老艺术焕发新生",
                        "memorable_quote": "每一刀都承载着文化的传承",
                        "favorite_materials": ["红纸", "金箔", "宣纸"],
                        "concerns": "如何让传统艺术被现代人接受"
                    }
                }
            ]
        },
        "consumer_1": {
            "name": "李女士",
            "background": "23岁的大学生，热爱文化创意产品",
            "memories": [
                {
                    "type": "background", 
                    "content": {
                        "preferences": "实用性、美观性、文化价值",
                        "shopping_habits": "关注社交媒体评价，重视性价比",
                        "cultural_interest": "传统文化与现代设计的结合",
                        "budget_range": "中等价位，注重品质"
                    }
                }
            ]
        },
        "designer_1": {
            "name": "王设计师",
            "background": "23岁的产品设计师，研究生在读",
            "memories": [
                {
                    "type": "background",
                    "content": {
                        "design_philosophy": "艺术性与实用性的平衡",
                        "expertise": "用户研究、交互设计、视觉设计",
                        "approach": "协作和迭代的设计方法",
                        "goal": "创造满足用户需求的愉悦体验"
                    }
                }
            ]
        },
        "manufacturer_1": {
            "name": "陈总",
            "background": "35岁的文化创意产品生产商，4年行业经验",
            "memories": [
                {
                    "type": "background",
                    "content": {
                        "focus_areas": "材料成本、生产效率、质量控制、供应链管理",
                        "experience": "大规模生产工艺流程和限制",
                        "concerns": "设计可行性、成本控制、市场需求",
                        "approach": "与设计团队紧密合作，确保产品质量"
                    }
                }
            ]
        }
    }
    
    # 为每个智能体添加背景记忆
    for agent_id, data in agent_backgrounds.items():
        try:
            memory = MemoryAdapter(agent_id, storage_type="auto", settings=settings)
            
            for memory_data in data["memories"]:
                await memory.add_memory(memory_data["type"], memory_data["content"])
            
            print(f"✅ 为 {data['name']} ({agent_id}) 添加背景记忆")
            
        except Exception as e:
            print(f"❌ 为 {agent_id} 添加记忆失败: {str(e)}")
    
    # 2. 测试增强后的记忆效果
    print("\n2. 测试增强后的记忆效果...")
    
    try:
        # 获取craftsman_1的记忆
        memory = MemoryAdapter("craftsman_1", storage_type="auto", settings=settings)
        memories = await memory.get_relevant_memories("产品设计", limit=5)
        
        print(f"📚 craftsman_1的相关记忆数量: {len(memories)}")
        if memories:
            print("📝 记忆内容预览:")
            for i, mem in enumerate(memories[:3], 1):
                print(f"   {i}. {mem[:100]}...")
        
        # 构建增强prompt示例
        enhanced_prompt = EnhancedMemoryPromptBuilder.build_enhanced_discussion_prompt(
            agent_name="张师傅",
            agent_role="craftsman",
            agent_background="65岁的蒙古族剪纸艺术传承人，从事剪纸艺术45年",
            topic="剪纸文创产品的现代化设计",
            personal_memories=memories,
            global_context="【李女士】: 我希望产品既实用又有文化内涵\n【王设计师】: 可以考虑用现代材料和工艺",
            base_prompt="请分享你对这个话题的看法和建议。"
        )
        
        print(f"\n🎯 增强prompt示例:")
        print(f"长度: {len(enhanced_prompt)} 字符")
        print(f"内容预览:\n{enhanced_prompt[:400]}...")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    # 3. 提供使用建议
    print(f"\n3. 使用建议:")
    print(f"✅ 记忆功能已增强，现在智能体会有更丰富的背景记忆")
    print(f"✅ 在对话中，智能体会更多地体现个人特色和专业背景")
    print(f"✅ 建议在agent.py中使用EnhancedMemoryPromptBuilder来构建prompt")
    print(f"✅ 可以通过添加更多个人化记忆来进一步提升效果")
    
    print("\n" + "=" * 60)
    print("🏁 记忆功能增强完成")


async def demonstrate_memory_difference():
    """演示记忆功能的差异"""
    print("\n🎭 演示记忆功能的差异...")
    
    settings = Settings()
    memory = MemoryAdapter("craftsman_1", storage_type="auto", settings=settings)
    
    # 获取记忆
    memories = await memory.get_relevant_memories("传统文化", limit=3)
    
    print(f"\n📊 记忆使用对比:")
    print(f"有记忆版本特征:")
    print(f"  - 提到具体的个人经历和年龄")
    print(f"  - 使用专业术语和材料名称")
    print(f"  - 体现个人情感和态度")
    print(f"  - 回应其他人的具体发言")
    
    print(f"\n无记忆版本特征:")
    print(f"  - 通用的建议和观点")
    print(f"  - 缺乏个人化特色")
    print(f"  - 教科书式的回答")
    print(f"  - 没有情感色彩")
    
    if memories:
        print(f"\n📝 当前可用记忆:")
        for i, mem in enumerate(memories, 1):
            print(f"   {i}. {mem[:80]}...")


if __name__ == "__main__":
    async def main():
        await apply_memory_enhancement()
        await demonstrate_memory_difference()
    
    asyncio.run(main())
