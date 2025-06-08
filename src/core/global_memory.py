#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
全局记忆模块 - 实现AI会议的全局记忆机制
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from src.core.memory_adapter import MemoryAdapter
from src.config.redis_config import get_redis_client, RedisSettings
import redis.asyncio as redis


class GlobalMemory:
    """
    全局记忆模块 - 管理会议期间所有智能体的共享记忆
    
    功能：
    1. 存储所有agent的发言历史
    2. 提供实时的会议上下文
    3. 支持按阶段、按agent、按主题检索
    4. 维护会议的完整时间线
    """
    
    def __init__(self, session_id: str, storage_type: str = "auto"):
        """
        初始化全局记忆
        
        Args:
            session_id: 会议会话ID
            storage_type: 存储类型 (auto/file/redis)
        """
        self.session_id = session_id
        self.storage_type = storage_type
        self.logger = logging.getLogger(f"global_memory.{session_id}")
        
        # 会议状态
        self.meeting_start_time = time.time()
        self.current_stage = "init"
        self.participants = set()  # 参与者列表
        
        # Redis配置
        self._redis_settings = RedisSettings()
        self._redis_client: Optional[redis.Redis] = None
        
        # 全局记忆Key设计
        self.global_key_prefix = f"meeting:{session_id}"
        self.timeline_key = f"{self.global_key_prefix}:timeline"
        self.participants_key = f"{self.global_key_prefix}:participants"
        self.stage_key = f"{self.global_key_prefix}:stage"
        self.context_key = f"{self.global_key_prefix}:context"
    
    async def _get_redis_client(self) -> Optional[redis.Redis]:
        """获取Redis客户端"""
        if self._redis_client is None and self._redis_settings.ENABLE_REDIS:
            try:
                self._redis_client = await get_redis_client()
                return self._redis_client
            except Exception as e:
                self.logger.warning(f"Redis连接失败: {str(e)}")
                return None
        return self._redis_client
    
    async def add_participant(self, agent_id: str, agent_name: str, agent_role: str) -> None:
        """
        添加会议参与者
        
        Args:
            agent_id: 智能体ID
            agent_name: 智能体名称
            agent_role: 智能体角色
        """
        participant_info = {
            "agent_id": agent_id,
            "agent_name": agent_name,
            "agent_role": agent_role,
            "join_time": time.time()
        }
        
        self.participants.add(agent_id)
        
        # 存储到Redis
        redis_client = await self._get_redis_client()
        if redis_client:
            try:
                await redis_client.hset(
                    self.participants_key,
                    agent_id,
                    json.dumps(participant_info, ensure_ascii=False)
                )
                self.logger.info(f"参与者加入会议: {agent_name} ({agent_role})")
            except Exception as e:
                self.logger.error(f"添加参与者到Redis失败: {str(e)}")
    
    async def record_speech(
        self,
        agent_id: str,
        agent_name: str,
        speech_type: str,
        content: str,
        stage: str,
        additional_data: Dict[str, Any] = None
    ) -> str:
        """
        记录智能体发言
        
        Args:
            agent_id: 智能体ID
            agent_name: 智能体名称
            speech_type: 发言类型 (introduction/discussion/keywords/voting等)
            content: 发言内容
            stage: 会议阶段
            additional_data: 额外数据
            
        Returns:
            发言记录ID
        """
        timestamp = time.time()
        speech_id = f"{int(timestamp * 1000)}_{agent_id}"
        
        speech_record = {
            "speech_id": speech_id,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "speech_type": speech_type,
            "content": content,
            "stage": stage,
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
            "additional_data": additional_data or {}
        }
        
        # 存储到Redis时间线
        redis_client = await self._get_redis_client()
        if redis_client:
            try:
                # 使用有序集合存储时间线，按时间戳排序
                await redis_client.zadd(
                    self.timeline_key,
                    {speech_id: timestamp}
                )
                
                # 存储发言详情
                speech_key = f"{self.global_key_prefix}:speech:{speech_id}"
                await redis_client.hset(
                    speech_key,
                    mapping={
                        k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
                        for k, v in speech_record.items()
                    }
                )
                
                # 设置过期时间
                await redis_client.expire(speech_key, self._redis_settings.MEMORY_TTL)
                
                self.logger.debug(f"记录发言: {agent_name} - {speech_type}")
                
            except Exception as e:
                self.logger.error(f"记录发言到Redis失败: {str(e)}")
        
        return speech_id
    
    async def get_meeting_timeline(
        self,
        limit: int = 50,
        stage_filter: str = None,
        agent_filter: str = None
    ) -> List[Dict[str, Any]]:
        """
        获取会议时间线
        
        Args:
            limit: 最大返回数量
            stage_filter: 按阶段过滤
            agent_filter: 按智能体过滤
            
        Returns:
            按时间排序的发言记录列表
        """
        redis_client = await self._get_redis_client()
        if not redis_client:
            return []
        
        try:
            # 获取最近的发言ID（按时间戳倒序）
            speech_ids = await redis_client.zrevrange(
                self.timeline_key, 0, limit - 1
            )
            
            if not speech_ids:
                return []
            
            # 批量获取发言详情
            timeline = []
            for speech_id in speech_ids:
                speech_key = f"{self.global_key_prefix}:speech:{speech_id.decode()}"
                speech_data = await redis_client.hgetall(speech_key)
                
                if speech_data:
                    # 解码数据
                    decoded_speech = {}
                    for key, value in speech_data.items():
                        key_str = key.decode() if isinstance(key, bytes) else key
                        value_str = value.decode() if isinstance(value, bytes) else value
                        
                        # 尝试解析JSON
                        if key_str in ['additional_data']:
                            try:
                                decoded_speech[key_str] = json.loads(value_str)
                            except:
                                decoded_speech[key_str] = value_str
                        else:
                            decoded_speech[key_str] = value_str
                    
                    # 应用过滤器
                    if stage_filter and decoded_speech.get('stage') != stage_filter:
                        continue
                    if agent_filter and decoded_speech.get('agent_id') != agent_filter:
                        continue
                    
                    timeline.append(decoded_speech)
            
            return timeline
            
        except Exception as e:
            self.logger.error(f"获取会议时间线失败: {str(e)}")
            return []
    
    async def get_current_context(self, requesting_agent_id: str, max_context: int = 10) -> str:
        """
        获取当前会议上下文（供智能体参考）
        
        Args:
            requesting_agent_id: 请求上下文的智能体ID
            max_context: 最大上下文条数
            
        Returns:
            格式化的会议上下文文本
        """
        timeline = await self.get_meeting_timeline(limit=max_context)
        
        if not timeline:
            return "会议刚开始，暂无其他发言。"
        
        context_parts = []
        context_parts.append("=== 会议上下文 ===")
        
        for record in reversed(timeline):  # 按时间正序显示
            agent_name = record.get('agent_name', 'Unknown')
            speech_type = record.get('speech_type', 'unknown')
            content = record.get('content', '')
            stage = record.get('stage', 'unknown')
            
            # 跳过请求者自己的发言（避免重复）
            if record.get('agent_id') == requesting_agent_id:
                continue
            
            # 格式化发言
            if speech_type == 'introduction':
                context_parts.append(f"【{agent_name}】自我介绍: {content[:100]}...")
            elif speech_type == 'discussion':
                context_parts.append(f"【{agent_name}】讨论发言: {content[:150]}...")
            elif speech_type == 'keywords':
                context_parts.append(f"【{agent_name}】提取关键词: {content}")
            elif speech_type == 'voting':
                context_parts.append(f"【{agent_name}】投票: {content}")
            else:
                context_parts.append(f"【{agent_name}】{speech_type}: {content[:100]}...")
        
        if len(context_parts) == 1:  # 只有标题
            return "会议中其他参与者暂无相关发言。"
        
        return "\n".join(context_parts)
    
    async def get_stage_summary(self, stage: str) -> Dict[str, Any]:
        """
        获取特定阶段的总结
        
        Args:
            stage: 会议阶段
            
        Returns:
            阶段总结信息
        """
        stage_timeline = await self.get_meeting_timeline(
            limit=100, stage_filter=stage
        )
        
        summary = {
            "stage": stage,
            "speech_count": len(stage_timeline),
            "participants": set(),
            "speech_types": {},
            "start_time": None,
            "end_time": None
        }
        
        for record in stage_timeline:
            summary["participants"].add(record.get('agent_name', 'Unknown'))
            
            speech_type = record.get('speech_type', 'unknown')
            summary["speech_types"][speech_type] = summary["speech_types"].get(speech_type, 0) + 1
            
            timestamp = float(record.get('timestamp', 0))
            if summary["start_time"] is None or timestamp < summary["start_time"]:
                summary["start_time"] = timestamp
            if summary["end_time"] is None or timestamp > summary["end_time"]:
                summary["end_time"] = timestamp
        
        summary["participants"] = list(summary["participants"])
        return summary
    
    async def update_stage(self, new_stage: str) -> None:
        """
        更新会议阶段
        
        Args:
            new_stage: 新的会议阶段
        """
        self.current_stage = new_stage
        
        redis_client = await self._get_redis_client()
        if redis_client:
            try:
                await redis_client.hset(
                    self.stage_key,
                    mapping={
                        "current_stage": new_stage,
                        "update_time": str(time.time())
                    }
                )
                self.logger.info(f"会议阶段更新: {new_stage}")
            except Exception as e:
                self.logger.error(f"更新会议阶段失败: {str(e)}")
    
    async def clear_session(self) -> None:
        """清空会议会话数据"""
        redis_client = await self._get_redis_client()
        if redis_client:
            try:
                # 查找所有相关的key
                pattern = f"{self.global_key_prefix}:*"
                keys = []
                
                async for key in redis_client.scan_iter(match=pattern):
                    keys.append(key)
                
                if keys:
                    await redis_client.delete(*keys)
                
                self.logger.info(f"清空会议会话数据: {len(keys)} 个key")
                
            except Exception as e:
                self.logger.error(f"清空会议会话数据失败: {str(e)}")
    
    async def get_meeting_stats(self) -> Dict[str, Any]:
        """
        获取会议统计信息
        
        Returns:
            会议统计数据
        """
        timeline = await self.get_meeting_timeline(limit=1000)
        
        stats = {
            "session_id": self.session_id,
            "start_time": self.meeting_start_time,
            "current_stage": self.current_stage,
            "total_speeches": len(timeline),
            "participants_count": len(self.participants),
            "participants": list(self.participants),
            "speech_by_type": {},
            "speech_by_agent": {},
            "duration_minutes": (time.time() - self.meeting_start_time) / 60
        }
        
        for record in timeline:
            speech_type = record.get('speech_type', 'unknown')
            agent_name = record.get('agent_name', 'Unknown')
            
            stats["speech_by_type"][speech_type] = stats["speech_by_type"].get(speech_type, 0) + 1
            stats["speech_by_agent"][agent_name] = stats["speech_by_agent"].get(agent_name, 0) + 1
        
        return stats
