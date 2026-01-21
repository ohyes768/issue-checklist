#!/bin/bash

echo "========================================"
echo "  运维知识库智能排查助手 v1.1.0"
echo "========================================"
echo ""
echo "正在启动应用..."
echo ""

# 切换到项目根目录
cd "$(dirname "$0")/.."

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "[1/4] 创建虚拟环境..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "错误: 无法创建虚拟环境"
        exit 1
    fi
    echo "       虚拟环境创建完成"
else
    echo "[1/4] 虚拟环境已存在"
fi

# 激活虚拟环境
echo "[2/4] 激活虚拟环境..."
source .venv/bin/activate

# 安装/更新依赖
echo "[3/4] 检查依赖..."
pip install -r requirements.txt -q

# 创建日志目录
if [ ! -d "logs" ]; then
    mkdir logs
fi

# 启动应用
echo "[4/4] 启动 Web 应用..."
echo ""
echo "✅ 应用将在浏览器中打开: http://localhost:8501"
echo "🛑 按 Ctrl+C 停止应用"
echo ""
echo "========================================"
echo ""

streamlit run main.py --server.headless false --server.port 8501

# 停止后清理
deactivate 2>/dev/null
echo ""
echo "========================================"
echo "  应用已停止"
echo "========================================"
