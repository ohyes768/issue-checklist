#!/bin/bash
# Docker 镜像加载脚本 - Linux 服务器部署
# 用于加载从 Windows 导出的 Docker 镜像

set -e

PROJECT_NAME="issue-checklist"
VERSION="1.0.0"
IMAGE_DIR="./docker-images"

echo "========================================"
echo "Docker 镜像加载工具"
echo "========================================"

# 检查镜像目录是否存在
if [ ! -d "$IMAGE_DIR" ]; then
    echo "错误: 找不到 docker-images 目录"
    echo "请先从 Windows 传输镜像文件到当前目录"
    exit 1
fi

# 查找镜像文件（支持 .tar 和 .tar.gz 格式）
BACKEND_FILE="$IMAGE_DIR/${PROJECT_NAME}-backend-${VERSION}.tar"
if [ ! -f "$BACKEND_FILE" ]; then
    BACKEND_FILE="$IMAGE_DIR/${PROJECT_NAME}-backend-${VERSION}.tar.gz"
fi

FRONTEND_FILE="$IMAGE_DIR/${PROJECT_NAME}-frontend-${VERSION}.tar"
if [ ! -f "$FRONTEND_FILE" ]; then
    FRONTEND_FILE="$IMAGE_DIR/${PROJECT_NAME}-frontend-${VERSION}.tar.gz"
fi

if [ ! -f "$BACKEND_FILE" ]; then
    echo "错误: 找不到后端镜像文件"
    echo "期望文件: ${PROJECT_NAME}-backend-${VERSION}.tar 或 .tar.gz"
    exit 1
fi

if [ ! -f "$FRONTEND_FILE" ]; then
    echo "错误: 找不到前端镜像文件"
    echo "期望文件: ${PROJECT_NAME}-frontend-${VERSION}.tar 或 .tar.gz"
    exit 1
fi

echo ""
echo "[1/3] 加载后端镜像: $BACKEND_FILE"
docker load -i "$BACKEND_FILE"

echo ""
echo "[2/3] 加载前端镜像: $FRONTEND_FILE"
docker load -i "$FRONTEND_FILE"

echo ""
echo "[3/3] 验证镜像..."
docker images | grep "$PROJECT_NAME"

echo ""
echo "========================================"
echo "镜像加载完成！"
echo "========================================"
echo ""
echo "下一步: 使用 docker-compose -f docker-compose-linux.yml up -d 启动服务"
echo ""

# 询问是否立即启动
read -p "是否立即启动服务? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "docker-compose-linux.yml" ]; then
        docker-compose -f docker-compose-linux.yml up -d
        echo ""
        echo "服务已启动！"
        echo "前端: http://$(hostname -I | awk '{print $1}')"
        echo "后端: http://$(hostname -I | awk '{print $1}'):8000"
    else
        echo "错误: 找不到 docker-compose-linux.yml 文件"
        exit 1
    fi
fi
