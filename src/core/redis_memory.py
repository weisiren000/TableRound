#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Redis记忆模块
"""

import json
import logging
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import redis.asyncio as redis


class RedisMemory:
    """基于Redis的记忆模块"""

    def __init__(
        self,
        agent_id: str,
        redis_client: redis.Redis,
        max_memories: int = 1000,
        ttl: int = 86400 * 7  # 7天过期
    ):
        """
        初始化Redis记忆模块

        Args:
            agent_id: 智能体ID
            redis_client: Redis客户端
            max_memories: 最大记忆数量
            ttl: 记忆过期时间（秒）
        """
        self.agent_id = agent_id
        self.redis = redis_client
        self.max_memories = max_memories
        self.ttl = ttl
        self.logger = logging.getLogger(f"redis_memory.{agent_id}")

        # Redis Key前缀
        self.key_prefix = f"agent:{agent_id}"
        self.memories_list_key = f"{self.key_prefix}:memories:list"
        self.memories_types_key = f"{self.key_prefix}:memories:types"
        self.stats_key = f"{self.key_prefix}:stats"

    async def add_memory(self, memory_type: str, content: Dict[str, Any]) -> str:
        """
        添加记忆

        Args:
            memory_type: 记忆类型
            content: 记忆内容

        Returns:
            记忆ID
        """
        memory_id = f"{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"
        timestamp = time.time()
        
        memory_data = {
            "id": memory_id,
            "type": memory_type,
            "content": json.dumps(content, ensure_ascii=False),
            "timestamp": str(timestamp),
            "agent_id": self.agent_id,
            "created_at": datetime.fromtimestamp(timestamp).isoformat()
        }

        try:
            # 使用管道进行原子操作
            pipe = self.redis.pipeline()
            
            # 存储记忆详情
            memory_key = f"{self.key_prefix}:memory:{memory_id}"
            pipe.hset(memory_key, mapping=memory_data)
            pipe.expire(memory_key, self.ttl)
            
            # 添加到有序列表（按时间戳排序）
            pipe.zadd(self.memories_list_key, {memory_id: timestamp})
            pipe.expire(self.memories_list_key, self.ttl)
            
            # 按类型分组
            type_key = f"{self.memories_types_key}:{memory_type}"
            pipe.zadd(type_key, {memory_id: timestamp})
            pipe.expire(type_key, self.ttl)
            
            # 限制记忆数量（保留最新的）
            pipe.zremrangebyrank(self.memories_list_key, 0, -(self.max_memories + 1))
            
            # 更新统计信息
            pipe.hincrby(self.stats_key, "total_memories", 1)
            pipe.hincrby(self.stats_key, f"type_{memory_type}", 1)
            pipe.hset(self.stats_key, "last_update", timestamp)
            pipe.expire(self.stats_key, self.ttl)
            
            await pipe.execute()
            
            self.logger.debug(f"添加记忆成功: {memory_type} - {memory_id}")
            return memory_id
            
        except Exception as e:
            self.logger.error(f"添加记忆失败: {str(e)}")
            raise

    async def get_relevant_memories(self, topic: str, limit: int = 5) -> List[str]:
        """
        获取相关记忆

        Args:
            topic: 主题
            limit: 最大返回数量

        Returns:
            相关记忆的文本表示
        """
        try:
            # 获取最近的记忆ID（按时间戳倒序）
            memory_ids = await self.redis.zrevrange(
                self.memories_list_key, 0, limit - 1
            )
            
            if not memory_ids:
                return []
            
            # 批量获取记忆详情
            pipe = self.redis.pipeline()
            for memory_id in memory_ids:
                memory_key = f"{self.key_prefix}:memory:{memory_id.decode()}"
                pipe.hgetall(memory_key)
            
            memories_data = await pipe.execute()
            
            # 格式化记忆
            formatted_memories = []
            for memory_data in memories_data:
                if memory_data:
                    formatted_memory = await self._format_memory_as_text(memory_data)
                    if formatted_memory:
                        formatted_memories.append(formatted_memory)
            
            return formatted_memories
            
        except Exception as e:
            self.logger.error(f"获取相关记忆失败: {str(e)}")
            return []

    async def get_memories_by_type(self, memory_type: str, limit: int = 10) -> List[str]:
        """
        获取指定类型的记忆

        Args:
            memory_type: 记忆类型
            limit: 最大返回数量

        Returns:
            指定类型记忆的文本表示
        """
        try:
            type_key = f"{self.memories_types_key}:{memory_type}"
            memory_ids = await self.redis.zrevrange(type_key, 0, limit - 1)
            
            if not memory_ids:
                return []
            
            # 批量获取记忆详情
            pipe = self.redis.pipeline()
            for memory_id in memory_ids:
                memory_key = f"{self.key_prefix}:memory:{memory_id.decode()}"
                pipe.hgetall(memory_key)
            
            memories_data = await pipe.execute()
            
            # 格式化记忆
            formatted_memories = []
            for memory_data in memories_data:
                if memory_data:
                    formatted_memory = await self._format_memory_as_text(memory_data)
                    if formatted_memory:
                        formatted_memories.append(formatted_memory)
            
            return formatted_memories
            
        except Exception as e:
            self.logger.error(f"获取类型记忆失败: {str(e)}")
            return []

    async def get_all_memories(self) -> List[str]:
        """
        获取所有记忆

        Returns:
            所有记忆的文本表示
        """
        try:
            # 获取所有记忆ID（按时间戳正序）
            memory_ids = await self.redis.zrange(self.memories_list_key, 0, -1)
            
            if not memory_ids:
                return []
            
            # 批量获取记忆详情
            pipe = self.redis.pipeline()
            for memory_id in memory_ids:
                memory_key = f"{self.key_prefix}:memory:{memory_id.decode()}"
                pipe.hgetall(memory_key)
            
            memories_data = await pipe.execute()
            
            # 格式化记忆
            formatted_memories = []
            for memory_data in memories_data:
                if memory_data:
                    formatted_memory = await self._format_memory_as_text(memory_data)
                    if formatted_memory:
                        formatted_memories.append(formatted_memory)
            
            return formatted_memories
            
        except Exception as e:
            self.logger.error(f"获取所有记忆失败: {str(e)}")
            return []

    async def clear_memories(self) -> None:
        """清空记忆"""
        try:
            # 获取所有相关的key
            pattern = f"{self.key_prefix}:*"
            keys = []
            
            async for key in self.redis.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                await self.redis.delete(*keys)
            
            self.logger.info(f"清空记忆成功，删除了 {len(keys)} 个key")
            
        except Exception as e:
            self.logger.error(f"清空记忆失败: {str(e)}")

    async def get_memory_stats(self) -> Dict[str, Any]:
        """
        获取记忆统计信息

        Returns:
            统计信息字典
        """
        try:
            stats = await self.redis.hgetall(self.stats_key)
            
            # 解码并转换数据类型
            decoded_stats = {}
            for key, value in stats.items():
                key_str = key.decode() if isinstance(key, bytes) else key
                value_str = value.decode() if isinstance(value, bytes) else value
                
                if key_str.startswith('type_') or key_str == 'total_memories':
                    decoded_stats[key_str] = int(value_str)
                else:
                    decoded_stats[key_str] = value_str
            
            return decoded_stats
            
        except Exception as e:
            self.logger.error(f"获取统计信息失败: {str(e)}")
            return {}

    async def _format_memory_as_text(self, memory_data: Dict) -> str:
        """
        将记忆格式化为文本

        Args:
            memory_data: 记忆数据

        Returns:
            格式化后的文本
        """
        try:
            # 解码字节数据
            decoded_data = {}
            for key, value in memory_data.items():
                key_str = key.decode() if isinstance(key, bytes) else key
                value_str = value.decode() if isinstance(value, bytes) else value
                decoded_data[key_str] = value_str
            
            memory_type = decoded_data.get("type", "")
            content_str = decoded_data.get("content", "{}")
            timestamp = float(decoded_data.get("timestamp", 0))
            
            # 解析内容JSON
            try:
                content = json.loads(content_str)
            except:
                content = {}
            
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
            
            else:
                # 默认格式化
                return f"[{time_str}] {memory_type}: {str(content)}"
                
        except Exception as e:
            self.logger.error(f"格式化记忆失败: {str(e)}")
            return ""
