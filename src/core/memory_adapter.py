#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
记忆模块适配器 - Redis统一存储接口
"""

import logging
from typing import Dict, List, Any, Optional
from src.core.redis_memory import RedisMemory
from src.config.redis_config import RedisSettings, get_redis_client


class MemoryAdapter:
    """记忆模块适配器，提供Redis统一存储接口"""

    def __init__(
        self,
        agent_id: str,
        storage_type: str = "redis",  # 只支持redis
        max_tokens: int = 4000,
        settings: Any = None
    ):
        """
        初始化记忆适配器

        Args:
            agent_id: 智能体ID
            storage_type: 存储类型 (只支持redis，保持兼容性)
            max_tokens: 最大记忆令牌数（保留参数兼容性）
            settings: 全局设置
        """
        self.agent_id = agent_id
        self.storage_type = "redis"  # 强制使用Redis
        self.max_tokens = max_tokens
        self.settings = settings
        self.logger = logging.getLogger(f"memory_adapter.{agent_id}")

        self._memory_impl: Optional[RedisMemory] = None
        self._redis_settings = RedisSettings()
    
    async def _get_memory_impl(self) -> RedisMemory:
        """获取Redis记忆实现实例"""
        if self._memory_impl is not None:
            return self._memory_impl

        try:
            redis_client = await get_redis_client()
            self._memory_impl = RedisMemory(
                agent_id=self.agent_id,
                redis_client=redis_client,
                max_memories=self._redis_settings.MEMORY_MAX_SIZE,
                ttl=self._redis_settings.MEMORY_TTL
            )
            self.logger.info(f"使用Redis存储记忆: {self.agent_id}")
        except Exception as e:
            self.logger.error(f"Redis连接失败: {str(e)}")
            raise RuntimeError(f"Redis记忆模块初始化失败: {str(e)}")

        return self._memory_impl


    
    async def add_memory(self, memory_type: str, content: Dict[str, Any]) -> None:
        """
        添加记忆

        Args:
            memory_type: 记忆类型
            content: 记忆内容
        """
        memory_impl = await self._get_memory_impl()
        await memory_impl.add_memory(memory_type, content)
    
    async def get_relevant_memories(self, topic: str, limit: int = 5) -> List[str]:
        """
        获取相关记忆

        Args:
            topic: 主题
            limit: 最大返回数量

        Returns:
            相关记忆的文本表示
        """
        memory_impl = await self._get_memory_impl()
        return await memory_impl.get_relevant_memories(topic, limit)
    
    async def get_all_memories(self) -> List[str]:
        """
        获取所有记忆

        Returns:
            所有记忆的文本表示
        """
        memory_impl = await self._get_memory_impl()
        return await memory_impl.get_all_memories()

    async def get_memories_by_type(self, memory_type: str) -> List[str]:
        """
        获取指定类型的记忆

        Args:
            memory_type: 记忆类型

        Returns:
            指定类型记忆的文本表示
        """
        memory_impl = await self._get_memory_impl()
        return await memory_impl.get_memories_by_type(memory_type)
    
    async def get_conversation_history(self) -> str:
        """
        获取对话历史

        Returns:
            对话历史的文本表示
        """
        memory_impl = await self._get_memory_impl()
        # Redis版本需要自己实现对话历史格式化
        discussions = await memory_impl.get_memories_by_type("discussion")
        return "\n\n".join(discussions)

    async def clear_memories(self) -> None:
        """清空记忆"""
        memory_impl = await self._get_memory_impl()
        await memory_impl.clear_memories()
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """
        获取记忆统计信息

        Returns:
            统计信息字典
        """
        memory_impl = await self._get_memory_impl()
        return await memory_impl.get_memory_stats()
    
    def is_redis_enabled(self) -> bool:
        """检查是否启用了Redis"""
        return self._redis_settings.ENABLE_REDIS
    
    async def get_storage_info(self) -> Dict[str, Any]:
        """
        获取存储信息

        Returns:
            存储信息字典
        """
        info = {
            "agent_id": self.agent_id,
            "storage_type": "redis",
            "redis_enabled": self._redis_settings.ENABLE_REDIS,
            "max_tokens": self.max_tokens,
            "max_memories": self._redis_settings.MEMORY_MAX_SIZE,
            "ttl": self._redis_settings.MEMORY_TTL,
            "redis_host": self._redis_settings.REDIS_HOST,
            "redis_port": self._redis_settings.REDIS_PORT,
            "redis_db": self._redis_settings.REDIS_DB
        }

        return info
