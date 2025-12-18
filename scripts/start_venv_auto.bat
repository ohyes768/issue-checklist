@echo off
chcp 65001 >nul
echo Starting O&M Assistant (venv mode, auto)...

REM Change to project root directory
cd /d "%~dp0.."
echo Current directory: %CD%

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if venv directory exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Check if requirements.txt exists
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo WARNING: requirements.txt not found, skipping dependency installation
)

REM Create logs directory
if not exist "logs" mkdir logs

REM Check if main.py exists
if exist "main.py" (
    echo.
    echo Starting web application...
    echo Application will open in browser: http://localhost:8501
    echo Press Ctrl+C to stop the application
    echo.

    REM Auto-start streamlit without interactive prompts
    echo "" | streamlit run main.py --server.headless false --server.port 8501
) else (
    echo ERROR: main.py not found in %CD%
    echo Please ensure you are running the script from the correct directory
    pause
    exit /b 1
)

REM Deactivate virtual environment
call .venv\Scripts\deactivate.bat 2>nul

pause