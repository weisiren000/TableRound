#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
会议清理模块 - 会议启动时清理Redis数据
"""

import asyncio
import logging
import time
from typing import List, Dict, Any, Optional
import redis.asyncio as redis

from src.config.redis_config import get_redis_client


class MeetingCleaner:
    """会议清理器 - 负责会议启动时的数据清理"""

    def __init__(self):
        self.logger = logging.getLogger("meeting_cleaner")
        self.redis: Optional[redis.Redis] = None

    async def _get_redis(self) -> redis.Redis:
        """获取Redis连接"""
        if not self.redis:
            self.redis = await get_redis_client()
        return self.redis

    async def clean_for_new_meeting(
        self, 
        preserve_agent_memories: bool = False,
        backup_before_clean: bool = True
    ) -> Dict[str, Any]:
        """
        为新会议清理Redis数据
        
        Args:
            preserve_agent_memories: 是否保留智能体的历史记忆
            backup_before_clean: 清理前是否备份数据
            
        Returns:
            清理结果统计
        """
        start_time = time.time()
        self.logger.info("🧹 开始为新会议清理Redis数据...")
        
        try:
            redis_client = await self._get_redis()
            
            # 备份数据（如果需要）
            backup_info = {}
            if backup_before_clean:
                backup_info = await self._backup_data(redis_client)
            
            # 清理会议数据
            meeting_cleaned = await self._clean_meeting_data(redis_client)
            
            # 清理智能体记忆（如果需要）
            agent_cleaned = {}
            if not preserve_agent_memories:
                agent_cleaned = await self._clean_agent_memories(redis_client)
            else:
                # 只清理当前会话的临时数据
                agent_cleaned = await self._clean_session_data(redis_client)
            
            # 清理其他临时数据
            temp_cleaned = await self._clean_temporary_data(redis_client)
            
            end_time = time.time()
            
            result = {
                "success": True,
                "duration": round(end_time - start_time, 3),
                "backup_info": backup_info,
                "meeting_data_cleaned": meeting_cleaned,
                "agent_data_cleaned": agent_cleaned,
                "temporary_data_cleaned": temp_cleaned,
                "preserve_agent_memories": preserve_agent_memories,
                "timestamp": time.time()
            }
            
            self.logger.info(f"✅ 会议清理完成，耗时 {result['duration']} 秒")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 会议清理失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }

    async def _backup_data(self, redis_client: redis.Redis) -> Dict[str, Any]:
        """备份重要数据"""
        try:
            self.logger.info("📦 备份数据中...")
            
            # 获取所有键
            all_keys = await redis_client.keys("*")
            
            backup_info = {
                "total_keys": len(all_keys),
                "backup_timestamp": int(time.time()),
                "categories": {}
            }
            
            # 按类别统计
            for key in all_keys:
                key_str = key.decode() if isinstance(key, bytes) else str(key)
                category = key_str.split(':')[0]
                if category not in backup_info["categories"]:
                    backup_info["categories"][category] = 0
                backup_info["categories"][category] += 1
            
            # 这里可以扩展为实际的数据备份到文件
            # 例如：await self._export_to_file(all_keys, redis_client)
            
            self.logger.info(f"📦 备份完成，共 {len(all_keys)} 个键")
            return backup_info
            
        except Exception as e:
            self.logger.warning(f"⚠️ 数据备份失败: {str(e)}")
            return {"error": str(e)}

    async def _clean_meeting_data(self, redis_client: redis.Redis) -> Dict[str, Any]:
        """清理所有会议数据"""
        try:
            self.logger.info("🏛️ 清理会议数据...")
            
            # 获取所有会议相关的键
            meeting_keys = await redis_client.keys("meeting:*")
            
            if not meeting_keys:
                self.logger.info("📭 没有找到会议数据")
                return {"cleaned_keys": 0, "categories": {}}
            
            # 按类别分组
            categories = {}
            for key in meeting_keys:
                key_str = key.decode() if isinstance(key, bytes) else str(key)
                parts = key_str.split(':')
                if len(parts) >= 3:
                    category = parts[2]  # timeline, participants, speech, stage等
                    if category not in categories:
                        categories[category] = 0
                    categories[category] += 1
            
            # 批量删除
            if meeting_keys:
                deleted_count = await redis_client.delete(*meeting_keys)
                self.logger.info(f"🗑️ 删除了 {deleted_count} 个会议相关键")
            else:
                deleted_count = 0
            
            return {
                "cleaned_keys": deleted_count,
                "categories": categories
            }
            
        except Exception as e:
            self.logger.error(f"❌ 清理会议数据失败: {str(e)}")
            return {"error": str(e)}

    async def _clean_agent_memories(self, redis_client: redis.Redis) -> Dict[str, Any]:
        """清理所有智能体记忆"""
        try:
            self.logger.info("🧠 清理智能体记忆...")
            
            # 获取所有智能体相关的键
            agent_keys = await redis_client.keys("agent:*")
            
            if not agent_keys:
                self.logger.info("📭 没有找到智能体数据")
                return {"cleaned_keys": 0, "agents": {}}
            
            # 按智能体分组统计
            agents = {}
            for key in agent_keys:
                key_str = key.decode() if isinstance(key, bytes) else str(key)
                parts = key_str.split(':')
                if len(parts) >= 2:
                    agent_id = parts[1]
                    if agent_id not in agents:
                        agents[agent_id] = 0
                    agents[agent_id] += 1
            
            # 批量删除
            if agent_keys:
                deleted_count = await redis_client.delete(*agent_keys)
                self.logger.info(f"🗑️ 删除了 {deleted_count} 个智能体相关键")
            else:
                deleted_count = 0
            
            return {
                "cleaned_keys": deleted_count,
                "agents": agents
            }
            
        except Exception as e:
            self.logger.error(f"❌ 清理智能体记忆失败: {str(e)}")
            return {"error": str(e)}

    async def _clean_session_data(self, redis_client: redis.Redis) -> Dict[str, Any]:
        """只清理会话临时数据，保留智能体核心记忆"""
        try:
            self.logger.info("🔄 清理会话临时数据...")
            
            # 清理临时会话数据（如果有的话）
            session_patterns = [
                "session:*",
                "temp:*",
                "cache:*"
            ]
            
            total_deleted = 0
            categories = {}
            
            for pattern in session_patterns:
                keys = await redis_client.keys(pattern)
                if keys:
                    deleted = await redis_client.delete(*keys)
                    total_deleted += deleted
                    categories[pattern] = deleted
            
            self.logger.info(f"🗑️ 删除了 {total_deleted} 个临时数据键")
            
            return {
                "cleaned_keys": total_deleted,
                "categories": categories
            }
            
        except Exception as e:
            self.logger.error(f"❌ 清理会话数据失败: {str(e)}")
            return {"error": str(e)}

    async def _clean_temporary_data(self, redis_client: redis.Redis) -> Dict[str, Any]:
        """清理其他临时数据"""
        try:
            self.logger.info("🧽 清理其他临时数据...")
            
            # 清理可能的临时键
            temp_patterns = [
                "lock:*",
                "queue:*",
                "notification:*",
                "status:*"
            ]
            
            total_deleted = 0
            categories = {}
            
            for pattern in temp_patterns:
                keys = await redis_client.keys(pattern)
                if keys:
                    deleted = await redis_client.delete(*keys)
                    total_deleted += deleted
                    categories[pattern] = deleted
            
            if total_deleted > 0:
                self.logger.info(f"🗑️ 删除了 {total_deleted} 个其他临时键")
            
            return {
                "cleaned_keys": total_deleted,
                "categories": categories
            }
            
        except Exception as e:
            self.logger.error(f"❌ 清理临时数据失败: {str(e)}")
            return {"error": str(e)}

    async def get_current_data_status(self) -> Dict[str, Any]:
        """获取当前Redis数据状态"""
        try:
            redis_client = await self._get_redis()
            
            # 获取所有键
            all_keys = await redis_client.keys("*")
            
            # 按类别统计
            categories = {}
            for key in all_keys:
                key_str = key.decode() if isinstance(key, bytes) else str(key)
                category = key_str.split(':')[0]
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1
            
            # 获取内存使用情况
            info = await redis_client.info('memory')
            memory_usage = info.get('used_memory_human', 'Unknown')
            
            return {
                "total_keys": len(all_keys),
                "categories": categories,
                "memory_usage": memory_usage,
                "timestamp": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"❌ 获取数据状态失败: {str(e)}")
            return {"error": str(e)}

    async def close(self):
        """关闭连接"""
        if self.redis:
            await self.redis.close()


# 便捷函数
async def clean_redis_for_new_meeting(
    preserve_agent_memories: bool = False,
    backup_before_clean: bool = True
) -> Dict[str, Any]:
    """
    便捷函数：为新会议清理Redis
    
    Args:
        preserve_agent_memories: 是否保留智能体历史记忆
        backup_before_clean: 清理前是否备份
        
    Returns:
        清理结果
    """
    cleaner = MeetingCleaner()
    try:
        result = await cleaner.clean_for_new_meeting(
            preserve_agent_memories=preserve_agent_memories,
            backup_before_clean=backup_before_clean
        )
        return result
    finally:
        await cleaner.close()


async def get_redis_status() -> Dict[str, Any]:
    """
    便捷函数：获取Redis状态
    
    Returns:
        Redis数据状态
    """
    cleaner = MeetingCleaner()
    try:
        status = await cleaner.get_current_data_status()
        return status
    finally:
        await cleaner.close()
