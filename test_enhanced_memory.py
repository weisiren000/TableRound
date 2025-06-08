#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
增强记忆功能测试
让记忆效果在对话中更明显
"""

import asyncio
from src.core.memory_adapter import MemoryAdapter
from src.core.global_memory import GlobalMemory
from src.config.settings import Settings
from src.models.openrouter import OpenRouterModel


async def test_enhanced_memory_conversation():
    """测试增强记忆功能在对话中的表现"""
    print("🧠 测试增强记忆功能...")
    print("=" * 60)
    
    # 初始化
    settings = Settings()
    # 使用settings的get_model_instance方法
    model = settings.get_model_instance("openrouter", "meta-llama/llama-4-maverick:free")
    
    # 创建记忆适配器
    memory = MemoryAdapter("enhanced_test_agent", storage_type="auto", settings=settings)
    global_memory = GlobalMemory("enhanced_test_session", storage_type="auto")
    
    # 1. 添加丰富的个人记忆
    print("\n1. 添加个人记忆...")
    personal_memories = [
        {
            "type": "introduction",
            "content": {
                "role": "craftsman",
                "name": "张师傅",
                "age": 65,
                "experience": "从事蒙古族剪纸艺术45年",
                "specialty": "传统蝙蝠吉祥纹样设计",
                "philosophy": "传统与现代相结合，让古老艺术焕发新生",
                "memorable_quote": "每一刀都承载着文化的传承"
            }
        },
        {
            "type": "discussion",
            "content": {
                "topic": "中国精神",
                "viewpoint": "中国精神体现在工匠精神中，追求完美，传承文化",
                "personal_story": "我曾经为了一个蝙蝠纹样的对称性，反复修改了三天",
                "emotion": "自豪和责任感"
            }
        },
        {
            "type": "preference",
            "content": {
                "favorite_materials": ["红纸", "金箔", "宣纸"],
                "design_style": "对称美学，寓意吉祥",
                "target_audience": "年轻人和文化爱好者",
                "concerns": "如何让传统艺术被现代人接受"
            }
        }
    ]
    
    for memory_data in personal_memories:
        await memory.add_memory(memory_data["type"], memory_data["content"])
        print(f"✅ 添加{memory_data['type']}记忆")
    
    # 2. 添加全局记忆（其他人的发言）
    print("\n2. 添加全局记忆...")
    await global_memory.add_participant("consumer_zhang", "张女士", "consumer")
    await global_memory.add_participant("designer_li", "李设计师", "designer")
    
    # 模拟其他人的发言
    other_speeches = [
        {
            "agent_id": "consumer_zhang",
            "agent_name": "张女士",
            "content": "我希望剪纸产品能融入现代生活，比如做成手机壳或者书签",
            "speech_type": "discussion"
        },
        {
            "agent_id": "designer_li", 
            "agent_name": "李设计师",
            "content": "蝙蝠纹样确实很有文化内涵，我们可以用现代的色彩搭配来吸引年轻人",
            "speech_type": "discussion"
        }
    ]
    
    for speech in other_speeches:
        await global_memory.record_speech(
            agent_id=speech["agent_id"],
            agent_name=speech["agent_name"],
            speech_type=speech["speech_type"],
            content=speech["content"],
            stage="discussion"
        )
        print(f"✅ 记录{speech['agent_name']}的发言")
    
    # 3. 模拟智能体参与讨论（使用记忆）
    print("\n3. 模拟智能体讨论...")
    topic = "如何设计现代化的剪纸文创产品"
    
    # 获取个人记忆
    personal_memories_text = await memory.get_relevant_memories(topic, limit=5)
    
    # 获取全局上下文
    global_context = await global_memory.get_current_context("enhanced_test_agent", max_context=10)
    
    # 构建增强prompt
    enhanced_prompt = f"""
你是张师傅，一位65岁的蒙古族剪纸艺术传承人，从事剪纸艺术45年。

当前讨论主题：{topic}

你的个人记忆和经验：
{chr(10).join(personal_memories_text) if personal_memories_text else "暂无相关记忆"}

会议中其他人的发言：
{global_context if global_context and "暂无" not in global_context else "暂无其他发言"}

请基于你的个人经验、记忆和其他人的发言，发表你的观点。要体现出：
1. 你的个人经历和专业背景
2. 对其他人发言的回应
3. 具体的建议和想法
4. 你的情感和态度

请用第一人称，以张师傅的身份回答，字数控制在200字左右。
"""
    
    print(f"\n📝 构建的增强prompt:")
    print(f"长度: {len(enhanced_prompt)} 字符")
    print(f"内容预览:\n{enhanced_prompt[:500]}...")
    
    # 使用AI模型生成回复
    print(f"\n🤖 AI生成回复...")
    try:
        response = await model.generate(
            prompt=enhanced_prompt,
            system_prompt="你是一位经验丰富的传统手工艺人，善于结合传统文化和现代需求。"
        )
        
        print(f"\n💬 张师傅的回复:")
        print(f"{response}")
        
        # 分析回复中的记忆体现
        print(f"\n📊 记忆体现分析:")
        memory_indicators = [
            ("个人经历", ["45年", "65岁", "蒙古族", "张师傅"]),
            ("专业术语", ["剪纸", "蝙蝠", "纹样", "对称"]),
            ("回应他人", ["张女士", "李设计师", "手机壳", "书签", "色彩"]),
            ("情感表达", ["自豪", "责任", "传承", "文化"])
        ]
        
        for category, keywords in memory_indicators:
            found_keywords = [kw for kw in keywords if kw in response]
            if found_keywords:
                print(f"✅ {category}: {', '.join(found_keywords)}")
            else:
                print(f"❌ {category}: 未体现")
                
    except Exception as e:
        print(f"❌ AI生成失败: {str(e)}")
    
    # 4. 对比测试：不使用记忆的回复
    print(f"\n4. 对比测试：不使用记忆的回复")
    simple_prompt = f"请就'{topic}'这个话题发表你的观点，字数控制在200字左右。"
    
    try:
        simple_response = await model.generate(
            prompt=simple_prompt,
            system_prompt="你是一位传统手工艺人。"
        )
        
        print(f"\n💬 无记忆版本的回复:")
        print(f"{simple_response}")
        
        print(f"\n📊 对比分析:")
        print(f"有记忆版本长度: {len(response)} 字符")
        print(f"无记忆版本长度: {len(simple_response)} 字符")
        print(f"个性化程度对比: {'有记忆版本更具个性化' if len(response) > len(simple_response) else '差异不明显'}")
        
    except Exception as e:
        print(f"❌ 对比测试失败: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🏁 增强记忆功能测试完成")


if __name__ == "__main__":
    asyncio.run(test_enhanced_memory_conversation())
