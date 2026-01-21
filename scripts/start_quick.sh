#!/bin/bash

echo "🔥 运维排查助手 - 快速启动"
echo ""

# 切换到项目根目录
cd "$(dirname "$0")/.."

# 快速启动（使用系统Python，跳过依赖检查）
echo "正在启动应用..."
echo ""
echo "✅ 浏览器访问: http://localhost:8501"
echo "🛑 按 Ctrl+C 停止"
echo ""

streamlit run main.py --server.headless false --server.port 8501
