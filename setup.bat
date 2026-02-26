@echo off
REM Quick setup batch script for Windows PowerShell
REM Usage: setup.bat

echo.
echo ========================================
echo Android Game AI Bot - Quick Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found in PATH
    echo Download from: https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/3] Installing dependencies...
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Read SETUP.md for detailed configuration
echo 2. Edit game_ai_bot/config.py to calibrate grid coordinates
echo 3. Enable USB Debugging on your Android device
echo 4. Connect your device via USB
echo 5. Run: python -m game_ai_bot.main
echo.
pause
