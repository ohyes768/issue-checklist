# Windows 打包镜像 + Linux 服务器部署指南

本文档介绍如何在 Windows 本地构建 Docker 镜像，然后部署到 Linux 服务器。

## 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **方案一：直接导出** | 简单快速 | 可能存在平台兼容性问题 | Windows 和 Linux 架构相同 |
| **方案二：多平台构建** | 兼容性好，支持多种架构 | 构建时间较长 | 生产环境推荐 |

---

## 方案一：直接导出镜像（简单快速）

### Windows 端 - 导出镜像

```batch
# 方式1：使用脚本（推荐）
scripts\export-images.bat

# 方式2：手动执行
docker build -f Dockerfile.backend -t issue-checklist-backend:1.0.0 .
docker build -f Dockerfile.frontend -t issue-checklist-frontend:1.0.0 .

docker save issue-checklist-backend:1.0.0 -o docker-images/backend.tar
docker save issue-checklist-frontend:1.0.0 -o docker-images/frontend.tar
```

### 传输镜像到 Linux

```bash
# 使用 scp 传输
scp -r docker-images/ user@your-server:/opt/issue-checklist/

# 或使用其他方式（FTP、U盘等）
```

### Linux 端 - 加载并运行

```bash
# 1. 解压并加载镜像
cd /opt/issue-checklist
chmod +x scripts/load-images.sh
./scripts/load-images.sh

# 2. 启动服务
docker-compose -f docker-compose-linux.yml up -d

# 3. 查看状态
docker-compose -f docker-compose-linux.yml ps
```

---

## 方案二：多平台镜像构建（推荐）

### Windows 端 - 构建多平台镜像

```bash
# 使用 Git Bash 或 WSL 运行
bash scripts/export-images.sh
```

这会构建支持 AMD64 和 ARM64 的镜像，兼容性更好。

### Linux 端 - 加载并运行

```bash
# 1. 解压镜像
cd /opt/issue-checklist/docker-images
tar -xzf issue-checklist-backend-1.0.0.tar.gz
tar -xzf issue-checklist-frontend-1.0.0.tar.gz

# 2. 加载镜像
docker load -i backend/images/amd64/issue-checklist-backend.tar  # AMD64
# 或
docker load -i backend/images/arm64/issue-checklist-backend.tar  # ARM64

# 3. 启动服务
docker-compose -f docker-compose-linux.yml up -d
```

---

## 完整部署流程（方案一示例）

### 1. Windows 端准备

```batch
# 1. 构建并导出镜像
cd F:\dbapp\issue-checklist
scripts\export-images.bat

# 2. 传输文件（使用 scp、FTP 或其他方式）
scp -r docker-images/ root@192.168.1.100:/opt/issue-checklist/
scp docker-compose-linux.yml root@192.168.1.100:/opt/issue-checklist/
scp -r data/ root@192.168.1.100:/opt/issue-checklist/
```

### 2. Linux 端部署

```bash
# 1. 安装 Docker 和 Docker Compose（如果未安装）
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 2. 创建目录并上传文件
mkdir -p /opt/issue-checklist
cd /opt/issue-checklist

# 上传文件后...

# 3. 加载镜像
chmod +x scripts/load-images.sh
./scripts/load-images.sh

# 4. 启动服务
docker-compose -f docker-compose-linux.yml up -d

# 5. 设置开机自启
docker-compose -f docker-compose-linux.yml update
```

### 3. 验证部署

```bash
# 查看容器状态
docker-compose -f docker-compose-linux.yml ps

# 查看日志
docker-compose -f docker-compose-linux.yml logs -f

# 测试访问
curl http://localhost:8000/api/issues
```

---

## 配置防火墙

```bash
# CentOS/RHEL
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --permanent --add-port=8000/tcp
firewall-cmd --reload

# Ubuntu/Debian
ufw allow 80/tcp
ufw allow 8000/tcp
ufw reload
```

---

## 常见问题

### 1. 架构不匹配

**问题**: Windows 是 x86_64，Linux 服务器是 ARM64（如国产服务器）

**解决**: 使用方案二的多平台构建

```bash
# 检查镜像架构
docker inspect issue-checklist-backend:latest | grep Architecture
```

### 2. 镜像加载失败

**问题**: `Error loading image`

**解决**:
```bash
# 检查文件完整性
md5sum backend.tar

# 重新传输（使用二进制模式）
# FTP 客户端确保使用 BINARY 模式
```

### 3. 容器启动失败

**问题**: 容器无法启动

**解决**:
```bash
# 查看详细日志
docker-compose -f docker-compose-linux.yml logs backend

# 进入容器调试
docker-compose -f docker-compose-linux.yml run --rm backend bash
```

---

## 更新部署

```bash
# 1. Windows 端重新构建并导出
scripts\export-images.bat

# 2. 传输到 Linux
scp docker-images/*.tar root@your-server:/opt/issue-checklist/docker-images/

# 3. Linux 端更新
cd /opt/issue-checklist

# 停止服务
docker-compose -f docker-compose-linux.yml down

# 加载新镜像
docker load -i docker-images/backend.tar
docker load -i docker-images/frontend.tar

# 重启服务
docker-compose -f docker-compose-linux.yml up -d
```

---

## 备份与恢复

```bash
# 备份
tar -czf issue-checklist-backup-$(date +%Y%m%d).tar.gz \
    data/ logs/ docker-compose-linux.yml

# 恢复
tar -xzf issue-checklist-backup-20250211.tar.gz
docker-compose -f docker-compose-linux.yml up -d
```
