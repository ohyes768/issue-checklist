@echo off
chcp 65001 >nul
echo 🔥 运维排查助手 - 快速启动
echo.

cd /d "%~dp0.."

REM 快速启动（使用系统Python，跳过依赖检查）
echo 正在启动应用...
echo.
echo ✅ 浏览器访问: http://localhost:8501
echo 🛑 按 Ctrl+C 停止
echo.

streamlit run main.py --server.headless false --server.port 8501

pause
