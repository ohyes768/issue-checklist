@echo off
chcp 65001 >nul
echo ========================================
echo   运维知识库智能排查助手 v1.1.0
echo ========================================
echo.
echo 正在启动应用...
echo.

REM 切换到项目根目录
cd /d "%~dp0.."

REM 检查虚拟环境
if not exist ".venv" (
    echo [1/4] 创建虚拟环境...
    python -m venv .venv
    if errorlevel 1 (
        echo 错误: 无法创建虚拟环境
        pause
        exit /b 1
    )
    echo        虚拟环境创建完成
) else (
    echo [1/4] 虚拟环境已存在
)

REM 激活虚拟环境
echo [2/4] 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 安装/更新依赖
echo [3/4] 检查依赖...
pip install -r requirements.txt -q

REM 创建日志目录
if not exist "logs" mkdir logs

REM 启动应用
echo [4/4] 启动 Web 应用...
echo.
echo ✅ 应用将在浏览器中打开: http://localhost:8501
echo 🛑 按 Ctrl+C 停止应用
echo.
echo ========================================
echo.

streamlit run main.py --server.headless false --server.port 8501

REM 停止后清理
call .venv\Scripts\deactivate.bat 2>nul
echo.
echo ========================================
echo   应用已停止
echo ========================================
pause
