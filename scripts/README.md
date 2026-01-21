# 启动脚本说明

本目录包含运维排查助手的启动脚本，统一使用虚拟环境运行。

## Windows 脚本

### 1. `start.bat` - 标准启动脚本（推荐）
**适用场景**: 首次使用或需要确保环境完整

**功能**:
- ✅ 自动创建虚拟环境（如果不存在）
- ✅ 自动激活虚拟环境
- ✅ 自动安装/更新依赖
- ✅ 自动创建 logs 目录
- ✅ 启动 Streamlit 应用

**使用方法**:
```cmd
scripts\start.bat
```

**特点**:
- 带进度提示（1/4、2/4...）
- 完整的环境检查
- 适合生产环境

---

### 2. `start_venv_auto.bat` - 自动虚拟环境启动
**适用场景**: 需要完整的虚拟环境管理

**功能**:
- 🔧 自动升级 pip
- 🔧 完整的依赖安装检查
- 🔧 详细的错误提示

**使用方法**:
```cmd
scripts\start_venv_auto.bat
```

---

### 4. `stop_app.bat` - 停止应用
**功能**:
- 🛑 停止所有 streamlit 进程
- 🛑 释放 8501 端口

**使用方法**:
```cmd
scripts\stop_app.bat
```

---

## Linux/Mac 脚本

### 1. `start.sh` - 标准启动脚本（推荐）
**使用方法**:
```bash
./scripts/start.sh
# 或
bash scripts/start.sh
```

功能同 Windows 的 `start.bat`

---

### 2. `stop_app.sh` - 停止应用
**使用方法**:
```bash
./scripts/stop_app.sh
# 或
bash scripts/stop_app.sh
```

---

## 脚本选择指南

| 场景 | 推荐脚本 | Windows | Linux/Mac |
|------|---------|---------|-----------|
| 首次使用 | 标准启动 | `start.bat` | `start.sh` |
| 日常开发 | 标准启动 | `start.bat` | `start.sh` |
| 生产部署 | 标准启动 | `start.bat` | `start.sh` |
| 环境管理 | 完整管理 | `start_venv_auto.bat` | - |
| 停止应用 | 停止脚本 | `stop_app.bat` | `stop_app.sh` |

> **说明**: 所有启动脚本都使用虚拟环境，确保依赖隔离和环境一致性。

---

## 启动后操作

1. **浏览器访问**: 应用会自动在浏览器中打开
   - 默认地址: http://localhost:8501
   - 如未自动打开，手动访问该地址

2. **停止应用**:
   - 方法1: 在命令行窗口按 `Ctrl + C`
   - 方法2: 运行停止脚本

3. **查看日志**:
   - 日志目录: `logs/`
   - 应用输出会显示在命令行窗口

---

## 常见问题

### Q: 脚本运行时提示"Python not found"
**A**: 请先安装 Python 3.8 或更高版本
- Windows: 从 python.org 下载安装
- Linux/Mac: 使用系统包管理器安装

### Q: 启动后浏览器无法访问
**A**: 检查防火墙设置或端口占用
```bash
# 检查8501端口是否被占用
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # Linux/Mac
```

### Q: 依赖安装失败
**A**: 尝试手动安装
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Q: 虚拟环境激活失败
**A**: 检查 Python 是否正确安装
```bash
python --version
python -m venv --help
```

---

## 高级用法

### 自定义端口
编辑脚本，修改端口号：
```bash
# 将 8501 改为其他端口
streamlit run main.py --server.port 8502
```

### 指定 host
```bash
# 允许局域网访问
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

### 开启调试模式
```bash
# 显示详细日志
streamlit run main.py --logger.level debug
```

---

## 更新日志

### v1.1.0 (2026-01-21)
- ✨ 新增 `start.bat` 和 `start.sh` 标准启动脚本
- ✨ 新增 `start_quick.bat` 和 `start_quick.sh` 快速启动脚本
- 🎨 优化脚本输出格式，添加版本信息
- 📝 添加本使用说明文档
