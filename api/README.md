# 运维知识库 FastAPI 后端

提供运维排查知识库的 RESTful API 接口，供 React 前端调用。

## 安装依赖

由于网络问题，需要手动安装 FastAPI 和 uvicorn：

```bash
# 方法1: 使用 uv（推荐）
uv pip install fastapi uvicorn

# 方法2: 使用 pip
pip install fastapi uvicorn

# 方法3: 使用项目脚本
bash api/install_dependencies.sh
```

## 启动 API 服务器

### 开发模式（推荐）

```bash
# 使用 uvicorn 直接启动（支持热重载）
uvicorn api.main:app --reload --port 8000

# 或者使用 uv run
uv run uvicorn api.main:app --reload --port 8000

# 或者直接运行 Python 文件
python api/main.py
```

### 生产模式

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API 文档

启动服务器后，访问以下地址查看交互式 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API 端点

### 1. 根路径

```
GET /
```

返回 API 欢迎信息和端点列表。

### 2. 获取问题列表

```
GET /api/issues
```

返回所有 `display=True` 的问题列表（按优先级降序排列）。

**响应示例**：
```json
{
  "issues": [
    "数据查询响应慢",
    "数据同步失败",
    "任务调度异常",
    ...
  ],
  "total": 29
}
```

### 3. 获取问题树形结构

```
GET /api/issues/{issue_name}/tree
```

获取指定问题的完整树形结构（包含 refer 引用解析）。

**路径参数**：
- `issue_name`: 问题名称（需要 URL 编码）

**响应示例**：
```json
{
  "id": "数据查询响应慢",
  "title": "数据查询响应慢",
  "describe": "观察用户查询请求的响应时间...",
  "version": "v3.0+",
  "priority": 9,
  "sourceFile": "issue-1",
  "originalPath": ["数据查询响应慢"],
  "isRefer": false,
  "howToCheck": {
    "description": "...",
    "knowledgeLinks": [...],
    "gifGuides": [...],
    "scriptLinks": [...]
  },
  "fixSteps": {
    "description": "...",
    "knowledgeLinks": [...],
    "gifGuides": [...],
    "scriptLinks": [...]
  },
  "subCheckItems": [...]
}
```

### 4. 重新加载数据

```
POST /api/reload
```

重新加载 YAML 数据文件（用于更新数据后刷新，无需重启服务）。

**响应示例**：
```json
{
  "success": true,
  "message": "数据重新加载成功",
  "stats": {
    "total_issues": 29,
    "total_checklists": 156,
    "avg_checklists_per_issue": 5.38
  }
}
```

### 5. 获取统计信息

```
GET /api/stats
```

获取数据统计信息。

**响应示例**：
```json
{
  "total_issues": 29,
  "total_checklists": 156,
  "avg_checklists_per_issue": 5.38
}
```

## 测试 API

使用提供的测试脚本：

```bash
# 1. 确保已安装 requests 库
uv pip install requests

# 2. 启动 API 服务器
uv run uvicorn api.main:app --reload --port 8000

# 3. 在另一个终端运行测试脚本
python api/test_api.py
```

## CORS 配置

API 已配置 CORS，允许以下来源访问：

- `http://localhost:5173`（Vite 开发服务器默认端口）
- `http://localhost:3000`（备用端口）

如需添加其他域名，请修改 `api/main.py` 中的 `allow_origins` 配置。

## 项目结构

```
api/
├── __init__.py          # 包初始化
├── main.py              # FastAPI 应用入口
├── serializers.py       # 数据序列化器
├── install_dependencies.sh  # 依赖安装脚本
├── test_api.py          # API 测试脚本
└── README.md            # 本文档
```

## 数据流程

1. **数据加载**: `DataLoader` 从 `data/` 目录加载 YAML 文件
2. **树构建**: `TreeBuilder` 构建树形结构并处理 refer 引用
3. **数据序列化**: `tree_node_to_dict()` 将 Python 对象转换为 JSON
4. **API 响应**: FastAPI 自动序列化为 JSON 响应

## 错误处理

API 使用标准 HTTP 状态码：

- `200` - 成功
- `404` - 资源不存在
- `500` - 服务器内部错误

错误响应格式：
```json
{
  "detail": "错误描述信息"
}
```

## 生产部署建议

1. **使用 Gunicorn + Uvicorn**:
   ```bash
   gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```

2. **使用 Docker**:
   ```dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY . .
   RUN pip install fastapi uvicorn
   CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **使用 systemd**:
   ```ini
   [Unit]
   Description=运维知识库 API
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/issue-checklist
   ExecStart=/usr/local/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

## 故障排查

### 问题: 端口被占用

```
Error: [Errno 48] Address already in use
```

**解决方案**: 更换端口或杀死占用进程
```bash
# 更换端口
uvicorn api.main:app --port 8001

# 查找并杀死进程（Linux/Mac）
lsof -ti:8000 | xargs kill -9
```

### 问题: CORS 错误

浏览器控制台显示：
```
Access to XMLHttpRequest at 'http://localhost:8000/...' has been blocked by CORS policy
```

**解决方案**: 检查 `api/main.py` 中的 CORS 配置，确保前端地址在 `allow_origins` 中。

### 问题: 数据加载失败

```
错误: 未找到问题 'xxx'
```

**解决方案**:
1. 检查 `data/` 目录是否存在
2. 检查 YAML 文件格式是否正确
3. 查看服务器日志获取详细错误信息

## 开发建议

1. **使用热重载**: 开发时使用 `--reload` 参数，代码修改自动重启
2. **查看日志**: API 会在控制台输出详细的加载和错误信息
3. **使用 API 文档**: Swagger UI 提供交互式测试界面
4. **数据验证**: 修改 YAML 文件后，使用 `POST /api/reload` 重新加载

## 联系方式

如有问题，请联系开发团队或提交 Issue。
