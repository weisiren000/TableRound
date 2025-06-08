#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主程序入口
"""

import os
import sys
import asyncio
import logging
import argparse
from pathlib import Path

# 添加项目根目录到系统路径
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT_DIR))

from src.config.settings import Settings
from src.core.conversation import ConversationManager
from src.core.god_view import GodView
from src.utils.logger import setup_logger
from ui.cli.terminal import start_cli


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="圆桌会议系统")
    
    parser.add_argument(
        "--config", 
        type=str, 
        default=".env",
        help="配置文件路径"
    )
    
    parser.add_argument(
        "--log-level", 
        type=str, 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="日志级别"
    )
    
    parser.add_argument(
        "--log-file", 
        type=str, 
        default=None,
        help="日志文件路径"
    )
    
    parser.add_argument(
        "--no-console-log", 
        action="store_true",
        help="不输出日志到控制台"
    )
    
    return parser.parse_args()


async def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志
    log_level = getattr(logging, args.log_level)
    log_file = args.log_file or os.path.join(ROOT_DIR, "logs", "app.log")
    log_to_console = not args.no_console_log
    
    setup_logger(
        level=log_level,
        log_file=log_file,
        log_to_console=log_to_console
    )
    
    logger = logging.getLogger("main")
    logger.info("启动圆桌会议系统")
    
    try:
        # 加载设置
        settings = Settings(args.config)

        # 初始化Redis连接（如果启用）
        try:
            from src.config.redis_config import init_redis
            await init_redis()
            logger.info("Redis连接初始化成功")
        except Exception as e:
            logger.warning(f"Redis连接初始化失败，将使用文件存储: {str(e)}")

        # 创建上帝视角
        god_view = GodView(settings)

        # 创建对话管理器
        conversation_manager = ConversationManager(god_view, settings)

        # 启动命令行界面
        await start_cli(conversation_manager, settings)
        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        # 关闭Redis连接
        try:
            from src.config.redis_config import close_redis
            await close_redis()
            logger.info("Redis连接已关闭")
        except Exception as e:
            logger.debug(f"关闭Redis连接时出错: {str(e)}")

    logger.info("圆桌会议系统正常退出")


if __name__ == "__main__":
    asyncio.run(main())
