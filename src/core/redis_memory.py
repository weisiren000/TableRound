#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Redis记忆模块 - 优化版本
"""

import json
import logging
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import redis.asyncio as redis

# 常量定义
UUID_LENGTH = 8
DEFAULT_BATCH_SIZE = 100
MAX_RETRIES = 3


class RedisMemory:
    """基于Redis的记忆模块 - 优化版本"""

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

        # 本地缓存（简单的LRU缓存）
        self._cache = {}
        self._cache_max_size = 50

    def _safe_decode(self, data: Any) -> str:
        """安全的数据解码"""
        if isinstance(data, bytes):
            return data.decode('utf-8')
        return str(data)

    def _safe_json_dumps(self, obj: Any) -> str:
        """安全的JSON序列化"""
        try:
            return json.dumps(obj, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.warning(f"JSON序列化失败: {e}")
            return json.dumps({"error": "serialization_failed", "original_type": type(obj).__name__})

    def _safe_json_loads(self, json_str: str) -> Dict[str, Any]:
        """安全的JSON反序列化"""
        try:
            return json.loads(json_str)
        except Exception as e:
            self.logger.warning(f"JSON反序列化失败: {e}")
            return {"error": "deserialization_failed", "raw_data": json_str}

    def _generate_memory_id(self) -> str:
        """生成记忆ID"""
        return f"{int(time.time() * 1000)}_{uuid.uuid4().hex[:UUID_LENGTH]}"

    def _update_cache(self, key: str, value: Any) -> None:
        """更新本地缓存"""
        if len(self._cache) >= self._cache_max_size:
            # 简单的LRU：删除最旧的条目
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[key] = value

    def _get_from_cache(self, key: str) -> Optional[Any]:
        """从缓存获取数据"""
        return self._cache.get(key)

    async def add_memory(self, memory_type: str, content: Dict[str, Any]) -> str:
        """
        添加记忆 - 优化版本

        Args:
            memory_type: 记忆类型
            content: 记忆内容

        Returns:
            记忆ID
        """
        memory_id = self._generate_memory_id()
        timestamp = time.time()

        memory_data = {
            "id": memory_id,
            "type": memory_type,
            "content": self._safe_json_dumps(content),
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

            # 更新统计信息
            pipe.hincrby(self.stats_key, "total_memories", 1)
            pipe.hincrby(self.stats_key, f"type_{memory_type}", 1)
            pipe.hset(self.stats_key, "last_update", timestamp)
            pipe.expire(self.stats_key, self.ttl)

            # 执行管道操作
            results = await pipe.execute()

            # 检查执行结果
            if not all(results[:4]):  # 检查前4个关键操作
                raise Exception("Pipeline执行部分失败")

            # 异步清理旧记忆（避免在同一事务中）
            await self._cleanup_old_memories()

            # 更新缓存
            self._update_cache(f"memory:{memory_id}", memory_data)

            self.logger.info(f"添加记忆成功: {memory_type} - {memory_id}")
            return memory_id

        except Exception as e:
            self.logger.error(f"添加记忆失败: {str(e)}", exc_info=True)
            raise

    async def _cleanup_old_memories(self) -> None:
        """清理旧记忆（异步执行）"""
        try:
            # 获取当前记忆数量
            count = await self.redis.zcard(self.memories_list_key)
            if count > self.max_memories:
                # 删除最旧的记忆
                to_remove = count - self.max_memories
                old_memory_ids = await self.redis.zrange(self.memories_list_key, 0, to_remove - 1)

                if old_memory_ids:
                    pipe = self.redis.pipeline()
                    for memory_id in old_memory_ids:
                        memory_id_str = self._safe_decode(memory_id)
                        memory_key = f"{self.key_prefix}:memory:{memory_id_str}"
                        pipe.delete(memory_key)

                    # 从索引中删除
                    pipe.zremrangebyrank(self.memories_list_key, 0, to_remove - 1)
                    await pipe.execute()

                    self.logger.debug(f"清理了 {len(old_memory_ids)} 条旧记忆")

        except Exception as e:
            self.logger.warning(f"清理旧记忆失败: {str(e)}")

    async def _get_memories_batch(
        self,
        key: str,
        limit: int,
        reverse: bool = False,
        start: int = 0
    ) -> List[str]:
        """
        批量获取记忆的通用方法

        Args:
            key: Redis key
            limit: 限制数量
            reverse: 是否倒序
            start: 起始位置

        Returns:
            格式化的记忆列表
        """
        try:
            # 从Redis获取记忆ID
            if reverse:
                memory_ids = await self.redis.zrevrange(key, start, start + limit - 1)
            else:
                memory_ids = await self.redis.zrange(key, start, start + limit - 1)

            if not memory_ids:
                return []

            # 批量获取记忆详情
            pipe = self.redis.pipeline()
            for memory_id in memory_ids:
                memory_id_str = self._safe_decode(memory_id)
                memory_key = f"{self.key_prefix}:memory:{memory_id_str}"

                # 先检查缓存
                cached_data = self._get_from_cache(f"memory:{memory_id_str}")
                if cached_data:
                    continue

                pipe.hgetall(memory_key)

            memories_data = await pipe.execute()

            # 格式化记忆
            formatted_memories = []
            cache_index = 0

            for i, memory_id in enumerate(memory_ids):
                memory_id_str = self._safe_decode(memory_id)

                # 先尝试从缓存获取
                cached_data = self._get_from_cache(f"memory:{memory_id_str}")
                if cached_data:
                    formatted_memory = await self._format_memory_as_text(cached_data)
                else:
                    # 从Redis结果获取
                    if cache_index < len(memories_data):
                        memory_data = memories_data[cache_index]
                        cache_index += 1

                        if memory_data:
                            # 更新缓存
                            self._update_cache(f"memory:{memory_id_str}", memory_data)
                            formatted_memory = await self._format_memory_as_text(memory_data)
                        else:
                            continue
                    else:
                        continue

                if formatted_memory:
                    formatted_memories.append(formatted_memory)

            return formatted_memories

        except Exception as e:
            self.logger.error(f"批量获取记忆失败: {str(e)}")
            return []

    async def get_relevant_memories(self, topic: str, limit: int = 5) -> List[str]:
        """
        获取相关记忆 - 优化版本

        Args:
            topic: 主题（当前版本基于时间，未来可实现语义匹配）
            limit: 最大返回数量

        Returns:
            相关记忆的文本表示
        """
        try:
            # TODO: 实现基于topic的语义匹配
            # 当前版本：返回最近的记忆作为临时方案
            self.logger.debug(f"获取与主题 '{topic}' 相关的记忆，限制 {limit} 条")

            # 使用通用批量获取方法
            return await self._get_memories_batch(
                self.memories_list_key,
                limit,
                reverse=True  # 最新的记忆优先
            )

        except Exception as e:
            self.logger.error(f"获取相关记忆失败: {str(e)}")
            return []

    async def search_memories_by_content(self, keyword: str, limit: int = 10) -> List[str]:
        """
        根据内容关键词搜索记忆

        Args:
            keyword: 搜索关键词
            limit: 最大返回数量

        Returns:
            匹配的记忆列表
        """
        try:
            # 获取所有记忆进行内容匹配
            all_memories = await self._get_memories_batch(
                self.memories_list_key,
                self.max_memories,
                reverse=True
            )

            # 简单的关键词匹配
            matched_memories = []
            keyword_lower = keyword.lower()

            for memory in all_memories:
                if keyword_lower in memory.lower():
                    matched_memories.append(memory)
                    if len(matched_memories) >= limit:
                        break

            self.logger.debug(f"关键词 '{keyword}' 匹配到 {len(matched_memories)} 条记忆")
            return matched_memories

        except Exception as e:
            self.logger.error(f"搜索记忆失败: {str(e)}")
            return []

    async def get_memories_by_type(self, memory_type: str, limit: int = 10) -> List[str]:
        """
        获取指定类型的记忆 - 优化版本

        Args:
            memory_type: 记忆类型
            limit: 最大返回数量

        Returns:
            指定类型记忆的文本表示
        """
        try:
            type_key = f"{self.memories_types_key}:{memory_type}"

            # 使用通用批量获取方法
            return await self._get_memories_batch(type_key, limit, reverse=True)

        except Exception as e:
            self.logger.error(f"获取类型记忆失败: {str(e)}")
            return []

    async def get_all_memories(self) -> List[str]:
        """
        获取所有记忆 - 优化版本

        Returns:
            所有记忆的文本表示
        """
        try:
            # 使用通用批量获取方法，按时间正序
            return await self._get_memories_batch(
                self.memories_list_key,
                self.max_memories,
                reverse=False  # 按时间正序
            )

        except Exception as e:
            self.logger.error(f"获取所有记忆失败: {str(e)}")
            return []

    async def get_recent_memories(self, limit: int = 10) -> List[str]:
        """
        获取最近的记忆

        Args:
            limit: 限制数量

        Returns:
            最近的记忆列表
        """
        try:
            return await self._get_memories_batch(
                self.memories_list_key,
                limit,
                reverse=True  # 最新的优先
            )

        except Exception as e:
            self.logger.error(f"获取最近记忆失败: {str(e)}")
            return []

    async def clear_memories(self) -> int:
        """
        清空记忆 - 优化版本

        Returns:
            删除的key数量
        """
        try:
            # 分批获取和删除key，避免一次性加载太多
            pattern = f"{self.key_prefix}:*"
            deleted_count = 0
            batch_size = DEFAULT_BATCH_SIZE

            # 使用scan_iter分批处理
            keys_batch = []
            async for key in self.redis.scan_iter(match=pattern, count=batch_size):
                keys_batch.append(key)

                # 达到批次大小时执行删除
                if len(keys_batch) >= batch_size:
                    if keys_batch:
                        await self.redis.delete(*keys_batch)
                        deleted_count += len(keys_batch)
                        keys_batch = []

            # 删除剩余的key
            if keys_batch:
                await self.redis.delete(*keys_batch)
                deleted_count += len(keys_batch)

            # 清空本地缓存
            self._cache.clear()

            self.logger.info(f"清空记忆成功，删除了 {deleted_count} 个key")
            return deleted_count

        except Exception as e:
            self.logger.error(f"清空记忆失败: {str(e)}")
            return 0

    async def get_memory_stats(self) -> Dict[str, Any]:
        """
        获取记忆统计信息 - 优化版本

        Returns:
            统计信息字典
        """
        try:
            # 获取基础统计信息
            stats = await self.redis.hgetall(self.stats_key)

            # 安全的解码并转换数据类型
            decoded_stats = {}
            for key, value in stats.items():
                key_str = self._safe_decode(key)
                value_str = self._safe_decode(value)

                # 安全的类型转换
                if key_str.startswith('type_') or key_str == 'total_memories':
                    try:
                        decoded_stats[key_str] = int(value_str)
                    except ValueError:
                        self.logger.warning(f"无法转换统计值为整数: {key_str}={value_str}")
                        decoded_stats[key_str] = 0
                else:
                    decoded_stats[key_str] = value_str

            # 添加实时统计信息
            try:
                total_count = await self.redis.zcard(self.memories_list_key)
                decoded_stats['current_memory_count'] = total_count
                decoded_stats['cache_size'] = len(self._cache)
                decoded_stats['max_memories'] = self.max_memories
                decoded_stats['ttl_seconds'] = self.ttl
                decoded_stats['agent_id'] = self.agent_id
            except Exception as e:
                self.logger.warning(f"获取实时统计信息失败: {str(e)}")

            return decoded_stats

        except Exception as e:
            self.logger.error(f"获取统计信息失败: {str(e)}")
            return {}

    async def _format_memory_as_text(self, memory_data: Dict) -> str:
        """
        将记忆格式化为文本 - 优化版本

        Args:
            memory_data: 记忆数据

        Returns:
            格式化后的文本
        """
        try:
            # 安全解码字节数据
            decoded_data = {}
            for key, value in memory_data.items():
                key_str = self._safe_decode(key)
                value_str = self._safe_decode(value)
                decoded_data[key_str] = value_str

            memory_type = decoded_data.get("type", "unknown")
            content_str = decoded_data.get("content", "{}")
            timestamp_str = decoded_data.get("timestamp", "0")

            # 安全解析时间戳
            try:
                timestamp = float(timestamp_str)
            except ValueError:
                timestamp = time.time()  # 使用当前时间作为默认值

            # 安全解析内容JSON
            content = self._safe_json_loads(content_str)

            # 格式化时间戳
            try:
                time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, OSError):
                time_str = "未知时间"

            # 根据记忆类型格式化内容
            return self._format_by_type(memory_type, content, time_str)

        except Exception as e:
            self.logger.error(f"格式化记忆失败: {str(e)}")
            return f"[格式化失败] 类型: {memory_data.get('type', 'unknown')}"

    def _format_by_type(self, memory_type: str, content: Dict[str, Any], time_str: str) -> str:
        """
        根据记忆类型格式化内容

        Args:
            memory_type: 记忆类型
            content: 记忆内容
            time_str: 格式化的时间字符串

        Returns:
            格式化后的文本
        """
        try:
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
                keywords_str = ", ".join(str(k) for k in keywords)
                return f"[{time_str}] 关键词 ({role} 关于 {topic}): {keywords_str}"

            elif memory_type == "voting":
                role = content.get("role", "unknown")
                topic = content.get("topic", "unknown")
                voted_keywords = content.get("voted_keywords", [])
                if isinstance(voted_keywords, list) and voted_keywords:
                    # 处理投票关键词格式
                    voted_str = ", ".join([
                        k[0] if isinstance(k, (list, tuple)) and k else str(k)
                        for k in voted_keywords
                    ])
                else:
                    voted_str = "无"
                return f"[{time_str}] 投票 ({role} 关于 {topic}): {voted_str}"

            elif memory_type == "role_switch":
                previous_role = content.get("previous_role", "unknown")
                new_role = content.get("new_role", "unknown")
                return f"[{time_str}] 角色转换: 从 {previous_role} 转换为 {new_role}"

            elif memory_type == "image_story":
                role = content.get("role", "unknown")
                story = content.get("story", "")
                keywords = content.get("keywords", [])
                keywords_str = ", ".join(str(k) for k in keywords)
                return f"[{time_str}] 图片故事 ({role}): {story}\n关键词: {keywords_str}"

            elif memory_type == "design_card":
                role = content.get("role", "unknown")
                design = content.get("content", "")
                keywords = content.get("keywords", [])
                keywords_str = ", ".join(str(k) for k in keywords)
                return f"[{time_str}] 设计卡牌 ({role}): {design}\n关键词: {keywords_str}"

            else:
                # 默认格式化
                content_preview = str(content)[:100] + "..." if len(str(content)) > 100 else str(content)
                return f"[{time_str}] {memory_type}: {content_preview}"

        except Exception as e:
            self.logger.warning(f"格式化记忆类型 {memory_type} 失败: {str(e)}")
            return f"[{time_str}] {memory_type}: [格式化错误]"

    async def health_check(self) -> Dict[str, Any]:
        """
        健康检查

        Returns:
            健康状态信息
        """
        try:
            # 检查Redis连接
            await self.redis.ping()

            # 获取基本统计
            stats = await self.get_memory_stats()

            return {
                "status": "healthy",
                "redis_connected": True,
                "agent_id": self.agent_id,
                "memory_count": stats.get("current_memory_count", 0),
                "cache_size": len(self._cache),
                "timestamp": time.time()
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "redis_connected": False,
                "error": str(e),
                "agent_id": self.agent_id,
                "timestamp": time.time()
            }
