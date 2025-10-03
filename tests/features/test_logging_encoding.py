#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试日志编码修复
验证中文日志能够正确写入和读取
"""

import os
import sys
import tempfile
import logging
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.logger import setup_logger


def test_logging_encoding():
    """测试日志编码"""
    print("=== 测试日志编码修复 ===")
    
    # 创建临时日志文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_log_file = temp_file.name
    
    try:
        # 设置日志记录器
        setup_logger(
            level=logging.INFO,
            log_file=temp_log_file,
            log_to_console=False
        )
        
        # 获取日志记录器
        logger = logging.getLogger("test_encoding")
        
        # 测试中文日志消息
        test_messages = [
            "启动圆桌会议系统",
            "Redis连接初始化成功", 
            "创建智能体: 手工艺人1 (craftsman)",
            "创建智能体: 消费者1 (consumer)",
            "创建智能体: 制造商1 (manufacturer)",
            "创建智能体: 设计师1 (designer)",
            "智能体 手工艺人1 正在根据图片讲故事",
            "智能体 消费者1 提取到 5 个关键词",
            "处理图片完成",
            "圆桌会议系统正常退出"
        ]
        
        print(f"写入测试日志到: {temp_log_file}")
        
        # 写入测试消息
        for i, message in enumerate(test_messages, 1):
            logger.info(f"{message}")
            print(f"  {i:2d}. {message}")
        
        # 强制刷新日志
        for handler in logger.handlers:
            handler.flush()
        
        # 读取日志文件验证编码
        print(f"\n从日志文件读取内容:")
        print("-" * 50)
        
        success = True
        
        try:
            with open(temp_log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
                
            # 检查是否包含测试消息
            for message in test_messages:
                if message in log_content:
                    print(f"找到: {message}")
                else:
                    print(f"缺失: {message}")
                    success = False
            
            # 检查是否有乱码
            lines = log_content.split('\n')
            for line_num, line in enumerate(lines, 1):
                if line.strip():
                    # 检查是否包含乱码字符
                    if '�' in line or any(ord(c) > 65535 for c in line if c.isprintable()):
                        print(f"第{line_num}行发现乱码: {line}")
                        success = False
            
            if success:
                print("\n日志编码测试通过 - 所有中文字符正确显示")
            else:
                print("\n日志编码测试失败 - 发现乱码或缺失内容")
                
        except UnicodeDecodeError as e:
            print(f"UTF-8解码失败: {e}")
            success = False

            # 尝试用其他编码读取
            try:
                with open(temp_log_file, 'r', encoding='gbk') as f:
                    content = f.read()
                print("文件使用了GBK编码而非UTF-8")
            except:
                print("无法用GBK编码读取文件")
        
        return success
        
    finally:
        # 清理临时文件
        try:
            os.unlink(temp_log_file)
        except:
            pass


def test_file_handler_encoding():
    """测试文件处理器编码设置"""
    print("\n=== 测试文件处理器编码设置 ===")
    
    from logging.handlers import RotatingFileHandler
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_log_file = temp_file.name
    
    try:
        # 创建文件处理器
        file_handler = RotatingFileHandler(
            temp_log_file,
            maxBytes=1024,
            backupCount=2,
            encoding='utf-8'
        )
        
        # 检查编码设置
        if hasattr(file_handler, 'encoding'):
            encoding = file_handler.encoding
            print(f"文件处理器编码: {encoding}")
            
            if encoding == 'utf-8':
                print("文件处理器编码设置正确")
                return True
            else:
                print(f"文件处理器编码设置错误: {encoding}")
                return False
        else:
            print("文件处理器没有编码属性")
            return False
            
    finally:
        try:
            os.unlink(temp_log_file)
        except:
            pass


def test_logger_setup():
    """测试日志设置函数"""
    print("\n=== 测试日志设置函数 ===")
    
    # 创建临时日志文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_log_file = temp_file.name
    
    try:
        # 测试setup_logger函数
        logger = setup_logger(
            level=logging.INFO,
            log_file=temp_log_file,
            log_to_console=False
        )
        
        # 检查文件处理器
        file_handlers = [h for h in logger.handlers if hasattr(h, 'baseFilename')]
        
        if file_handlers:
            file_handler = file_handlers[0]
            if hasattr(file_handler, 'encoding') and file_handler.encoding == 'utf-8':
                print("setup_logger创建的文件处理器编码正确")
                return True
            else:
                print(f"setup_logger创建的文件处理器编码错误: {getattr(file_handler, 'encoding', 'None')}")
                return False
        else:
            print("setup_logger没有创建文件处理器")
            return False
            
    finally:
        try:
            os.unlink(temp_log_file)
        except:
            pass


def main():
    """主测试函数"""
    print("开始测试日志编码修复...\n")
    
    # 测试结果
    results = {}
    
    # 1. 测试文件处理器编码设置
    results["file_handler_encoding"] = test_file_handler_encoding()
    
    # 2. 测试日志设置函数
    results["logger_setup"] = test_logger_setup()
    
    # 3. 测试日志编码
    results["logging_encoding"] = test_logging_encoding()
    
    # 总结结果
    print("\n" + "="*60)
    print("测试结果总结:")
    print("="*60)
    
    for test_name, success in results.items():
        status = "通过" if success else "失败"
        print(f"{test_name:20} - {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\n总体结果: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("所有日志编码测试通过！")
        return True
    else:
        print("部分日志编码测试失败")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
