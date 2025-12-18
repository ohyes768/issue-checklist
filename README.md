# 运维知识库智能排查助手

基于Streamlit构建的运维知识库智能排查助手，帮助运维人员快速定位和解决问题。

## 项目结构

```
checklist-2/
├── data/                           # YAML数据文件目录
│   ├── kafka节点离线.yml
│   ├── yarn节点异常.yml
│   └── 日志引擎启动异常.yml
├── src/                            # 源代码目录
│   ├── models/                     # 数据模型
│   │   └── checklist.py
│   ├── utils/                      # 工具类
│   │   ├── data_loader.py
│   │   └── tree_builder.py
│   ├── controllers/                # 控制器
│   │   ├── state_manager.py
│   │   └── web_controller.py
│   └── main_app.py                # 主应用
├── scripts/                        # 启动脚本
│   ├── start_web.bat
│   └── start_web.sh
├── docs/                          # 文档目录
├── main.py                        # 入口文件
└── requirements.txt               # 依赖文件
```

## 功能特性

- **智能排查流程**: 基于YAML配置的树形排查逻辑
- **refer引用支持**: 支持问题间的相互引用
- **优先级排序**: 按优先级自动排序检查项
- **实时状态跟踪**: 显示当前排查路径和进度
- **直观界面**: 所有检查项直接显示，无需展开
- **视觉反馈**: 排除项目带删除线效果
- **动态详情**: 实时显示当前检查项的详细信息
- **Web界面**: 基于Streamlit的现代化Web界面

## 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 或使用uv（推荐）
uv pip install -r requirements.txt
```

## 启动应用

### 推荐方式：使用虚拟环境（venv）

#### Windows
```bash
# 使用venv启动脚本（自动创建虚拟环境）
scripts/start_venv_auto.bat
```

#### Linux/Mac
```bash
# 使用venv启动脚本（自动创建虚拟环境）
./scripts/start_venv.sh
```

### 快速启动方式：使用全局Python

#### Windows
```bash
# 使用批处理脚本
scripts/start_web.bat

# 或直接启动
streamlit run main.py
```

#### Linux/Mac
```bash
# 使用shell脚本
chmod +x scripts/start_web.sh
./scripts/start_web.sh

# 或直接启动
streamlit run main.py
```

### 手动使用venv

如果需要手动管理虚拟环境：

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动应用
streamlit run main.py

# 停用虚拟环境
deactivate
```

应用启动后会在浏览器中打开: http://localhost:8501

### 停止应用

#### 方法1：快捷键停止（推荐）
在运行应用的命令行窗口中按下 `Ctrl + C`

#### 方法2：关闭窗口
直接关闭运行应用的命令行窗口

#### 方法3：使用停止脚本
```bash
# Windows
scripts/stop_app.bat

# Linux/Mac
./scripts/stop_app.sh
```

## 使用说明

1. **选择问题**: 从顶部下拉框选择要排查的问题现象
2. **查看详情**: 右上区域显示当前检查项的详细信息
3. **导航路径**: 左上角显示完整的排查路径和当前位置
4. **确认检查项**: 在右下区域直接查看所有检查项，逐项确认或排除
5. **获取解决方案**: 确认后自动显示具体的解决方案和操作步骤
6. **快捷操作**: 使用顶部工具栏的重置和首页按钮快速导航

## YAML数据格式

每个YAML文件包含一个问题的完整排查流程：

```yaml
status: "问题标题"
describe: "问题描述"
priority: 10  # 优先级(1-10)
version: "影响版本范围"
checklist:
  - status: "直接原因现象"
    describe: "详细说明和确认方法"
    priority: 8
    version: "版本范围"
    todo: "解决方案描述"
    checklist:  # 子检查项（可选）
      - status: "子现象"
        describe: "子描述"
        priority: 5
        version: "-"
        todo: "子解决方案"
  - status: "另一个直接原因"
    refer: "其他问题标题"  # 引用其他问题（可选）
```

## 开发规范

- 使用强类型数据结构
- 每个文件不超过300行
- 遵循模块化设计原则
- 详细的错误处理和日志记录

## 技术栈

- **Python 3.8+**
- **Streamlit**: Web框架
- **PyYAML**: YAML解析
- **Pandas**: 数据处理

## 版本信息

- 版本: 1.0.0
- 基于: Claude Code 生成