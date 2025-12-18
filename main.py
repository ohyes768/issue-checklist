#!/usr/bin/env python3
"""
运维知识库智能排查助手 - Streamlit Web版本
主入口文件
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.main_app import main

if __name__ == "__main__":
    main()