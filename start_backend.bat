@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo Starting CodeWise AI Backend...

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found, creating...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check Python version
echo Checking Python environment...
python --version
if errorlevel 1 (
    echo Python not properly installed or configured
    pause
    exit /b 1
)

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

REM Create necessary directories
echo Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "data\vector_db" mkdir data\vector_db
if not exist "data\knowledge_base" mkdir data\knowledge_base

REM Check environment configuration
if not exist ".env" (
    echo .env file not found, copying example configuration...
    copy .env.example .env
    echo Please edit .env file and configure your API key
    pause
)

REM Set Python path to include current directory
set PYTHONPATH=%CD%;%PYTHONPATH%

REM Start backend service
echo Starting backend service...
echo If errors occur, please check the detailed information...
python backend/main.py

echo.
echo Press any key to exit...
pause >nul