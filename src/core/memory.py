#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
记忆模块
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional


class Memory:
    """记忆模块"""

    def __init__(
        self,
        agent_id: str,
        storage_type: str = "memory",
        max_tokens: int = 4000,
        settings: Any = None
    ):
        """
        初始化记忆模块

        Args:
            agent_id: 智能体ID
            storage_type: 存储类型，可选值：memory（内存）, file（文件）
            max_tokens: 最大记忆令牌数
            settings: 全局设置
        """
        self.agent_id = agent_id
        self.storage_type = storage_type
        self.max_tokens = max_tokens
        self.settings = settings
        self.memories: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(f"memory.{agent_id}")

        # 如果使用文件存储，确保目录存在
        if self.storage_type == "file" and settings:
            self.memory_dir = os.path.join(settings.DATA_DIR, "memories", agent_id)
            os.makedirs(self.memory_dir, exist_ok=True)
            self.memory_file = os.path.join(self.memory_dir, "memory.json")
            self._load_memories()

    def add_memory(self, memory_type: str, content: Dict[str, Any]) -> None:
        """
        添加记忆

        Args:
            memory_type: 记忆类型
            content: 记忆内容
        """
        memory = {
            "type": memory_type,
            "content": content,
            "timestamp": time.time()
        }

        self.memories.append(memory)
        self.logger.debug(f"添加记忆: {memory_type}")

        # 如果使用文件存储，保存到文件
        if self.storage_type == "file":
            self._save_memories()

    def get_relevant_memories(self, topic: str, limit: int = 5) -> List[str]:
        """
        获取相关记忆

        Args:
            topic: 主题
            limit: 最大返回数量

        Returns:
            相关记忆的文本表示
        """
        # 简单实现：按时间戳排序，返回最近的记忆
        sorted_memories = sorted(self.memories, key=lambda x: x.get("timestamp", 0), reverse=True)

        # 格式化记忆
        formatted_memories = []
        for memory in sorted_memories[:limit]:
            formatted_memory = self._format_memory_as_text(memory)
            if formatted_memory:
                formatted_memories.append(formatted_memory)

        return formatted_memories

    def get_all_memories(self) -> List[str]:
        """
        获取所有记忆

        Returns:
            所有记忆的文本表示
        """
        formatted_memories = []

        # 按时间戳排序
        sorted_memories = sorted(self.memories, key=lambda x: x.get("timestamp", 0))

        # 格式化每条记忆
        for memory in sorted_memories:
            formatted_memory = self._format_memory_as_text(memory)
            if formatted_memory:
                formatted_memories.append(formatted_memory)

        return formatted_memories

    def get_memories_by_type(self, memory_type: str) -> List[str]:
        """
        获取指定类型的记忆

        Args:
            memory_type: 记忆类型

        Returns:
            指定类型记忆的文本表示
        """
        # 获取指定类型的记忆
        type_memories = [m for m in self.memories if m.get("type") == memory_type]

        # 按时间戳排序
        sorted_memories = sorted(type_memories, key=lambda x: x.get("timestamp", 0))

        # 格式化记忆
        formatted_memories = []
        for memory in sorted_memories:
            formatted_memory = self._format_memory_as_text(memory)
            if formatted_memory:
                formatted_memories.append(formatted_memory)

        return formatted_memories

    def get_conversation_history(self) -> str:
        """
        获取对话历史

        Returns:
            对话历史的文本表示
        """
        # 获取讨论类型的记忆
        discussion_memories = [m for m in self.memories if m.get("type") == "discussion"]

        # 按时间戳排序
        sorted_discussions = sorted(discussion_memories, key=lambda x: x.get("timestamp", 0))

        # 格式化对话历史
        history = []
        for memory in sorted_discussions:
            content = memory.get("content", {})
            role = content.get("role", "unknown")
            topic = content.get("topic", "unknown")
            text = content.get("content", "")

            history.append(f"{role} 关于 {topic} 的发言: {text}")

        return "\n\n".join(history)

    def clear_memories(self) -> None:
        """清空记忆"""
        self.memories = []

        # 如果使用文件存储，删除文件
        if self.storage_type == "file" and os.path.exists(self.memory_file):
            os.remove(self.memory_file)

    def _format_memory_as_text(self, memory: Dict[str, Any]) -> str:
        """
        将记忆格式化为文本

        Args:
            memory: 记忆数据

        Returns:
            格式化后的文本
        """
        memory_type = memory.get("type", "")
        content = memory.get("content", {})
        timestamp = memory.get("timestamp", 0)

        # 格式化时间戳
        time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        # 根据记忆类型格式化内容
        if memory_type == "introduction":
            role = content.get("role", "unknown")
            text = content.get("content", "")
            return f"[{time_str}] 自我介绍 ({role}): {text}"

        elif memory_type == "discussion":
            role = content.get("role", "unknown")
            topic = content.get("topic", "unknown")
            text = content.get("content", "")
            return f"[{time_str}] 讨论 ({role} 关于 {topic}): {text}"

        elif memory_type == "keywords":
            role = content.get("role", "unknown")
            topic = content.get("topic", "unknown")
            keywords = content.get("keywords", [])
            keywords_str = ", ".join(keywords)
            return f"[{time_str}] 关键词 ({role} 关于 {topic}): {keywords_str}"

        elif memory_type == "voting":
            role = content.get("role", "unknown")
            topic = content.get("topic", "unknown")
            voted_keywords = content.get("voted_keywords", [])
            voted_str = ", ".join([k[0] for k in voted_keywords])
            return f"[{time_str}] 投票 ({role} 关于 {topic}): {voted_str}"

        elif memory_type == "role_switch":
            previous_role = content.get("previous_role", "unknown")
            new_role = content.get("new_role", "unknown")
            return f"[{time_str}] 角色转换: 从 {previous_role} 转换为 {new_role}"

        elif memory_type == "image_story":
            role = content.get("role", "unknown")
            story = content.get("story", "")
            keywords = content.get("keywords", [])
            keywords_str = ", ".join(keywords)
            return f"[{time_str}] 图片故事 ({role}): {story}\n关键词: {keywords_str}"

        elif memory_type == "design_card":
            role = content.get("role", "unknown")
            design = content.get("content", "")
            keywords = content.get("keywords", [])
            keywords_str = ", ".join(keywords)
            return f"[{time_str}] 设计卡牌 ({role}): {design}\n关键词: {keywords_str}"

        else:
            # 默认格式化
            return f"[{time_str}] {memory_type}: {str(content)}"

    def _save_memories(self) -> None:
        """保存记忆到文件"""
        if self.storage_type != "file":
            return

        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.memories, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存记忆失败: {str(e)}")

    def _load_memories(self) -> None:
        """从文件加载记忆"""
        if self.storage_type != "file" or not os.path.exists(self.memory_file):
            return

        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                self.memories = json.load(f)
        except Exception as e:
            self.logger.error(f"加载记忆失败: {str(e)}")
            self.memories = []
