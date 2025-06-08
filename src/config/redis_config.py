#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Redis配置模块
"""

import os
from typing import Optional
import redis.asyncio as redis
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class RedisSettings(BaseSettings):
    """Redis配置"""

    # Redis连接配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_USERNAME: Optional[str] = None

    # 连接池配置
    REDIS_MAX_CONNECTIONS: int = 20
    REDIS_RETRY_ON_TIMEOUT: bool = True
    REDIS_SOCKET_TIMEOUT: float = 5.0
    REDIS_SOCKET_CONNECT_TIMEOUT: float = 5.0

    # 记忆模块配置
    MEMORY_MAX_SIZE: int = 1000  # 每个agent最大记忆数量
    MEMORY_TTL: int = 86400 * 7  # 记忆过期时间（7天）

    # 启用/禁用Redis
    ENABLE_REDIS: bool = True

    class Config:
        env_file = ".env"
        env_prefix = ""
        extra = "ignore"  # 忽略额外的环境变量


class RedisManager:
    """Redis连接管理器"""
    
    def __init__(self, settings: RedisSettings = None):
        self.settings = settings or RedisSettings()
        self._client: Optional[redis.Redis] = None
        self._connection_pool: Optional[redis.ConnectionPool] = None
    
    async def get_client(self) -> redis.Redis:
        """
        获取Redis客户端
        
        Returns:
            Redis客户端实例
        """
        if not self.settings.ENABLE_REDIS:
            raise RuntimeError("Redis未启用")
        
        if self._client is None:
            await self._create_client()
        
        return self._client
    
    async def _create_client(self) -> None:
        """创建Redis客户端"""
        try:
            # 创建连接池
            self._connection_pool = redis.ConnectionPool(
                host=self.settings.REDIS_HOST,
                port=self.settings.REDIS_PORT,
                db=self.settings.REDIS_DB,
                password=self.settings.REDIS_PASSWORD,
                username=self.settings.REDIS_USERNAME,
                max_connections=self.settings.REDIS_MAX_CONNECTIONS,
                retry_on_timeout=self.settings.REDIS_RETRY_ON_TIMEOUT,
                socket_timeout=self.settings.REDIS_SOCKET_TIMEOUT,
                socket_connect_timeout=self.settings.REDIS_SOCKET_CONNECT_TIMEOUT,
                decode_responses=False  # 保持字节格式，手动处理编码
            )
            
            # 创建客户端
            self._client = redis.Redis(connection_pool=self._connection_pool)
            
            # 测试连接
            await self._client.ping()
            print(f"✅ Redis连接成功: {self.settings.REDIS_HOST}:{self.settings.REDIS_PORT}")
            
        except Exception as e:
            print(f"❌ Redis连接失败: {str(e)}")
            raise
    
    async def close(self) -> None:
        """关闭Redis连接"""
        if self._client:
            await self._client.close()
            self._client = None
        
        if self._connection_pool:
            await self._connection_pool.disconnect()
            self._connection_pool = None
    
    async def health_check(self) -> bool:
        """
        健康检查
        
        Returns:
            连接是否正常
        """
        try:
            if not self._client:
                return False
            
            await self._client.ping()
            return True
        except:
            return False
    
    async def get_info(self) -> dict:
        """
        获取Redis服务器信息
        
        Returns:
            服务器信息字典
        """
        try:
            client = await self.get_client()
            info = await client.info()
            return info
        except Exception as e:
            return {"error": str(e)}
    
    async def clear_all_agent_data(self) -> int:
        """
        清空所有agent数据（危险操作，仅用于测试）
        
        Returns:
            删除的key数量
        """
        try:
            client = await self.get_client()
            
            # 查找所有agent相关的key
            keys = []
            async for key in client.scan_iter(match="agent:*"):
                keys.append(key)
            
            if keys:
                deleted_count = await client.delete(*keys)
                return deleted_count
            
            return 0
            
        except Exception as e:
            print(f"清空数据失败: {str(e)}")
            return 0


# 全局Redis管理器实例
redis_manager = RedisManager()


async def get_redis_client() -> redis.Redis:
    """
    获取Redis客户端的便捷函数
    
    Returns:
        Redis客户端实例
    """
    return await redis_manager.get_client()


async def init_redis() -> None:
    """初始化Redis连接"""
    try:
        await redis_manager.get_client()
    except Exception as e:
        print(f"Redis初始化失败: {str(e)}")
        raise


async def close_redis() -> None:
    """关闭Redis连接"""
    await redis_manager.close()
