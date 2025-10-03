#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TableRound 测试运行器
提供便捷的测试运行和管理功能
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd or project_root,
            capture_output=True, 
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def list_tests():
    """列出所有可用的测试"""
    print("可用的测试分类:")
    print("=" * 50)
    
    test_categories = {
        'api': 'API和模型测试',
        'memory': '记忆系统测试', 
        'integration': '系统集成测试',
        'features': '功能特性测试',
        'demos': '演示脚本',
        'unit': '单元测试（原有）'
    }
    
    for category, description in test_categories.items():
        print(f"{category:12} - {description}")
        
        if category == 'unit':
            # 原有的单元测试
            unit_tests = [
                'test_agents.py',
                'test_colors.py', 
                'test_conversation.py',
                'test_memory.py',
                'test_models.py',
                'test_role_playing.py'
            ]
            for test in unit_tests:
                test_path = project_root / 'tests' / test
                if test_path.exists():
                    print(f"             └── {test}")
        else:
            # 分类测试
            category_path = project_root / 'tests' / category
            if category_path.exists():
                for test_file in sorted(category_path.glob('*.py')):
                    if test_file.name != '__init__.py':
                        print(f"             └── {test_file.name}")
        print()

def run_category_tests(category):
    """运行指定分类的测试"""
    print(f"运行 {category} 分类测试...")
    print("=" * 50)
    
    if category == 'unit':
        # 运行原有的单元测试
        unit_tests = [
            'test_agents.py',
            'test_colors.py',
            'test_conversation.py', 
            'test_memory.py',
            'test_models.py',
            'test_role_playing.py'
        ]
        
        success_count = 0
        total_count = 0
        
        for test in unit_tests:
            test_path = project_root / 'tests' / test
            if test_path.exists():
                total_count += 1
                print(f"\n运行: {test}")
                print("-" * 30)
                
                success, stdout, stderr = run_command(f"python tests/{test}")
                if success:
                    print("✅ 通过")
                    success_count += 1
                else:
                    print("❌ 失败")
                    if stderr:
                        print(f"错误: {stderr}")
                        
        print(f"\n单元测试结果: {success_count}/{total_count} 通过")
        
    else:
        # 运行分类测试
        category_path = project_root / 'tests' / category
        if not category_path.exists():
            print(f"错误: 测试分类 '{category}' 不存在")
            return False
            
        test_files = list(category_path.glob('*.py'))
        test_files = [f for f in test_files if f.name != '__init__.py']
        
        if not test_files:
            print(f"警告: 分类 '{category}' 中没有找到测试文件")
            return True
            
        success_count = 0
        total_count = len(test_files)
        
        for test_file in sorted(test_files):
            print(f"\n运行: {test_file.name}")
            print("-" * 30)
            
            success, stdout, stderr = run_command(f"python tests/{category}/{test_file.name}")
            if success:
                print("✅ 通过")
                success_count += 1
            else:
                print("❌ 失败")
                if stderr:
                    print(f"错误: {stderr}")
                    
        print(f"\n{category} 测试结果: {success_count}/{total_count} 通过")
        return success_count == total_count

def run_single_test(test_path):
    """运行单个测试文件"""
    print(f"运行单个测试: {test_path}")
    print("=" * 50)
    
    full_path = project_root / test_path
    if not full_path.exists():
        print(f"错误: 测试文件 '{test_path}' 不存在")
        return False
        
    success, stdout, stderr = run_command(f"python {test_path}")
    if success:
        print("✅ 测试通过")
        if stdout:
            print(f"输出:\n{stdout}")
    else:
        print("❌ 测试失败")
        if stderr:
            print(f"错误:\n{stderr}")
        if stdout:
            print(f"输出:\n{stdout}")
            
    return success

def run_all_tests():
    """运行所有测试"""
    print("运行所有测试...")
    print("=" * 50)
    
    categories = ['api', 'memory', 'integration', 'features', 'unit']
    results = {}
    
    for category in categories:
        print(f"\n{'='*20} {category.upper()} {'='*20}")
        results[category] = run_category_tests(category)
    
    # 总结
    print("\n" + "="*50)
    print("测试总结:")
    print("="*50)
    
    for category, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{category:12} - {status}")
    
    all_passed = all(results.values())
    print(f"\n整体结果: {'✅ 所有测试通过' if all_passed else '❌ 部分测试失败'}")
    
    return all_passed

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='TableRound 测试运行器')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有可用测试')
    parser.add_argument('--category', '-c', help='运行指定分类的测试 (api/memory/integration/features/unit)')
    parser.add_argument('--test', '-t', help='运行单个测试文件')
    parser.add_argument('--all', '-a', action='store_true', help='运行所有测试')
    
    args = parser.parse_args()
    
    if args.list:
        list_tests()
    elif args.category:
        run_category_tests(args.category)
    elif args.test:
        run_single_test(args.test)
    elif args.all:
        run_all_tests()
    else:
        print("TableRound 测试运行器")
        print("使用 --help 查看可用选项")
        print("\n快速开始:")
        print("  python tests/run_tests.py --list          # 列出所有测试")
        print("  python tests/run_tests.py --all           # 运行所有测试")
        print("  python tests/run_tests.py -c api          # 运行API测试")
        print("  python tests/run_tests.py -t tests/api/test_doubao_watermark.py  # 运行单个测试")

if __name__ == "__main__":
    main()
