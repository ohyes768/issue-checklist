#!/bin/bash
# 安装 FastAPI 依赖脚本

echo "正在安装 FastAPI 和 uvicorn..."

# 使用 uv 安装
uv pip install fastapi uvicorn

echo "安装完成！"
echo ""
echo "启动 API 服务器："
echo "  uv run uvicorn api.main:app --reload --port 8000"
echo ""
echo "或者直接运行："
echo "  python api/main.py"
