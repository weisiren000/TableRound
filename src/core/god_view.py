#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
上帝视角模块
"""

import logging
from typing import Dict, List, Any, Optional


class GodView:
    """上帝视角类"""

    def __init__(self, settings):
        """
        初始化上帝视角

        Args:
            settings: 全局设置
        """
        self.settings = settings
        self.logger = logging.getLogger("god_view")

    def summarize_discussion(self, discussion_history: List[Dict[str, Any]]) -> str:
        """
        总结讨论

        Args:
            discussion_history: 讨论历史

        Returns:
            总结内容
        """
        self.logger.info("总结讨论")

        # 按阶段分组
        stages = {}
        for item in discussion_history:
            stage = item.get("stage", "unknown")
            if stage not in stages:
                stages[stage] = []
            stages[stage].append(item)

        # 构建总结
        summary = []

        # 自我介绍总结
        if "introduction" in stages:
            intro_summary = "智能体自我介绍:\n"
            for item in stages["introduction"]:
                agent = item.get("agent", "unknown")
                content = item.get("content", "")
                intro_summary += f"- {agent}: {content[:50]}...\n"
            summary.append(intro_summary)

        # 讨论总结
        discussion_stages = [s for s in stages.keys() if s.startswith("discussion_turn_")]
        if discussion_stages:
            discussion_summary = "讨论内容:\n"
            for stage in sorted(discussion_stages):
                discussion_summary += f"- {stage}:\n"
                for item in stages[stage]:
                    agent = item.get("agent", "unknown")
                    content = item.get("content", "")
                    discussion_summary += f"  - {agent}: {content[:50]}...\n"
            summary.append(discussion_summary)

        # 关键词总结
        if "keywords" in stages:
            keywords_summary = "提取的关键词:\n"
            for item in stages["keywords"]:
                agent = item.get("agent", "unknown")
                keywords = item.get("keywords", [])
                keywords_summary += f"- {agent}: {', '.join(keywords)}\n"
            summary.append(keywords_summary)

        # 投票总结
        if "voting" in stages:
            voting_summary = "关键词投票:\n"
            for item in stages["voting"]:
                agent = item.get("agent", "unknown")
                voted_keywords = item.get("voted_keywords", [])
                voting_summary += f"- {agent}: {', '.join(voted_keywords)}\n"
            summary.append(voting_summary)

        # 角色转换总结
        if "role_switch" in stages:
            role_switch_summary = "角色转换:\n"
            for item in stages["role_switch"]:
                agent = item.get("agent", "unknown")
                original_role = item.get("original_role", "unknown")
                new_role = item.get("new_role", "unknown")
                role_switch_summary += f"- {agent}: {original_role} -> {new_role}\n"
            summary.append(role_switch_summary)

        # 角色转换后讨论总结
        if "discussion_after_switch" in stages:
            after_switch_summary = "角色转换后讨论:\n"
            for item in stages["discussion_after_switch"]:
                agent = item.get("agent", "unknown")
                role = item.get("role", "unknown")
                content = item.get("content", "")
                after_switch_summary += f"- {agent} ({role}): {content[:50]}...\n"
            summary.append(after_switch_summary)

        # 角色转换后关键词总结
        if "keywords_after_switch" in stages:
            after_switch_keywords_summary = "角色转换后提取的关键词:\n"
            for item in stages["keywords_after_switch"]:
                agent = item.get("agent", "unknown")
                role = item.get("role", "unknown")
                keywords = item.get("keywords", [])
                after_switch_keywords_summary += f"- {agent} ({role}): {', '.join(keywords)}\n"
            summary.append(after_switch_keywords_summary)

        return "\n\n".join(summary)

    def analyze_keywords(self, keywords: List[str]) -> Dict[str, Any]:
        """
        分析关键词

        Args:
            keywords: 关键词列表

        Returns:
            分析结果
        """
        self.logger.info("分析关键词")

        # 简单分析：统计词频
        word_count = {}
        for keyword in keywords:
            if keyword in word_count:
                word_count[keyword] += 1
            else:
                word_count[keyword] = 1

        # 排序
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

        # 构建结果
        result = {
            "total_keywords": len(keywords),
            "unique_keywords": len(word_count),
            "top_keywords": [w for w, c in sorted_words[:10]],
            "word_count": dict(sorted_words)
        }

        return result

    def guide_discussion(self, topic: str, stage: str) -> str:
        """
        引导讨论

        Args:
            topic: 讨论主题
            stage: 讨论阶段

        Returns:
            引导内容
        """
        self.logger.info(f"引导讨论，主题: {topic}，阶段: {stage}")

        if stage == "introduction":
            return f"欢迎参加关于\"{topic}\"的讨论。请每位智能体先进行自我介绍，让我们相互了解。"

        elif stage == "discussion":
            return f"现在我们开始讨论\"{topic}\"。请每位智能体基于自己的专业背景和经验，分享你的观点和见解。"

        elif stage == "keywords":
            return "请每位智能体从讨论中提取关键词，这些关键词应该能够概括讨论的核心内容。"

        elif stage == "voting":
            return "请每位智能体对提取的关键词进行投票，选出你认为最重要的关键词。"

        elif stage == "role_switch":
            return "现在我们进入角色转换阶段。每位智能体将转换为一个新的角色，但保持记忆的连续性。"

        elif stage == "discussion_after_switch":
            return f"角色转换后，请以新的角色身份继续讨论\"{topic}\"，但保持对之前讨论内容的记忆。"

        else:
            return f"请继续关于\"{topic}\"的讨论。"
