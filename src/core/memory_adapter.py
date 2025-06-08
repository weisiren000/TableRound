#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
记忆模块适配器 - 支持文件存储和Redis存储的统一接口
"""

import logging
from typing import Dict, List, Any, Optional, Union
from src.core.memory import Memory
from src.core.redis_memory import RedisMemory
from src.config.redis_config import RedisSettings, get_redis_client


class MemoryAdapter:
    """记忆模块适配器，提供统一的记忆接口"""
    
    def __init__(
        self,
        agent_id: str,
        storage_type: str = "auto",  # auto, file, redis
        max_tokens: int = 4000,
        settings: Any = None
    ):
        """
        初始化记忆适配器
        
        Args:
            agent_id: 智能体ID
            storage_type: 存储类型 (auto/file/redis)
            max_tokens: 最大记忆令牌数
            settings: 全局设置
        """
        self.agent_id = agent_id
        self.storage_type = storage_type
        self.max_tokens = max_tokens
        self.settings = settings
        self.logger = logging.getLogger(f"memory_adapter.{agent_id}")
        
        self._memory_impl: Optional[Union[Memory, RedisMemory]] = None
        self._redis_settings = RedisSettings()
    
    async def _get_memory_impl(self) -> Union[Memory, RedisMemory]:
        """获取记忆实现实例"""
        if self._memory_impl is not None:
            return self._memory_impl
        
        # 决定使用哪种存储方式
        use_redis = await self._should_use_redis()
        
        if use_redis:
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
                self.logger.warning(f"Redis连接失败，回退到文件存储: {str(e)}")
                self._memory_impl = Memory(
                    agent_id=self.agent_id,
                    storage_type="file",
                    max_tokens=self.max_tokens,
                    settings=self.settings
                )
        else:
            self._memory_impl = Memory(
                agent_id=self.agent_id,
                storage_type="file",
                max_tokens=self.max_tokens,
                settings=self.settings
            )
            self.logger.info(f"使用文件存储记忆: {self.agent_id}")
        
        return self._memory_impl
    
    async def _should_use_redis(self) -> bool:
        """判断是否应该使用Redis"""
        if self.storage_type == "file":
            return False
        elif self.storage_type == "redis":
            return True
        elif self.storage_type == "auto":
            # 自动判断：如果Redis可用且启用，则使用Redis
            return self._redis_settings.ENABLE_REDIS
        else:
            return False
    
    async def add_memory(self, memory_type: str, content: Dict[str, Any]) -> None:
        """
        添加记忆
        
        Args:
            memory_type: 记忆类型
            content: 记忆内容
        """
        memory_impl = await self._get_memory_impl()
        
        if isinstance(memory_impl, RedisMemory):
            await memory_impl.add_memory(memory_type, content)
        else:
            memory_impl.add_memory(memory_type, content)
    
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
        
        if isinstance(memory_impl, RedisMemory):
            return await memory_impl.get_relevant_memories(topic, limit)
        else:
            return memory_impl.get_relevant_memories(topic, limit)
    
    async def get_all_memories(self) -> List[str]:
        """
        获取所有记忆
        
        Returns:
            所有记忆的文本表示
        """
        memory_impl = await self._get_memory_impl()
        
        if isinstance(memory_impl, RedisMemory):
            return await memory_impl.get_all_memories()
        else:
            return memory_impl.get_all_memories()
    
    async def get_memories_by_type(self, memory_type: str) -> List[str]:
        """
        获取指定类型的记忆
        
        Args:
            memory_type: 记忆类型
            
        Returns:
            指定类型记忆的文本表示
        """
        memory_impl = await self._get_memory_impl()
        
        if isinstance(memory_impl, RedisMemory):
            return await memory_impl.get_memories_by_type(memory_type)
        else:
            return memory_impl.get_memories_by_type(memory_type)
    
    async def get_conversation_history(self) -> str:
        """
        获取对话历史
        
        Returns:
            对话历史的文本表示
        """
        memory_impl = await self._get_memory_impl()
        
        if isinstance(memory_impl, RedisMemory):
            # Redis版本需要自己实现对话历史格式化
            discussions = await memory_impl.get_memories_by_type("discussion")
            return "\n\n".join(discussions)
        else:
            return memory_impl.get_conversation_history()
    
    async def clear_memories(self) -> None:
        """清空记忆"""
        memory_impl = await self._get_memory_impl()
        
        if isinstance(memory_impl, RedisMemory):
            await memory_impl.clear_memories()
        else:
            memory_impl.clear_memories()
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """
        获取记忆统计信息
        
        Returns:
            统计信息字典
        """
        memory_impl = await self._get_memory_impl()
        
        if isinstance(memory_impl, RedisMemory):
            return await memory_impl.get_memory_stats()
        else:
            # 文件存储版本的统计信息
            stats = {
                "total_memories": len(memory_impl.memories),
                "storage_type": "file",
                "agent_id": self.agent_id
            }
            
            # 按类型统计
            type_counts = {}
            for memory in memory_impl.memories:
                memory_type = memory.get("type", "unknown")
                type_counts[f"type_{memory_type}"] = type_counts.get(f"type_{memory_type}", 0) + 1
            
            stats.update(type_counts)
            return stats
    
    def is_redis_enabled(self) -> bool:
        """检查是否启用了Redis"""
        return self._redis_settings.ENABLE_REDIS
    
    async def get_storage_info(self) -> Dict[str, Any]:
        """
        获取存储信息
        
        Returns:
            存储信息字典
        """
        memory_impl = await self._get_memory_impl()
        
        info = {
            "agent_id": self.agent_id,
            "storage_type": "redis" if isinstance(memory_impl, RedisMemory) else "file",
            "redis_enabled": self._redis_settings.ENABLE_REDIS,
            "max_tokens": self.max_tokens
        }
        
        if isinstance(memory_impl, RedisMemory):
            info.update({
                "max_memories": self._redis_settings.MEMORY_MAX_SIZE,
                "ttl": self._redis_settings.MEMORY_TTL,
                "redis_host": self._redis_settings.REDIS_HOST,
                "redis_port": self._redis_settings.REDIS_PORT,
                "redis_db": self._redis_settings.REDIS_DB
            })
        
        return info
