@echo off
REM Docker 镜像导出脚本 - Windows 本地打包
REM 用于将镜像打包后传输到 Linux 服务器部署

echo ========================================
echo Docker 镜像导出工具
echo ========================================

SET PROJECT_NAME=issue-checklist
SET VERSION=1.0.0
SET OUTPUT_DIR=.\docker-images

REM 创建输出目录
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo.
echo [1/3] 构建后端镜像...
docker build -f Dockerfile.backend -t %PROJECT_NAME%-backend:%VERSION% .
docker tag %PROJECT_NAME%-backend:%VERSION% %PROJECT_NAME%-backend:latest

echo.
echo [2/3] 构建前端镜像...
docker build -f Dockerfile.frontend -t %PROJECT_NAME%-frontend:%VERSION% .
docker tag %PROJECT_NAME%-frontend:%VERSION% %PROJECT_NAME%-frontend:latest

echo.
echo [3/3] 导出镜像到文件...
docker save %PROJECT_NAME%-backend:%VERSION% -o "%OUTPUT_DIR%\%PROJECT_NAME%-backend-%VERSION%.tar"
docker save %PROJECT_NAME%-frontend:%VERSION% -o "%OUTPUT_DIR%\%PROJECT_NAME%-frontend-%VERSION%.tar"

echo.
echo ========================================
echo 导出完成！
echo ========================================
echo.
echo 镜像文件位置: %OUTPUT_DIR%\
echo - %PROJECT_NAME%-backend-%VERSION%.tar
echo - %PROJECT_NAME%-frontend-%VERSION%.tar
echo.
echo 下一步:
echo 1. 将 docker-images 目录传输到 Linux 服务器
echo 2. 在 Linux 服务器上运行 load-images.sh 加载镜像
echo 3. 使用 docker-compose-linux.yml 启动服务
echo.

pause
