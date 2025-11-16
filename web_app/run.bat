@echo off
REM Financial Planner Web Application - Startup Script for Windows PowerShell

echo.
echo =========================================================
echo Financial Planner Web Application - Startup
echo =========================================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Creating .env from template...
    if exist ".env.example" (
        copy .env.example .env
        echo [INFO] .env created. Please edit it and add your OPENAI_API_KEY
        echo [INFO] Opening .env file...
        start notepad .env
        echo [INFO] After adding your API key, run this script again.
        pause
        exit /b 1
    ) else (
        echo [ERROR] .env.example not found!
        pause
        exit /b 1
    )
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [INFO] Python found: 
python --version

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt

REM Run the Flask app
echo.
echo =========================================================
echo Starting Financial Planner Web Application
echo =========================================================
echo.
echo Opening http://localhost:5000 in your browser...
python app.py
