@echo off
echo Stopping O&M Assistant...

REM Find and kill streamlit processes
taskkill /f /im streamlit.exe 2>nul
if errorlevel 1 (
    echo No streamlit processes found
) else (
    echo Streamlit processes stopped
)

REM Optional: Kill Python processes using port 8501
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501') do (
    echo Killing process %%a using port 8501
    taskkill /f /pid %%a 2>nul
)

echo O&M Assistant stopped
pause