# Docker Compose 部署指南

本文档介绍如何使用 Docker Compose 部署运维知识库系统。

## 前置要求

- Docker Engine 20.10+
- Docker Compose 2.0+

## 快速开始

### 1. 构建并启动服务

```bash
# 构建镜像并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 2. 访问服务

- **前端**: http://localhost
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

### 3. 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除卷
docker-compose down -v
```

## 服务说明

### 后端服务 (backend)

- **端口**: 8000
- **容器名**: issue-checklist-backend
- **挂载目录**:
  - `./data:/app/data` - YAML 数据文件
  - `./logs:/app/logs` - 日志文件
- **健康检查**: 每 30 秒检查一次

### 前端服务 (frontend)

- **端口**: 80
- **容器名**: issue-checklist-frontend
- **依赖**: 后端服务
- **特性**: 静态文件由 Nginx 提供，API 请求代理到后端

## 数据持久化

### 更新 YAML 数据

直接修改 `./data` 目录下的 YAML 文件，然后调用 API 重新加载：

```bash
curl -X POST http://localhost:8000/api/reload
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 高级配置

### 自定义端口

修改 `docker-compose.yml` 中的端口映射：

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # 宿主机端口:容器端口

  frontend:
    ports:
      - "8080:80"
```

### 生产环境优化

1. **限制资源使用**:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

2. **使用外部网络**:

```yaml
networks:
  issue-checklist-network:
    external: true
```

3. **配置日志驱动**:

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 故障排查

### 容器启动失败

```bash
# 查看详细日志
docker-compose logs backend

# 进入容器调试
docker-compose exec backend bash
```

### 端口冲突

如果端口已被占用，修改 `docker-compose.yml` 中的端口映射。

### 数据无法加载

```bash
# 检查挂载目录
docker-compose exec backend ls -la /app/data

# 检查文件权限
docker-compose exec backend cat /app/data/*.yml
```

### 前端无法访问后端

- 检查网络连接: `docker network inspect issue-checklist_issue-checklist-network`
- 查看后端健康状态: `docker-compose ps`
- 检查 Nginx 配置: `docker-compose exec frontend cat /etc/nginx/conf.d/default.conf`

## 重新构建

```bash
# 重新构建特定服务
docker-compose build backend

# 重新构建所有服务
docker-compose build --no-cache

# 重新构建并启动
docker-compose up -d --build
```

## 备份与恢复

### 备份数据

```bash
# 备份数据目录
tar -czf data-backup-$(date +%Y%m%d).tar.gz ./data

# 备份日志
tar -czf logs-backup-$(date +%Y%m%d).tar.gz ./logs
```

### 恢复数据

```bash
# 解压数据备份
tar -xzf data-backup-20250211.tar.gz

# 重启服务
docker-compose restart backend
```

## 安全建议

1. **生产环境**: 修改默认端口，使用防火墙限制访问
2. **HTTPS**: 在 Nginx 前添加反向代理（如 Nginx、Traefik）配置 SSL
3. **认证**: 在后端添加身份认证中间件
4. **日志**: 定期清理日志文件，避免磁盘空间不足
