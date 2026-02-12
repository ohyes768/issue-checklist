#!/bin/bash
# Docker 镜像导出脚本 - 使用 buildx 构建多平台镜像（推荐）
# 可以在 Windows/Mac/Linux 上构建，部署到 Linux 服务器

set -e

PROJECT_NAME="issue-checklist"
VERSION="1.0.0"
OUTPUT_DIR="./docker-images"
PLATFORMS="linux/amd64,linux/arm64"  # 支持 AMD64 和 ARM64 架构

echo "========================================"
echo "Docker 多平台镜像构建工具"
echo "========================================"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo ""
echo "检查 buildx 支持..."
if ! docker buildx version &> /dev/null; then
    echo "错误: docker buildx 未安装或未启用"
    echo "请升级 Docker 到最新版本"
    exit 1
fi

# 创建并使用 buildx 构建器
echo ""
echo "创建 buildx 构建器..."
docker buildx create --name multiarch-builder --use --bootstrap 2>/dev/null || true

echo ""
echo "[1/2] 构建并导出后端镜像..."
docker buildx build \
    --platform "$PLATFORMS" \
    -f Dockerfile.backend \
    -t "${PROJECT_NAME}-backend:${VERSION}" \
    -t "${PROJECT_NAME}-backend:latest" \
    --output type=local,dest="$OUTPUT_DIR/backend" \
    .

# 将构建结果打包为 tar
cd "$OUTPUT_DIR"
tar -czf "${PROJECT_NAME}-backend-${VERSION}.tar.gz" backend
rm -rf backend
cd ..

echo ""
echo "[2/2] 构建并导出前端镜像..."
docker buildx build \
    --platform "$PLATFORMS" \
    -f Dockerfile.frontend \
    -t "${PROJECT_NAME}-frontend:${VERSION}" \
    -t "${PROJECT_NAME}-frontend:latest" \
    --output type=local,dest="$OUTPUT_DIR/frontend" \
    .

# 将构建结果打包为 tar
cd "$OUTPUT_DIR"
tar -czf "${PROJECT_NAME}-frontend-${VERSION}.tar.gz" frontend
rm -rf frontend
cd ..

echo ""
echo "========================================"
echo "多平台镜像构建完成！"
echo "========================================"
echo ""
echo "支持的平台: $PLATFORMS"
echo "镜像文件位置: $OUTPUT_DIR/"
echo " - ${PROJECT_NAME}-backend-${VERSION}.tar.gz"
echo " - ${PROJECT_NAME}-frontend-${VERSION}.tar.gz"
echo ""
echo "下一步:"
echo "1. 将 docker-images 目录传输到 Linux 服务器"
echo "2. 在 Linux 服务器上解压并加载镜像"
echo "3. 使用 docker-compose-linux.yml 启动服务"
echo ""
