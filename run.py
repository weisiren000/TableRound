#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
启动脚本
"""

import os
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到系统路径
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(ROOT_DIR))

from src.main import main

if __name__ == "__main__":
    asyncio.run(main())
